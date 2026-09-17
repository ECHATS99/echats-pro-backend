"""Fonctions utilitaires de fuseau horaire. Le backend stocke tout en UTC (Partie 3.5 du SRS)
et convertit uniquement à l'affichage, jamais en base."""
from datetime import datetime
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = "Africa/Brazzaville"


def to_user_timezone(dt: datetime, timezone_name: str = DEFAULT_TIMEZONE) -> datetime:
    """Convertit un datetime UTC (aware) vers le fuseau horaire de l'utilisateur pour l'affichage."""
    try:
        return dt.astimezone(ZoneInfo(timezone_name))
    except Exception:
        return dt.astimezone(ZoneInfo(DEFAULT_TIMEZONE))
