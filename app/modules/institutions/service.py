"""Logique métier institutions (Chambre Close)."""
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError, ConflictError
from app.models.institution import Institution
from app.models.user import User
from app.modules.institutions import repository as repo
from app.modules.institutions.schemas import (
    InstitutionCreate, InstitutionOut, InstitutionUpdate,
    AccessKeyCreate, AccessKeyOut, JoinResult,
)
from app.services.audit_service import log_action


def _gen_prefix(code: str) -> str:
    """PRBN depuis PARABEN-CORP, ECHT depuis ECHATS-ACADEMY."""
    clean = "".join(c for c in code.upper() if c.isalnum())
    return (clean[:4] or "INST").ljust(4, "X")


def _gen_key(prefix: str, role: str) -> str:
    rand = secrets.token_hex(3).upper()  # 6 chars
    return f"{prefix}-{role}-{rand}"


def list_institutions(db: Session) -> list[InstitutionOut]:
    out = []
    for inst in repo.list_institutions(db):
        data = InstitutionOut.model_validate(inst).model_dump()
        data["members_count"] = repo.count_members(db, inst.id)
        out.append(InstitutionOut(**data))
    return out


def get_institution(db: Session, id_or_slug: str) -> InstitutionOut:
    inst = None
    try:
        inst = repo.get_institution(db, uuid.UUID(id_or_slug))
    except (ValueError, AttributeError):
        pass
    if inst is None:
        inst = repo.get_by_slug_or_code(db, id_or_slug)
    if inst is None:
        raise NotFoundError("Institut introuvable.")
    repo.increment_visitors(db, inst)
    data = InstitutionOut.model_validate(inst).model_dump()
    data["members_count"] = repo.count_members(db, inst.id)
    return InstitutionOut(**data)


def create_institution(db: Session, payload: InstitutionCreate, actor_id: uuid.UUID) -> InstitutionOut:
    data = payload.model_dump()
    data["slug"] = data.get("slug") or data["code"].lower().replace("_", "-")
    data["prefix"] = _gen_prefix(data["code"])
    data["owner_uid"] = str(actor_id)
    data["active"] = True
    data["members_count"] = 0
    data["visitors_count"] = 0
    inst = repo.create_institution(db, data)
    log_action(db, user_id=actor_id, action="institution.created",
               module="institutions", resource="institution", resource_id=str(inst.id))
    return InstitutionOut.model_validate(inst)


def update_institution(db: Session, inst_id: uuid.UUID, payload: InstitutionUpdate, actor_id: uuid.UUID) -> InstitutionOut:
    inst = repo.get_institution(db, inst_id)
    if inst is None:
        raise NotFoundError("Institut introuvable.")
    updated = repo.update_institution(db, inst, payload.model_dump(exclude_unset=True))
    log_action(db, user_id=actor_id, action="institution.updated",
               module="institutions", resource="institution", resource_id=str(inst_id))
    return InstitutionOut.model_validate(updated)


def list_members(db: Session, inst_id: uuid.UUID) -> list[dict]:
    from sqlalchemy import select
    stmt = select(User).where(User.institution_id == inst_id)
    users = db.execute(stmt).scalars().all()
    return [
        {"id": str(u.id), "username": u.username, "email": u.email,
         "xp": u.xp, "level": u.level, "status": u.status}
        for u in users
    ]


# --- Access Keys ---

def generate_access_key(db: Session, inst_id: uuid.UUID, payload: AccessKeyCreate, actor_id: uuid.UUID) -> AccessKeyOut:
    inst = repo.get_institution(db, inst_id)
    if inst is None:
        raise NotFoundError("Institut introuvable.")

    prefix = getattr(inst, "prefix", None) or _gen_prefix(inst.code)

    # Générer une clé unique (max 5 essais)
    key_value = None
    for _ in range(5):
        candidate = _gen_key(prefix, payload.assigned_role)
        if not repo.key_exists(db, candidate):
            key_value = candidate
            break
    if key_value is None:
        raise ConflictError("Impossible de générer une clé unique. Réessayez.")

    expires = datetime.now(timezone.utc) + timedelta(days=payload.days_valid)

    k = repo.create_access_key(db, {
        "institution_id": inst_id,
        "key": key_value,
        "assigned_role": payload.assigned_role,
        "max_uses": payload.max_uses,
        "current_uses": 0,
        "expires_at": expires,
        "created_by": actor_id,
        "is_active": True,
    })
    log_action(db, user_id=actor_id, action="institution.key_generated",
               module="institutions", resource="access_key", resource_id=str(k.id))
    return AccessKeyOut.model_validate(k)


def list_keys(db: Session, inst_id: uuid.UUID) -> list[AccessKeyOut]:
    return [AccessKeyOut.model_validate(k) for k in repo.list_access_keys(db, inst_id)]


def revoke_key(db: Session, key_id: uuid.UUID, actor_id: uuid.UUID) -> dict:
    from sqlalchemy import select
    stmt = select(repo.InstitutionAccessKey).where(repo.InstitutionAccessKey.id == key_id)
    k = db.execute(stmt).scalar_one_or_none()
    if k is None:
        raise NotFoundError("Clé introuvable.")
    repo.revoke_access_key(db, k)
    log_action(db, user_id=actor_id, action="institution.key_revoked",
               module="institutions", resource="access_key", resource_id=str(key_id))
    return {"success": True, "message": "Clé révoquée."}


def join_with_key(db: Session, key_value: str, user: User) -> JoinResult:
    """Rejoindre une institution avec une clé."""
    clean = key_value.strip().upper()
    k = repo.get_access_key_by_value(db, clean)
    if k is None:
        return JoinResult(success=False, message="Clé invalide.")
    if not k.is_active:
        return JoinResult(success=False, message="Cette clé est désactivée.")
    if k.expires_at and k.expires_at < datetime.now(timezone.utc):
        return JoinResult(success=False, message="Cette clé a expiré.")
    if k.current_uses >= k.max_uses:
        return JoinResult(success=False, message="Cette clé a atteint sa limite d'utilisation.")

    inst = repo.get_institution(db, k.institution_id)
    if inst is None:
        return JoinResult(success=False, message="Institut introuvable.")

    # Rejoindre
    user.institution_id = k.institution_id
    db.add(user)
    repo.consume_key_use(db, k)
    db.commit()

    log_action(db, user_id=user.id, action="institution.joined_with_key",
               module="institutions", resource="institution", resource_id=str(k.institution_id))

    return JoinResult(
        success=True,
        institution_id=inst.id,
        institution_name=inst.name,
        role=k.assigned_role,
        message=f"Bienvenue dans {inst.name} !",
    )


def join_direct(db: Session, inst_id: uuid.UUID, user: User) -> JoinResult:
    """Rejoindre une institution publique sans clé (ex: ECHATS ACADEMY)."""
    inst = repo.get_institution(db, inst_id)
    if inst is None:
        raise NotFoundError("Institut introuvable.")
    if not getattr(inst, "is_public", False) and inst.requires_key:
        raise ForbiddenError("Cet institut est privé. Une clé d'accès est requise.")

    user.institution_id = inst.id
    db.add(user)
    db.commit()

    log_action(db, user_id=user.id, action="institution.joined_direct",
               module="institutions", resource="institution", resource_id=str(inst.id))

    return JoinResult(
        success=True,
        institution_id=inst.id,
        institution_name=inst.name,
        role="ELEVE",
        message=f"Bienvenue dans {inst.name} !",
    )
