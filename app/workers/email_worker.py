"""Envoi asynchrone des emails (file simple via Redis, best effort)."""
import json
import logging

from app.core.redis import get_redis_client
from app.services.email_service import send_email

logger = logging.getLogger("echats.workers.email")
QUEUE_KEY = "queue:emails"


def enqueue(to: str, subject: str, html: str) -> None:
    get_redis_client().rpush(QUEUE_KEY, json.dumps({"to": to, "subject": subject, "html": html}))


def run_once(batch_size: int = 20) -> int:
    """Dépile et envoie jusqu'à `batch_size` emails en attente. Retourne le nombre envoyé."""
    client = get_redis_client()
    sent = 0
    for _ in range(batch_size):
        raw = client.lpop(QUEUE_KEY)
        if raw is None:
            break
        try:
            job = json.loads(raw)
            send_email(job["to"], job["subject"], job["html"])
            sent += 1
        except Exception:
            logger.exception("Échec d'envoi d'un email en file.")
    return sent
