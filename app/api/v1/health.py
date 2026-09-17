"""GET /health, /status, /version, /metrics — utilisés par Render/monitoring/Prometheus."""
from fastapi import APIRouter, Response

from app.core.settings import settings
from app.monitoring import health as health_monitor
from app.monitoring import metrics as metrics_monitor
from app.monitoring import uptime as uptime_monitor

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """Endpoint anti-cold-start (Partie 16 du SRS) : ping toutes les 14 min via UptimeRobot/cron."""
    uptime_monitor.record_ping()
    metrics_monitor.increment("health_checks_total")
    return {"status": "ok"}


@router.get("/status")
def status_check():
    """Statut détaillé (DB + Redis), utilisé par le monitoring interne (Partie 7.5 du SRS)."""
    report = health_monitor.full_health_report()
    return {**report, "env": settings.APP_ENV}


@router.get("/version")
def version():
    return {"version": settings.APP_VERSION}


@router.get("/metrics")
def metrics():
    """Format texte compatible Prometheus (Partie 5.32 du SRS)."""
    return Response(content=metrics_monitor.render_prometheus(), media_type="text/plain")
