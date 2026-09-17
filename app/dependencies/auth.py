"""Dependency FastAPI get_current_user() : décode le JWT interne, retourne l'utilisateur.

Deux niveaux sont exposés :
- get_current_user      : rapide, ne lit que les claims du JWT (role/plan/permissions).
                           Suffisant pour la plupart des routes.
- get_current_db_user   : recharge l'utilisateur depuis PostgreSQL (Zero Trust — Partie 8.3
                           du SRS) et revérifie que le compte est toujours actif. À utiliser
                           pour les opérations sensibles (paiement, admin, suppression...).
"""
import uuid
from dataclasses import dataclass

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AccountSuspendedError, UnauthorizedError
from app.dependencies.database import get_db
from app.models.user import User
from app.security.jwt import decode_access_token

_bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    id: uuid.UUID
    role: str
    plan: str
    permissions: list[str]


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> CurrentUser:
    """Décode l'access token JWT et retourne les claims (id/role/plan/permissions)."""
    if credentials is None:
        raise UnauthorizedError("Token d'authentification manquant.")

    payload = decode_access_token(credentials.credentials)
    return CurrentUser(
        id=uuid.UUID(payload["sub"]),
        role=payload["role"],
        plan=payload["plan"],
        permissions=payload.get("permissions", []),
    )


def get_current_db_user(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Recharge l'utilisateur depuis PostgreSQL et revérifie son statut (Zero Trust)."""
    user = db.get(User, current.id)
    if user is None or not user.is_active:
        raise AccountSuspendedError("Ce compte n'est plus actif.")
    return user
