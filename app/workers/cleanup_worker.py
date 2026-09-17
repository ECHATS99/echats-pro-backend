"""Nettoyage des fichiers temporaires, sessions expirées, labs inactifs."""
import logging

from app.core.redis import get_redis_client

logger = logging.getLogger("echats.workers.cleanup")


def run_once() -> None:
    """Purge les clés Redis de sessions/labs expirées (TTL Redis gère déjà la majorité,
    ceci nettoie les clés orphelines de type index qui n'ont pas de TTL propre).
    """
    client = get_redis_client()
    try:
        for key in client.scan_iter("lab_session:*"):
            if client.ttl(key) == -1:  # pas de TTL défini -> orpheline
                client.delete(key)
        logger.info("Cleanup worker exécuté.")
    except Exception:
        logger.exception("Échec du nettoyage périodique.")
