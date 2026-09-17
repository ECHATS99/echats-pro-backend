"""Validateurs d'entrée génériques (anti-injection SQL/NoSQL/commande système)."""
import re

from app.core.exceptions import AppError
from app.core.constants import ErrorCode

# Motifs suspects communs (defense-in-depth ; la protection primaire reste les requêtes
# paramétrées SQLAlchemy et la validation de type Pydantic).
_SQL_INJECTION_PATTERN = re.compile(
    r"(--|;|/\*|\*/|\bunion\b|\bselect\b.+\bfrom\b|\bdrop\b\s+\btable\b|\bor\b\s+1\s*=\s*1)",
    re.IGNORECASE,
)
_COMMAND_INJECTION_PATTERN = re.compile(r"[;&|`$]|\$\(|>\s*/dev")
_HTML_TAG_PATTERN = re.compile(r"<\s*script|<\s*iframe|on\w+\s*=", re.IGNORECASE)


def is_suspicious_input(value: str) -> bool:
    """Détection heuristique de contenu potentiellement malveillant dans une chaîne libre."""
    if not isinstance(value, str):
        return False
    return bool(
        _SQL_INJECTION_PATTERN.search(value)
        or _COMMAND_INJECTION_PATTERN.search(value)
        or _HTML_TAG_PATTERN.search(value)
    )


def assert_safe_input(value: str, field_name: str = "champ") -> None:
    """Lève une erreur de validation si l'entrée contient un motif suspect."""
    if is_suspicious_input(value):
        raise AppError(
            f"Le {field_name} contient des caractères non autorisés.",
            ErrorCode.VALIDATION_ERROR,
            422,
        )
