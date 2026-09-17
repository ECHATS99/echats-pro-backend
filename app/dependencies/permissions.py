"""Dépendances RBAC avec revalidation live depuis PostgreSQL."""
from fastapi import Depends

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.models.user import User
from app.security.rbac import assert_permission


def _live_current_user(cached: CurrentUser, user: User) -> CurrentUser:
    permissions = sorted({permission.name for role in user.roles for permission in role.permissions})
    return CurrentUser(
        id=user.id,
        role=user.primary_role_name,
        plan=cached.plan,
        permissions=permissions,
    )


def require_permission(permission: str):
    """Vérifie la permission live de l'utilisateur actif en base."""
    def _checker(
        cached: CurrentUser = Depends(get_current_user),
        user: User = Depends(get_current_db_user),
    ) -> CurrentUser:
        current = _live_current_user(cached, user)
        assert_permission(current.permissions, permission)
        return current

    return _checker
