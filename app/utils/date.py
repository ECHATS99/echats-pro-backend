"""Fonctions utilitaires de date/heure (toujours en UTC en interne)."""
from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def to_period_str(dt: datetime | None = None) -> str:
    """Retourne une période mensuelle 'YYYY-MM' (utilisé pour paraben_revenue, rapports)."""
    dt = dt or utcnow()
    return dt.strftime("%Y-%m")
