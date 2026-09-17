"""One-shot migration Firestore -> PostgreSQL.

Safety contract:
- ``--dry-run`` is the default and performs no PostgreSQL writes.
- ``--apply`` is required for writes and runs one transaction.
- Firebase Admin credentials are read server-side from FIREBASE_CREDENTIALS_JSON
  or FIREBASE_CREDENTIALS_FILE; they are never printed.
- Existing users and CTF solves are never duplicated.
- Firebase roles/plans are not trusted; imported users receive the backend's
  normal ``student`` role and ``GO`` plan.

Expected legacy Firestore collections (overridable with CLI flags):
  users, leaderboard, submissions, adminChallenges

The legacy frontend used ``users/{uid}``, ``leaderboard/{uid}``, and
``submissions/*``. CTF submissions are imported only when their challenge can
be matched to a PostgreSQL challenge by UUID or by a unique exact title.
Ambiguous/unmatched records are reported and skipped.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# Allow direct execution from the repository root:
# ``python scripts/migrate_firestore_to_postgres.py --dry-run``.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import firebase_admin
from firebase_admin import credentials, firestore
from sqlalchemy import select
from sqlalchemy.orm import Session

# Imported lazily after CLI validation so ``--help`` and missing-configuration
# diagnostics do not construct a PostgreSQL engine at module import time.
SessionLocal = None
DEFAULT_PLAN_ON_REGISTER = None
DEFAULT_ROLE_ON_REGISTER = None
CTFChallenge = Any
CTFSolve = Any
Plan = Any
Role = Any
Subscription = Any
User = Any


def _load_backend_dependencies() -> None:
    global SessionLocal, DEFAULT_PLAN_ON_REGISTER, DEFAULT_ROLE_ON_REGISTER
    global CTFChallenge, CTFSolve, Plan, Role, Subscription, User
    from app.core.constants import DEFAULT_PLAN_ON_REGISTER as default_plan
    from app.core.constants import DEFAULT_ROLE_ON_REGISTER as default_role
    from app.core.database import SessionLocal as session_factory
    from app.models.ctf import CTFChallenge as ctf_challenge, CTFSolve as ctf_solve
    from app.models.plan import Plan as plan_model
    from app.models.role_permission import Role as role_model
    from app.models.subscription import Subscription as subscription_model
    from app.models.user import User as user_model

    DEFAULT_PLAN_ON_REGISTER = default_plan
    DEFAULT_ROLE_ON_REGISTER = default_role
    SessionLocal = session_factory
    CTFChallenge = ctf_challenge
    CTFSolve = ctf_solve
    Plan = plan_model
    Role = role_model
    Subscription = subscription_model
    User = user_model


@dataclass
class UserPlan:
    firebase_uid: str
    email: str
    username: str
    xp: int
    country: str | None = None
    status: str = "active"
    source_doc_id: str = ""
    existing_user_id: uuid.UUID | None = None
    conflict: str | None = None
    planned_user_id: uuid.UUID | None = None
    action: str = "create"


@dataclass
class SolvePlan:
    source_doc_id: str
    firebase_uid: str
    challenge_ref: str
    challenge_title: str | None
    points_firestore: int
    solved_at: datetime | None
    user_id: uuid.UUID | None = None
    challenge_id: uuid.UUID | None = None
    action: str = "import"
    reason: str | None = None


@dataclass
class MigrationReport:
    users_seen: int = 0
    users_to_create: int = 0
    users_existing: int = 0
    users_conflicts: int = 0
    solves_seen: int = 0
    solves_to_import: int = 0
    solves_existing: int = 0
    solves_unmatched: int = 0
    solves_ambiguous: int = 0
    skipped_records: int = 0
    warnings: list[str] = field(default_factory=list)
    user_plans: list[UserPlan] = field(default_factory=list)
    solve_plans: list[SolvePlan] = field(default_factory=list)


class MigrationInputError(RuntimeError):
    pass


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyse et affiche les opérations prévues sans écrire (mode par défaut).",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Applique l'import dans une transaction PostgreSQL. À utiliser seulement après validation du dry-run.",
    )
    parser.add_argument("--users-collection", default=os.getenv("FIRESTORE_USERS_COLLECTION", "users"))
    parser.add_argument("--leaderboard-collection", default=os.getenv("FIRESTORE_LEADERBOARD_COLLECTION", "leaderboard"))
    parser.add_argument("--submissions-collection", default=os.getenv("FIRESTORE_SUBMISSIONS_COLLECTION", "submissions"))
    parser.add_argument("--challenge-collection", default=os.getenv("FIRESTORE_CHALLENGES_COLLECTION", "adminChallenges"))
    parser.add_argument(
        "--max-details",
        type=int,
        default=100,
        help="Nombre maximal de détails affichés par catégorie (les compteurs restent complets).",
    )
    return parser.parse_args()


def _get_firebase_app() -> firebase_admin.App:
    if firebase_admin._apps:
        return firebase_admin.get_app()

    raw_json = os.getenv("FIREBASE_CREDENTIALS_JSON", "").strip()
    credentials_file = os.getenv("FIREBASE_CREDENTIALS_FILE", "").strip()
    if raw_json:
        try:
            cred_info = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise MigrationInputError("FIREBASE_CREDENTIALS_JSON n'est pas un JSON valide.") from exc
        return firebase_admin.initialize_app(credentials.Certificate(cred_info))

    if credentials_file:
        path = Path(credentials_file)
        if not path.is_file():
            raise MigrationInputError("FIREBASE_CREDENTIALS_FILE pointe vers un fichier absent.")
        return firebase_admin.initialize_app(credentials.Certificate(str(path)))

    raise MigrationInputError(
        "Credentials Firebase Admin absentes : configurez FIREBASE_CREDENTIALS_JSON "
        "ou FIREBASE_CREDENTIALS_FILE côté serveur."
    )


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or isinstance(value, bool):
            return default
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


def _as_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    elif hasattr(value, "to_datetime"):
        dt = value.to_datetime()
    elif hasattr(value, "timestamp") and callable(value.timestamp):
        try:
            dt = datetime.fromtimestamp(value.timestamp(), tz=timezone.utc)
        except (TypeError, ValueError, OSError):
            return None
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _string(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def _mask_email(email: str) -> str:
    local, sep, domain = email.partition("@")
    if not sep:
        return "<email-invalide>"
    return f"{local[:1]}***@{domain}"


def _safe_username(email: str, preferred: str | None) -> str:
    raw = (preferred or email.split("@", 1)[0]).strip().lower()
    cleaned = "".join(ch for ch in raw if ch.isalnum() or ch == "_") or "user"
    return cleaned[:50]


def _unique_username(db: Session, base: str, reserved: set[str]) -> str:
    base = base[:50] or "user"
    candidate = base
    suffix = 0
    while candidate in reserved or db.execute(select(User.id).where(User.username == candidate)).scalar_one_or_none():
        suffix += 1
        suffix_text = str(suffix)
        candidate = f"{base[: max(1, 50 - len(suffix_text))]}{suffix_text}"
    reserved.add(candidate)
    return candidate


def _iter_docs(collection_ref: Any) -> list[Any]:
    return list(collection_ref.stream())


def _read_legacy_data(args: argparse.Namespace) -> tuple[list[Any], list[Any], list[Any], list[Any]]:
    _get_firebase_app()
    client = firestore.client()
    users = _iter_docs(client.collection(args.users_collection))
    leaderboard = _iter_docs(client.collection(args.leaderboard_collection))
    submissions = _iter_docs(client.collection(args.submissions_collection))
    challenges = _iter_docs(client.collection(args.challenge_collection))
    return users, leaderboard, submissions, challenges


def _build_user_plans(
    db: Session,
    user_docs: Iterable[Any],
    leaderboard_docs: Iterable[Any],
    report: MigrationReport,
) -> dict[str, UserPlan]:
    leaderboard_by_uid: dict[str, dict[str, Any]] = {}
    for doc in leaderboard_docs:
        data = doc.to_dict() or {}
        uid = _string(data, "uid") or doc.id
        leaderboard_by_uid[uid] = data

    plans: dict[str, UserPlan] = {}
    reserved_usernames: set[str] = set()
    for doc in user_docs:
        report.users_seen += 1
        data = doc.to_dict() or {}
        uid = _string(data, "uid") or doc.id
        email = _string(data, "email")
        if not uid or not email or "@" not in email:
            report.users_conflicts += 1
            report.skipped_records += 1
            report.warnings.append(f"Utilisateur Firestore {doc.id}: uid/email manquant ou invalide.")
            continue

        leaderboard_data = leaderboard_by_uid.get(uid, {})
        preferred_username = _string(data, "username", "displayName", "name") or _string(
            leaderboard_data, "username", "name"
        )
        xp = _as_int(data.get("xp", data.get("pts", data.get("score", leaderboard_data.get("pts", 0)))))
        country = _string(data, "country", "countryCode") or _string(leaderboard_data, "country")
        status = "banned" if bool(data.get("isBanned", False)) else "active"
        existing = db.execute(select(User).where(User.firebase_uid == uid)).scalar_one_or_none()
        if existing is None:
            email_owner = db.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()
            if email_owner is not None:
                plan = UserPlan(
                    firebase_uid=uid,
                    email=email.lower(),
                    username=_safe_username(email, preferred_username),
                    xp=xp,
                    country=country,
                    status=status,
                    source_doc_id=doc.id,
                    conflict=f"email déjà rattaché à firebase_uid={email_owner.firebase_uid}",
                )
                report.users_conflicts += 1
                report.skipped_records += 1
            else:
                username = _unique_username(db, _safe_username(email, preferred_username), reserved_usernames)
                plan = UserPlan(
                    firebase_uid=uid,
                    email=email.lower(),
                    username=username,
                    xp=xp,
                    country=country,
                    status=status,
                    source_doc_id=doc.id,
                    planned_user_id=uuid.uuid4(),
                )
                report.users_to_create += 1
        else:
            plan = UserPlan(
                firebase_uid=uid,
                email=existing.email,
                username=existing.username,
                xp=xp,
                country=country,
                status=existing.status,
                source_doc_id=doc.id,
                existing_user_id=existing.id,
                action="existing",
            )
            report.users_existing += 1
        plans[uid] = plan
        report.user_plans.append(plan)
    return plans


def _challenge_index(db: Session) -> tuple[dict[uuid.UUID, CTFChallenge], dict[str, list[CTFChallenge]]]:
    challenges = list(db.execute(select(CTFChallenge)).scalars().all())
    by_id = {challenge.id: challenge for challenge in challenges}
    by_title: dict[str, list[CTFChallenge]] = {}
    for challenge in challenges:
        by_title.setdefault(challenge.title.strip().casefold(), []).append(challenge)
    return by_id, by_title


def _match_challenge(
    challenge_ref: str,
    challenge_title: str | None,
    by_id: dict[uuid.UUID, CTFChallenge],
    by_title: dict[str, list[CTFChallenge]],
) -> tuple[CTFChallenge | None, str | None]:
    try:
        parsed = uuid.UUID(challenge_ref)
    except (ValueError, AttributeError):
        parsed = None
    if parsed is not None and parsed in by_id:
        return by_id[parsed], None
    if challenge_title:
        matches = by_title.get(challenge_title.strip().casefold(), [])
        if len(matches) == 1:
            return matches[0], None
        if len(matches) > 1:
            return None, "titre de challenge ambigu"
    return None, "challenge Firestore non trouvé dans PostgreSQL"


def _build_solve_plans(
    db: Session,
    submission_docs: Iterable[Any],
    user_plans: dict[str, UserPlan],
    report: MigrationReport,
) -> None:
    by_id, by_title = _challenge_index(db)
    planned_pairs: set[tuple[uuid.UUID, uuid.UUID]] = set()
    for doc in submission_docs:
        data = doc.to_dict() or {}
        if data.get("correct") is False or data.get("result") in {"wrong", "incorrect"}:
            continue
        report.solves_seen += 1
        firebase_uid = _string(data, "userId", "uid", "firebase_uid")
        challenge_ref = _string(data, "challengeId", "challenge_id", "id")
        challenge_title = _string(data, "challengeTitle", "title")
        if not firebase_uid or not challenge_ref:
            report.solves_unmatched += 1
            report.skipped_records += 1
            report.warnings.append(f"Submission Firestore {doc.id}: userId/challengeId manquant.")
            continue
        user_plan = user_plans.get(firebase_uid)
        if user_plan is None or user_plan.conflict:
            report.solves_unmatched += 1
            report.skipped_records += 1
            report.warnings.append(f"Submission {doc.id}: utilisateur {firebase_uid} absent ou en conflit.")
            continue
        challenge, reason = _match_challenge(challenge_ref, challenge_title, by_id, by_title)
        if challenge is None:
            if reason == "titre de challenge ambigu":
                report.solves_ambiguous += 1
            else:
                report.solves_unmatched += 1
            report.skipped_records += 1
            report.solve_plans.append(
                SolvePlan(
                    source_doc_id=doc.id,
                    firebase_uid=firebase_uid,
                    challenge_ref=challenge_ref,
                    challenge_title=challenge_title,
                    points_firestore=_as_int(data.get("pts", data.get("points", 0))),
                    solved_at=_as_datetime(data.get("solvedAt", data.get("solved_at"))),
                    action="skip",
                    reason=reason,
                )
            )
            continue
        user_id = user_plan.existing_user_id or user_plan.planned_user_id
        if user_id is None:
            report.solves_unmatched += 1
            report.skipped_records += 1
            continue
        pair = (user_id, challenge.id)
        existing = db.execute(
            select(CTFSolve.id).where(CTFSolve.user_id == user_id, CTFSolve.challenge_id == challenge.id)
        ).scalar_one_or_none()
        points_firestore = _as_int(data.get("pts", data.get("points", 0)))
        if existing is not None or pair in planned_pairs:
            report.solves_existing += 1
            action = "existing"
        else:
            report.solves_to_import += 1
            planned_pairs.add(pair)
            action = "import"
        if points_firestore and points_firestore != challenge.points:
            report.warnings.append(
                f"Submission {doc.id}: pts Firestore={points_firestore} différent de PostgreSQL={challenge.points}; "
                "la valeur PostgreSQL sera la source de vérité."
            )
        report.solve_plans.append(
            SolvePlan(
                source_doc_id=doc.id,
                firebase_uid=firebase_uid,
                challenge_ref=challenge_ref,
                challenge_title=challenge.title,
                points_firestore=points_firestore,
                solved_at=_as_datetime(data.get("solvedAt", data.get("solved_at"))),
                user_id=user_id,
                challenge_id=challenge.id,
                action=action,
            )
        )


def _apply(db: Session, report: MigrationReport) -> None:
    role = db.execute(select(Role).where(Role.name == DEFAULT_ROLE_ON_REGISTER.value)).scalar_one_or_none()
    if role is None:
        raise MigrationInputError(
            f"Rôle par défaut '{DEFAULT_ROLE_ON_REGISTER.value}' absent; import annulé."
        )
    plan = db.execute(select(Plan).where(Plan.code == DEFAULT_PLAN_ON_REGISTER.value)).scalar_one_or_none()

    created_users: dict[str, User] = {}
    for item in report.user_plans:
        if item.action != "create" or item.conflict:
            continue
        user = User(
            id=item.planned_user_id or uuid.uuid4(),
            firebase_uid=item.firebase_uid,
            email=item.email,
            username=item.username,
            country=item.country,
            xp=item.xp,
            status=item.status,
        )
        user.roles.append(role)
        db.add(user)
        db.flush()
        created_users[item.firebase_uid] = user
        if plan is not None:
            db.add(
                Subscription(
                    id=uuid.uuid4(),
                    user_id=user.id,
                    plan_id=plan.id,
                    status="active",
                    payment_provider=None,
                    starts_at=datetime.now(timezone.utc),
                    expires_at=None,
                )
            )

    for item in report.solve_plans:
        if item.action != "import" or item.user_id is None or item.challenge_id is None:
            continue
        user_id = created_users[item.firebase_uid].id if item.firebase_uid in created_users else item.user_id
        solve = CTFSolve(
            user_id=user_id,
            challenge_id=item.challenge_id,
            points=db.get(CTFChallenge, item.challenge_id).points,
            time=item.solved_at or datetime.now(timezone.utc),
        )
        db.add(solve)
    db.commit()


def _print_report(report: MigrationReport, *, mode: str, max_details: int) -> None:
    payload = {
        "mode": mode,
        "writes_performed": mode == "apply",
        "users": {
            "seen": report.users_seen,
            "to_create": report.users_to_create,
            "already_existing": report.users_existing,
            "conflicts_or_skipped": report.users_conflicts,
        },
        "ctf_solves": {
            "seen_as_correct": report.solves_seen,
            "to_import": report.solves_to_import,
            "already_existing": report.solves_existing,
            "unmatched": report.solves_unmatched,
            "ambiguous": report.solves_ambiguous,
        },
        "skipped_records": report.skipped_records,
        "warnings_count": len(report.warnings),
        "details": {
            "users_to_create": [
                {"firebase_uid": item.firebase_uid, "email": _mask_email(item.email), "username": item.username, "xp": item.xp}
                for item in report.user_plans
                if item.action == "create" and item.conflict is None
            ][:max_details],
            "user_conflicts": [
                {"firebase_uid": item.firebase_uid, "email": _mask_email(item.email), "reason": item.conflict}
                for item in report.user_plans
                if item.conflict
            ][:max_details],
            "solves_to_import": [
                {"firebase_uid": item.firebase_uid, "challenge": item.challenge_title or item.challenge_ref, "points_postgres_source": True}
                for item in report.solve_plans
                if item.action == "import"
            ][:max_details],
            "solves_skipped": [
                {"firebase_uid": item.firebase_uid, "challenge_ref": item.challenge_ref, "reason": item.reason}
                for item in report.solve_plans
                if item.action == "skip"
            ][:max_details],
            "warnings": report.warnings[:max_details],
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def main() -> int:
    args = _parse_args()
    mode = "apply" if args.apply else "dry-run"
    db = None
    try:
        if not os.getenv("DATABASE_URL", "").strip():
            raise MigrationInputError("DATABASE_URL absente; le dry-run doit lire PostgreSQL pour vérifier l'idempotence.")
        _load_backend_dependencies()
        user_docs, leaderboard_docs, submission_docs, _challenge_docs = _read_legacy_data(args)
        db = SessionLocal()
        report = MigrationReport()
        user_plans = _build_user_plans(db, user_docs, leaderboard_docs, report)
        _build_solve_plans(db, submission_docs, user_plans, report)
        if args.apply:
            _apply(db, report)
        _print_report(report, mode=mode, max_details=args.max_details)
        return 0
    except (MigrationInputError, RuntimeError, ValueError, OSError) as exc:
        if db is not None:
            db.rollback()
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - CLI must rollback and expose a concise failure
        if db is not None:
            db.rollback()
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "failed", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    raise SystemExit(main())
