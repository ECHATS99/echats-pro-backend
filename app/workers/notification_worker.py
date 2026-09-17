"""Envoi asynchrone des notifications push/email en masse (campagnes, annonces)."""
import logging

from sqlalchemy.orm import Session

logger = logging.getLogger("echats.workers.notification")


def run_once(db: Session, user_ids: list, type_: str, title: str, message: str) -> int:
    """Diffuse une notification à une liste d'utilisateurs en tâche de fond, pour ne pas
    bloquer la requête HTTP appelante sur de gros volumes (Partie 7.15 du SRS)."""
    from app.modules.notifications.service import create_and_push

    sent = 0
    for user_id in user_ids:
        try:
            create_and_push(db, user_id, type_, title, message)
            sent += 1
        except Exception:
            logger.exception("Échec d'envoi de notification à %s.", user_id)
    return sent
