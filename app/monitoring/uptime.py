"""Support pour le ping anti-cold-start (Partie 16 du SRS) : le plan gratuit Render s'endort
après 15 min d'inactivité. Un service externe (UptimeRobot ou cron GitHub Actions) doit
appeler GET /api/v1/health toutes les 14 minutes ; ce module ne fait qu'exposer l'horodatage du
dernier ping reçu pour diagnostic."""
from datetime import datetime, timezone

_last_ping_at: datetime | None = None


def record_ping() -> None:
    global _last_ping_at
    _last_ping_at = datetime.now(timezone.utc)


def last_ping_at() -> datetime | None:
    return _last_ping_at
