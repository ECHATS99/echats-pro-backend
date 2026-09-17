"""Rafraîchit les flux RSS toutes les heures."""
import logging

from app.core.database import SessionLocal
from app.services.rss_service import refresh_all_feeds

logger = logging.getLogger("echats.workers.news")


def run_once() -> int:
    """Exécute un rafraîchissement RSS complet. Retourne le nombre de nouveaux articles."""
    db = SessionLocal()
    try:
        count = refresh_all_feeds(db)
        logger.info("News worker : %s nouveaux articles importés.", count)
        return count
    except Exception:
        logger.exception("Échec du rafraîchissement RSS.")
        return 0
    finally:
        db.close()
