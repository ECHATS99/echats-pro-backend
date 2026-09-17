"""Sauvegardes automatiques (PostgreSQL, Redis, métadonnées Cloudinary — Partie 7.8 du SRS).

Le dump PostgreSQL réel est délégué à `pg_dump` (exécuté par un cron externe Render/GitHub
Actions disposant des credentials DB, hors process applicatif pour raisons de sécurité et de
mémoire). Ce worker se limite à la sauvegarde légère des structures Redis critiques
(feature flags, settings) qui n'ont pas de persistance PostgreSQL propre.
"""
import json
import logging
from datetime import datetime, timezone

from app.core.redis import get_redis_client

logger = logging.getLogger("echats.workers.backup")


def run_once() -> str | None:
    client = get_redis_client()
    snapshot = {}
    for key in client.scan_iter("cache:*"):
        snapshot[key] = client.get(key)

    if not snapshot:
        return None

    backup_key = f"backup:redis:{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    client.set(backup_key, json.dumps(snapshot), ex=7 * 86400)  # conservé 7 jours
    logger.info("Snapshot Redis léger sauvegardé sous %s.", backup_key)
    return backup_key
