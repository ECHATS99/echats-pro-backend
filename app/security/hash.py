"""Hashing SHA256+sel pour les flags CTF, et hashing des secrets internes (Argon2id)."""
import hashlib
import secrets

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_secret(value: str) -> str:
    """Hash Argon2id d'un secret interne (ex: mot de passe local, si jamais utilisé)."""
    return _pwd_context.hash(value)


def verify_secret(value: str, hashed: str) -> bool:
    """Vérifie un secret contre son hash Argon2id."""
    return _pwd_context.verify(value, hashed)


def generate_salt(length: int = 16) -> str:
    """Génère un sel cryptographiquement sécurisé pour les flags CTF."""
    return secrets.token_hex(length)


def hash_flag(flag: str, salt: str) -> str:
    """Hash SHA256(flag + sel). Le flag en clair n'est jamais stocké (Partie 7 du SRS)."""
    return hashlib.sha256(f"{salt}{flag}".encode("utf-8")).hexdigest()


def verify_flag(flag: str, salt: str, expected_hash: str) -> bool:
    """Vérifie un flag soumis contre son hash stocké, en temps constant."""
    computed = hash_flag(flag, salt)
    return secrets.compare_digest(computed, expected_hash)
