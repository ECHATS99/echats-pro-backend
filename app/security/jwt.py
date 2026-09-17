"""Génération et validation du JWT interne (access + refresh token).
Contient uniquement user_id/role/plan/permissions/expiration — aucune donnée sensible.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import uuid
from typing import Any, Dict, List

from jose import JWTError, jwt

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.settings import settings

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def _create_token(subject_claims: Dict[str, Any], secret: str, expires_delta: timedelta,
                   token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        **subject_claims,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str, role: str, plan: str, permissions: List[str]) -> str:
    """Génère un access token JWT court-vécu contenant user_id/role/plan/permissions."""
    claims = {"sub": user_id, "role": role, "plan": plan, "permissions": permissions}
    return _create_token(
        claims, settings.JWT_SECRET,
        timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES), TOKEN_TYPE_ACCESS,
    )


def create_refresh_token(user_id: str, session_id: str | None = None) -> str:
    """Génère un refresh token JWT longue durée lié à une session serveur."""
    claims = {"sub": user_id, "sid": session_id or str(uuid.uuid4())}
    return _create_token(
        claims, settings.JWT_REFRESH_SECRET,
        timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS), TOKEN_TYPE_REFRESH,
    )


def _decode(token: str, secret: str, expected_type: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        if "expired" in str(exc).lower():
            raise TokenExpiredError() from exc
        raise InvalidTokenError() from exc

    if payload.get("type") != expected_type:
        raise InvalidTokenError("Type de token invalide.")
    return payload


def decode_access_token(token: str) -> Dict[str, Any]:
    """Décode et valide un access token. Lève TokenExpiredError / InvalidTokenError."""
    return _decode(token, settings.JWT_SECRET, TOKEN_TYPE_ACCESS)


def decode_refresh_token(token: str) -> Dict[str, Any]:
    """Décode et valide un refresh token."""
    return _decode(token, settings.JWT_REFRESH_SECRET, TOKEN_TYPE_REFRESH)


def hash_refresh_token(token: str) -> str:
    """Retourne uniquement le hash SHA-256 d'un refresh token pour stockage serveur."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
