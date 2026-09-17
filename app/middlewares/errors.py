"""Formatage standardisé des erreurs (voir Partie 5.4 du SRS) — jamais de stack trace/secret exposé.

Le formatage effectif est centralisé dans app/core/exceptions.py (register_exception_handlers),
afin qu'un seul endroit gère la sérialisation des erreurs pour toute l'application.
"""
from app.core.exceptions import register_exception_handlers

__all__ = ["register_exception_handlers"]
