"""Extraction/validation du JWT interne sur les requêtes protégées.

Choix d'architecture assumé : plutôt qu'un middleware global (qui devrait deviner quelles
routes sont publiques), l'authentification est appliquée route par route via les
dependencies FastAPI `get_current_user` / `get_current_db_user`
(voir app/dependencies/auth.py) et les dependencies `require_role` / `require_permission`
(voir app/dependencies/roles.py et permissions.py). Cela respecte le principe Zero Trust
(Partie 8.3 du SRS) sans exposer par erreur une route censée être publique (health, auth/login).

Ce module ne contient donc pas de middleware Starlette actif ; il documente ce choix et
réexporte les dependencies pour un import pratique depuis un seul endroit si besoin.
"""
from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user

__all__ = ["CurrentUser", "get_current_user", "get_current_db_user"]
