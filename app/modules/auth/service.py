"""Service métier d'authentification et de gestion des sessions."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.constants import DEFAULT_PLAN_ON_REGISTER, ROLES_REQUIRING_2FA
from app.core.exceptions import AccountSuspendedError, TwoFactorRequiredError, UnauthorizedError
from app.core.redis import get_redis_client
from app.core.security import FirebaseTokenError, verify_firebase_token
from app.core.settings import settings
from app.models.refresh_session import RefreshSession
from app.models.user import User
from app.modules.auth import repository as auth_repo
from app.modules.auth import session_repository as sessions_repo
from app.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_refresh_token,
)
from app.security.rate_limit import check_rate_limit, reset_rate_limit
from app.security.totp import verify_totp_code_once
from app.services.audit_service import log_action


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def get_active_plan_code(user: User) -> str:
    """Retourne le code du plan actif le plus récent, ou GO par défaut."""
    now = _now()
    for sub in user.subscriptions:
        if sub.status in ("active", "trial") and (sub.expires_at is None or _as_utc(sub.expires_at) > now):
            return sub.plan.code
    return DEFAULT_PLAN_ON_REGISTER.value


def _flatten_permissions(user: User) -> list[str]:
    perms: set[str] = set()
    for role in user.roles:
        for perm in role.permissions:
            perms.add(perm.name)
    return sorted(perms)


def _assert_account_usable(user: User) -> None:
    if user.status == "suspended":
        raise AccountSuspendedError("Votre compte est suspendu. Contactez le support.")
    if user.status == "banned":
        raise AccountSuspendedError("Votre compte a été banni.")


def _issue_tokens(
    db: Session,
    user: User,
    *,
    role_name: str,
    plan_code: str,
    permissions: list[str],
    client_ip: str | None,
    user_agent: str | None,
) -> tuple[str, str]:
    access_token = create_access_token(str(user.id), role_name, plan_code, permissions)
    session_id = uuid.uuid4()
    refresh_token = create_refresh_token(str(user.id), str(session_id))
    sessions_repo.create(
        db,
        user_id=user.id,
        session_id=session_id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=_now() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        user_agent=user_agent,
        ip_address=client_ip,
    )
    return access_token, refresh_token


def _verify_required_2fa(
    user: User,
    totp_code: str | None,
    client_ip: str | None,
    redis_client,
) -> None:
    if not user.totp_enabled:
        raise TwoFactorRequiredError("Activez le 2FA sur votre compte pour continuer.")
    if not totp_code:
        raise TwoFactorRequiredError()

    ip_key = f"ratelimit:2fa:ip:{client_ip or 'unknown'}"
    user_key = f"ratelimit:2fa:user:{user.id}"
    check_rate_limit(redis_client, ip_key, settings.RATE_LIMIT_2FA_PER_MINUTE, 60)
    check_rate_limit(redis_client, user_key, settings.RATE_LIMIT_2FA_PER_MINUTE, 60)

    from app.security.encryption import decrypt_bytes
    secret = decrypt_bytes(user.totp_secret_encrypted.encode("utf-8")).decode("utf-8")
    if not verify_totp_code_once(secret, totp_code, redis_client, str(user.id)):
        raise TwoFactorRequiredError("Code TOTP invalide ou déjà utilisé.")

    reset_rate_limit(redis_client, ip_key)
    reset_rate_limit(redis_client, user_key)


def authenticate_with_firebase(
    db: Session,
    id_token: str,
    totp_code: str | None,
    client_ip: str | None,
    redis_client=None,
    user_agent: str | None = None,
) -> tuple[User, str, str]:
    """Vérifie Firebase, applique le 2FA et ouvre une session refresh serveur."""
    try:
        identity = verify_firebase_token(id_token)
    except FirebaseTokenError as exc:
        raise UnauthorizedError("Token Firebase invalide ou expiré.") from exc

    user = auth_repo.get_user_by_firebase_uid(db, identity.uid)
    is_first_access = user is None
    if user is None:
        if not identity.email or not identity.email_verified:
            raise UnauthorizedError("Un email vérifié est requis pour créer un compte.")
        user = auth_repo.create_user_from_firebase(db, identity.uid, identity.email)

    _assert_account_usable(user)

    role_name = user.primary_role_name
    if role_name in {r.value for r in ROLES_REQUIRING_2FA}:
        _verify_required_2fa(user, totp_code, client_ip, redis_client or get_redis_client())

    plan_code = get_active_plan_code(user)
    permissions = _flatten_permissions(user)
    access_token, refresh_token = _issue_tokens(
        db,
        user,
        role_name=role_name,
        plan_code=plan_code,
        permissions=permissions,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    auth_repo.update_last_login(db, user, client_ip)
    log_action(
        db,
        user_id=user.id,
        role=role_name,
        action="user.registered" if is_first_access else "user.login",
        module="auth",
        ip_address=client_ip,
    )

    return user, access_token, refresh_token


def refresh_access_token(
    db: Session,
    refresh_token: str,
    *,
    client_ip: str | None = None,
    user_agent: str | None = None,
) -> tuple[str, str]:
    """Valide puis fait tourner un refresh token à usage unique."""
    payload = decode_refresh_token(refresh_token)
    try:
        session_id = uuid.UUID(str(payload["sid"]))
        user_id = uuid.UUID(str(payload["sub"]))
    except (KeyError, ValueError, TypeError) as exc:
        raise UnauthorizedError("Session invalide.") from exc

    session = sessions_repo.get_by_session_id_for_update(db, session_id)
    if session is None or session.user_id != user_id:
        raise UnauthorizedError("Session invalide.")

    if session.revoked_at is not None:
        # Réutilisation d'un token déjà tourné : révoquer toutes les sessions de l'utilisateur.
        sessions_repo.revoke_all(db, user_id)
        raise UnauthorizedError("Session invalide ou réutilisée.")
    if _as_utc(session.expires_at) <= _now():
        sessions_repo.revoke(db, session)
        raise UnauthorizedError("Session expirée.")
    if not secrets_compare(hash_refresh_token(refresh_token), session.token_hash):
        raise UnauthorizedError("Session invalide.")

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("Session invalide.")

    role_name = user.primary_role_name
    plan_code = get_active_plan_code(user)
    permissions = _flatten_permissions(user)
    access_token = create_access_token(str(user.id), role_name, plan_code, permissions)
    new_session_id = uuid.uuid4()
    new_refresh_token = create_refresh_token(str(user.id), str(new_session_id))
    new_session = RefreshSession(
        user_id=user.id,
        session_id=new_session_id,
        token_hash=hash_refresh_token(new_refresh_token),
        expires_at=_now() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        user_agent=user_agent,
        ip_address=client_ip,
    )
    session.revoked_at = _now()
    session.replaced_by_session_id = new_session_id
    session.last_used_at = _now()
    db.add(session)
    db.add(new_session)
    db.commit()
    return access_token, new_refresh_token


def secrets_compare(left: str, right: str) -> bool:
    """Comparaison en temps constant sans exposer de primitive supplémentaire."""
    import secrets
    return secrets.compare_digest(left, right)


def revoke_refresh_token(db: Session, refresh_token: str, user_id: uuid.UUID) -> None:
    """Révoque individuellement un refresh token appartenant à l'utilisateur courant."""
    try:
        payload = decode_refresh_token(refresh_token)
        session_id = uuid.UUID(str(payload["sid"]))
        token_user_id = uuid.UUID(str(payload["sub"]))
    except (KeyError, ValueError, TypeError):
        raise UnauthorizedError("Session invalide.")
    if token_user_id != user_id:
        raise UnauthorizedError("Session invalide.")
    session = sessions_repo.get_by_session_id(db, session_id)
    if session is None or session.user_id != user_id:
        raise UnauthorizedError("Session invalide.")
    if session.revoked_at is None:
        sessions_repo.revoke(db, session)


def revoke_all_sessions(db: Session, user_id: uuid.UUID) -> None:
    """Révoque toutes les sessions actives d'un utilisateur."""
    sessions_repo.revoke_all(db, user_id)
