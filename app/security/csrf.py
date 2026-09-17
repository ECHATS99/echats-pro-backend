"""Protection CSRF sur les routes sensibles (double-submit cookie)."""
import secrets

CSRF_COOKIE_NAME = "echats_csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"


def generate_csrf_token() -> str:
    """Génère un token CSRF cryptographiquement sécurisé."""
    return secrets.token_urlsafe(32)


def validate_csrf(cookie_value: str | None, header_value: str | None) -> bool:
    """Compare le token du cookie et celui du header (pattern double-submit)."""
    if not cookie_value or not header_value:
        return False
    return secrets.compare_digest(cookie_value, header_value)
