"""Validateurs réutilisables au-delà de ce que Pydantic fournit nativement (Partie 8.4 du SRS :
contrôles obligatoires sur taille/type/format/caractères interdits)."""
import re

_PHONE_RE = re.compile(r"^\+?[0-9]{8,15}$")
_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_DANGEROUS_HTML_RE = re.compile(r"<\s*(script|iframe|object|embed)\b", re.IGNORECASE)


def is_valid_phone(value: str) -> bool:
    return bool(_PHONE_RE.match(value))


def is_valid_slug(value: str) -> bool:
    return bool(_SLUG_RE.match(value))


def contains_dangerous_html(value: str) -> bool:
    """Détecte les balises HTML potentiellement dangereuses (protection XSS en complément
    de la validation Pydantic — Partie 8.4 du SRS)."""
    return bool(_DANGEROUS_HTML_RE.search(value or ""))


def is_safe_text(value: str, max_length: int = 10000) -> bool:
    if len(value) > max_length:
        return False
    return not contains_dangerous_html(value)
