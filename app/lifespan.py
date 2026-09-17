"""Gestion du cycle de vie : connexion/déconnexion DB, Redis, démarrage/arrêt des workers
au lancement de l'app.
"""
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.core.redis import get_redis_client
from app.websocket.manager import connection_manager

logger = logging.getLogger("echats.lifespan")

_scheduler_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_task
    logger.info("Démarrage ECHATS PRO backend...")

    # Vérifie la connexion Redis dès le démarrage (fail-fast)
    try:
        get_redis_client().ping()
        logger.info("Connexion Redis OK.")
    except Exception:
        logger.exception("Impossible de se connecter à Redis au démarrage.")

    # Permet aux services synchrones (xp_service, badge_service, ...) de programmer
    # des envois WebSocket depuis n'importe quel thread/contexte.
    connection_manager.bind_loop(asyncio.get_event_loop())

    # Scheduler léger en tâche de fond : rafraîchissement RSS toutes les heures,
    # nettoyage, etc. Best effort — une erreur d'un tick n'arrête jamais le backend.
    from app.workers.scheduler import run_scheduler
    _scheduler_task = asyncio.create_task(run_scheduler())

    yield

    logger.info("Arrêt ECHATS PRO backend...")
    if _scheduler_task is not None:
        _scheduler_task.cancel()
    engine.dispose()
