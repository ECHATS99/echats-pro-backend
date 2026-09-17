"""Dépendance de contrôle de rôle avec revalidation depuis PostgreSQL."""
from fastapi import Depends

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.models.user import User
from app.security.rbac import assert_role


def require_role(*allowed_roles: str):
    """Vérifie le rôle principal live de l'utilisateur actif."""
    def _checker(
        cached: CurrentUser = Depends(get_current_user),
        user: User = Depends(get_current_db_user),
    ) -> CurrentUser:
        current = CurrentUser(
            id=user.id,
            role=user.primary_role_name,
            plan=cached.plan,
            permissions=sorted({permission.name for role in user.roles for permission in role.permissions}),
        )
        assert_role(current.role, allowed_roles)
        return current

    return _checker
