"""Chiffrement des documents sensibles de la Chambre Close (Fernet / AES-128-CBC + HMAC)."""
from functools import lru_cache

from cryptography.fernet import Fernet

from app.core.exceptions import AppError
from app.core.constants import ErrorCode
from app.core.settings import settings


@lru_cache
def _get_fernet() -> Fernet:
    if not settings.CHAMBER_CLOSE_ENCRYPTION_KEY:
        # On refuse explicitement de fonctionner avec une clé devinée ou dérivée :
        # une clé Fernet dédiée doit être générée (Fernet.generate_key()) et injectée
        # via la variable d'environnement CHAMBER_CLOSE_ENCRYPTION_KEY.
        raise AppError(
            "CHAMBER_CLOSE_ENCRYPTION_KEY n'est pas configurée.",
            ErrorCode.INTERNAL_ERROR, 500,
        )
    return Fernet(settings.CHAMBER_CLOSE_ENCRYPTION_KEY.encode("utf-8"))


def encrypt_bytes(data: bytes) -> bytes:
    """Chiffre un contenu (document Chambre Close) avant stockage."""
    return _get_fernet().encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    """Déchiffre un contenu précédemment chiffré."""
    return _get_fernet().decrypt(token)
