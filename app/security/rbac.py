"""Moteur de vérification des rôles et permissions à chaque requête.
Zero Trust : ne jamais faire confiance au frontend, tout est revérifié côté backend
à partir des données rechargées depuis PostgreSQL (jamais depuis le JWT seul pour les
opérations sensibles — le JWT sert de cache court-vécu des permissions au moment de l'émission).
"""
from typing import Iterable

from app.core.exceptions import ForbiddenError


def has_permission(user_permissions: Iterable[str], required_permission: str) -> bool:
    """Vérifie qu'une permission précise (ex: 'ctf.create') est présente."""
    return required_permission in set(user_permissions)


def has_role(user_role: str, required_roles: Iterable[str]) -> bool:
    """Vérifie que le rôle de l'utilisateur fait partie des rôles autorisés."""
    return user_role in set(required_roles)


def assert_permission(user_permissions: Iterable[str], required_permission: str) -> None:
    """Lève ForbiddenError si la permission n'est pas présente."""
    if not has_permission(user_permissions, required_permission):
        raise ForbiddenError(f"Permission manquante : {required_permission}")


def assert_role(user_role: str, required_roles: Iterable[str]) -> None:
    """Lève ForbiddenError si le rôle n'est pas autorisé."""
    if not has_role(user_role, required_roles):
        raise ForbiddenError("Rôle non autorisé pour cette action.")


def assert_same_institution(user_institution_id, resource_institution_id) -> None:
    """Isolation multi-tenant (Partie 4.11 du SRS) : une organisation ne voit jamais les
    données d'une autre. Lève ForbiddenError en cas de mismatch."""
    if resource_institution_id is not None and user_institution_id != resource_institution_id:
        raise ForbiddenError("Cette ressource n'appartient pas à votre institution.")
