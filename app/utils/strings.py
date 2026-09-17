"""Fonctions utilitaires sur les chaînes de caractères."""
import re
import secrets
import string


def generate_access_code(length: int = 8) -> str:
    """Génère un code d'accès alphanumérique lisible (classrooms, vérification)."""
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def strip_html(value: str) -> str:
    """Retire les balises HTML d'une chaîne (protection XSS basique en complément de Pydantic)."""
    return re.sub(r"<[^>]*>", "", value or "")


def truncate(value: str, length: int = 200, suffix: str = "…") -> str:
    if len(value) <= length:
        return value
    return value[: length - len(suffix)].rstrip() + suffix
