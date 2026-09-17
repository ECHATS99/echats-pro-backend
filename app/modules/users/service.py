"""Logique métier du domaine 'users'. Profil utilisateur, préférences, statistiques,
recherche d'utilisateurs.
Ne contient aucune requête SQL directe : passe par repository.py.
"""
import hashlib
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.core.redis import get_redis_client
from app.core.settings import settings
from app.modules.auth.service import get_active_plan_code, revoke_all_sessions
from app.modules.users import repository as users_repo
from app.modules.users.schemas import (
    TwoFactorEnableRequest, TwoFactorSetupOut, TwoFactorStatusOut,
    UserProfileOut, UserProfileUpdate, UserStatisticsOut,
)
from app.security.encryption import decrypt_bytes, encrypt_bytes
from app.security.rate_limit import check_rate_limit, reset_rate_limit
from app.security.totp import generate_totp_secret, get_provisioning_uri, verify_totp_code_once
from app.services.audit_service import log_action


def get_profile(db: Session, user_id: uuid.UUID) -> UserProfileOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")
    return UserProfileOut(
        id=user.id, email=user.email, username=user.username, avatar_url=user.avatar_url,
        country=user.country, city=user.city, language=user.language, timezone=user.timezone,
        bio=user.bio, xp=user.xp, level=user.level, streak=user.streak,
        role=user.primary_role_name, plan=get_active_plan_code(user),
        institution_id=user.institution_id, created_at=user.created_at,
    )


def update_profile(db: Session, user_id: uuid.UUID, payload: UserProfileUpdate) -> UserProfileOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")

    fields = payload.model_dump(exclude_unset=True)
    users_repo.update_profile_fields(db, user, fields)
    log_action(db, user_id=user_id, action="user.profile_updated", module="users", new_value=fields)
    return get_profile(db, user_id)


def get_statistics(db: Session, user_id: uuid.UUID) -> UserStatisticsOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")

    # Correction Phase 2 : ces domaines sont désormais livrés (voir modules exercises/ctf/
    # certificates/badges) — la note "Phase 1" précédente disant ces champs à 0 est obsolète.
    from sqlalchemy import func, select
    from app.models.flag import Submission
    from app.models.ctf import CTFSolve
    from app.models.certificate import Certificate
    from app.models.badge import UserBadge

    exercises_solved = db.execute(
        select(func.count()).select_from(Submission).where(Submission.user_id == user_id, Submission.correct.is_(True))
    ).scalar_one()
    ctf_solved = db.execute(
        select(func.count()).select_from(CTFSolve).where(CTFSolve.user_id == user_id)
    ).scalar_one()
    certificates_count = db.execute(
        select(func.count()).select_from(Certificate).where(Certificate.user_id == user_id)
    ).scalar_one()
    badges_count = db.execute(
        select(func.count()).select_from(UserBadge).where(UserBadge.user_id == user_id)
    ).scalar_one()

    return UserStatisticsOut(
        xp=user.xp, level=user.level, streak=user.streak,
        exercises_solved=exercises_solved, ctf_solved=ctf_solved,
        certificates_count=certificates_count, badges_count=badges_count,
    )


def search(db: Session, query: str, page: int = 1, limit: int = 20):
    users, total = users_repo.search_users(db, query, page, limit)
    return users, total


def setup_two_factor(db: Session, user_id: uuid.UUID) -> TwoFactorSetupOut:
    """Génère un nouveau secret TOTP et le stocke chiffré (Fernet) en base, mais ne
    l'active pas encore — l'activation effective requiert la confirmation d'un premier
    code valide via `enable_two_factor` (Partie 4.12 du SRS)."""
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")

    secret = generate_totp_secret()
    user.totp_secret_encrypted = encrypt_bytes(secret.encode("utf-8")).decode("utf-8")
    user.totp_enabled = False
    db.add(user)
    db.commit()

    log_action(db, user_id=user_id, action="user.2fa_setup_initiated", module="users")
    return TwoFactorSetupOut(secret=secret, provisioning_uri=get_provisioning_uri(secret, user.email))


def enable_two_factor(
    db: Session,
    user_id: uuid.UUID,
    payload: TwoFactorEnableRequest,
    *,
    redis_client=None,
    client_ip: str | None = None,
) -> TwoFactorStatusOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")
    if not user.totp_secret_encrypted:
        raise ValidationError("Aucune configuration 2FA en attente. Relancez la configuration.")

    secret = decrypt_bytes(user.totp_secret_encrypted.encode("utf-8")).decode("utf-8")
    redis_client = redis_client or get_redis_client()
    user_key = f"ratelimit:2fa:setup:user:{user_id}"
    ip_key = f"ratelimit:2fa:setup:ip:{client_ip or 'unknown'}"
    check_rate_limit(redis_client, user_key, settings.RATE_LIMIT_2FA_PER_MINUTE, 60)
    check_rate_limit(redis_client, ip_key, settings.RATE_LIMIT_2FA_PER_MINUTE, 60)
    subject = f"setup:{user_id}:{hashlib.sha256(secret.encode('utf-8')).hexdigest()[:16]}"
    if not verify_totp_code_once(secret, payload.totp_code, redis_client, subject):
        raise ValidationError("Code de vérification invalide ou déjà utilisé.")
    reset_rate_limit(redis_client, user_key)
    reset_rate_limit(redis_client, ip_key)

    user.totp_enabled = True
    db.add(user)
    db.commit()

    log_action(db, user_id=user_id, action="user.2fa_enabled", module="users")
    return TwoFactorStatusOut(enabled=True)


def disable_two_factor(db: Session, user_id: uuid.UUID) -> TwoFactorStatusOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")

    user.totp_enabled = False
    user.totp_secret_encrypted = None
    db.add(user)
    db.commit()
    # Un changement de facteur d'authentification invalide les sessions existantes.
    revoke_all_sessions(db, user_id)

    log_action(db, user_id=user_id, action="user.2fa_disabled", module="users")
    return TwoFactorStatusOut(enabled=False)


def get_two_factor_status(db: Session, user_id: uuid.UUID) -> TwoFactorStatusOut:
    user = users_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Utilisateur introuvable.")
    return TwoFactorStatusOut(enabled=user.totp_enabled)
