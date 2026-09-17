"""Calculs analytics lourds en arrière-plan (pré-chauffe le cache avant que l'admin
n'ouvre le dashboard, évite un premier chargement lent)."""
import logging

from app.core.database import SessionLocal

logger = logging.getLogger("echats.workers.analytics")


def run_once() -> None:
    from app.modules.analytics.service import courses_analytics, ctf_analytics, dashboard, payments_analytics, users_analytics

    db = SessionLocal()
    try:
        dashboard(db)
        users_analytics(db)
        courses_analytics(db)
        payments_analytics(db)
        ctf_analytics(db)
        logger.info("Cache analytics pré-chauffé.")
    except Exception:
        logger.exception("Échec du pré-chauffage analytics.")
    finally:
        db.close()
