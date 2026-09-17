"""Logique métier du domaine 'ctf'. Évènements CTF, catégories, challenges, soumissions de flags
(SHA256+sel), classement. Ne contient aucune requête SQL directe : passe par repository.py.
"""
import uuid

import redis

from app.core.exceptions import NotFoundError
from app.models.ctf import CTFChallenge
from app.modules.ctf import repository as ctf_repo
from app.modules.ctf.schemas import (
    CTFCategoryOut, CTFChallengeCreate, CTFChallengeOut, CTFChallengeUpdate,
    CTFEventOut, CTFFlagSubmission, CTFLeaderboardEntry, CTFSubmitResult,
)
from app.security.hash import generate_salt, hash_flag, verify_flag
from app.security.rate_limit import check_rate_limit
from app.services.audit_service import log_action
from app.services.badge_service import evaluate_badges_for_condition
from app.services.websocket_service import broadcast_activity, broadcast_leaderboard_update
from app.services.xp_service import award_xp

FLAG_RATE_LIMIT_MAX = 10
FLAG_RATE_LIMIT_WINDOW_SECONDS = 3600


def list_events(db) -> list[CTFEventOut]:
    return [CTFEventOut.model_validate(e) for e in ctf_repo.list_events(db)]


def list_categories(db) -> list[CTFCategoryOut]:
    return [CTFCategoryOut.model_validate(c) for c in ctf_repo.list_categories(db)]


def list_challenges(db, user_id: uuid.UUID | None, category_id: uuid.UUID | None, event_id: uuid.UUID | None) -> list[CTFChallengeOut]:
    solved_ids = ctf_repo.solved_challenge_ids_for_user(db, user_id) if user_id else set()
    challenges = ctf_repo.list_challenges(db, category_id=category_id, event_id=event_id, published_only=True)
    out = []
    for c in challenges:
        item = CTFChallengeOut.model_validate(c)
        item.solved_by_me = c.id in solved_ids
        out.append(item)
    return out


def get_challenge(db, challenge_id: uuid.UUID, user_id: uuid.UUID | None) -> CTFChallengeOut:
    challenge = ctf_repo.get_challenge(db, challenge_id)
    if challenge is None:
        raise NotFoundError("Challenge CTF introuvable.")
    item = CTFChallengeOut.model_validate(challenge)
    item.solved_by_me = user_id is not None and ctf_repo.has_solved(db, user_id, challenge_id)
    return item


def create_challenge(db, payload: CTFChallengeCreate, actor_id: uuid.UUID) -> CTFChallengeOut:
    salt = generate_salt()
    fields = payload.model_dump(exclude={"flag"})
    challenge = CTFChallenge(**fields, flag_hash=hash_flag(payload.flag, salt), flag_salt=salt)
    challenge = ctf_repo.create_challenge(db, challenge)
    log_action(db, user_id=actor_id, action="ctf.created", module="ctf", resource="challenge", resource_id=str(challenge.id))
    return get_challenge(db, challenge.id, actor_id)


def update_challenge(db, challenge_id: uuid.UUID, payload: CTFChallengeUpdate, actor_id: uuid.UUID) -> CTFChallengeOut:
    challenge = ctf_repo.get_challenge(db, challenge_id)
    if challenge is None:
        raise NotFoundError("Challenge CTF introuvable.")

    fields = payload.model_dump(exclude={"flag"}, exclude_unset=True)
    if payload.flag:
        salt = generate_salt()
        fields["flag_hash"] = hash_flag(payload.flag, salt)
        fields["flag_salt"] = salt
    challenge = ctf_repo.update_challenge(db, challenge, fields)
    log_action(db, user_id=actor_id, action="ctf.updated", module="ctf", resource="challenge", resource_id=str(challenge.id))
    return get_challenge(db, challenge.id, actor_id)


def delete_challenge(db, challenge_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    challenge = ctf_repo.get_challenge(db, challenge_id)
    if challenge is None:
        raise NotFoundError("Challenge CTF introuvable.")
    ctf_repo.delete_challenge(db, challenge)
    log_action(db, user_id=actor_id, action="ctf.deleted", module="ctf", resource="challenge", resource_id=str(challenge_id))


def submit_flag(db, redis_client: redis.Redis, challenge_id: uuid.UUID, user_id: uuid.UUID, payload: CTFFlagSubmission) -> CTFSubmitResult:
    challenge = ctf_repo.get_challenge(db, challenge_id)
    if challenge is None:
        raise NotFoundError("Challenge CTF introuvable.")

    check_rate_limit(
        redis_client, f"ratelimit:ctf_submit:{user_id}:{challenge_id}",
        FLAG_RATE_LIMIT_MAX, FLAG_RATE_LIMIT_WINDOW_SECONDS,
    )

    if ctf_repo.has_solved(db, user_id, challenge_id):
        log_action(db, user_id=user_id, action="ctf.flag_replay", module="ctf", resource="challenge", resource_id=str(challenge_id))
        return CTFSubmitResult(correct=True, points=0, message="Déjà résolu.")

    is_correct = verify_flag(payload.flag, challenge.flag_salt, challenge.flag_hash)
    if not is_correct:
        log_action(db, user_id=user_id, action="ctf.flag_incorrect", module="ctf", resource="challenge", resource_id=str(challenge_id))
        return CTFSubmitResult(correct=False, points=0, message="Flag incorrect.")

    ctf_repo.record_solve(db, user_id, challenge_id, challenge.points)
    award_xp(db, user_id, challenge.points, f"ctf_solved:{challenge_id}")

    solves_count = ctf_repo.user_solve_count(db, user_id)
    evaluate_badges_for_condition(db, user_id, "ctf_solves", solves_count)

    broadcast_activity({"user_id": str(user_id), "event": "ctf_solved", "challenge_id": str(challenge_id), "points": challenge.points})
    broadcast_leaderboard_update({"event": "ctf_solve", "user_id": str(user_id)})
    log_action(db, user_id=user_id, action="ctf.flag_correct", module="ctf", resource="challenge", resource_id=str(challenge_id))

    return CTFSubmitResult(correct=True, points=challenge.points, message="Flag correct !")


def get_leaderboard(db) -> list[CTFLeaderboardEntry]:
    rows = ctf_repo.leaderboard(db)
    return [CTFLeaderboardEntry(user_id=r.id, username=r.username, total_points=r.total_points, solves_count=r.solves_count) for r in rows]
