"""Scheduler léger en tâche de fond asyncio (in-process).

Pour un déploiement multi-workers, remplacer par un scheduler externe (cron GitHub Actions,
Render Cron Job, ou Celery beat) appelant directement les fonctions run_once() de chaque
worker — l'API de chaque worker est déjà conçue pour être invoquée indépendamment.
"""
import asyncio
import logging

logger = logging.getLogger("echats.workers.scheduler")

NEWS_REFRESH_INTERVAL_SECONDS = 3600  # toutes les heures (Partie 11 du SRS)
CLEANUP_INTERVAL_SECONDS = 900  # toutes les 15 minutes
KEEP_ALIVE_INTERVAL_SECONDS = 600  # toutes les 10 minutes (Anti-veille Render)


async def run_scheduler() -> None:
    """Boucle infinie best-effort : ne doit jamais planter le process principal."""
    from app.workers import cleanup_worker, news_worker

    elapsed = 0
    tick = 60
    while True:
        await asyncio.sleep(tick)
        elapsed += tick
        try:
            if elapsed % CLEANUP_INTERVAL_SECONDS == 0:
                cleanup_worker.run_once()
            if elapsed % NEWS_REFRESH_INTERVAL_SECONDS == 0:
                news_worker.run_once()
            
            # Keep-Alive Ping (Anti-veille Render)
            if elapsed % KEEP_ALIVE_INTERVAL_SECONDS == 0:
                import httpx
                import os
                from app.core.settings import settings
                url = os.environ.get("RENDER_EXTERNAL_URL")
                if not url:
                    url = f"http://localhost:{settings.PORT}/api/v1/health"
                else:
                    url = f"{url.rstrip('/')}/api/v1/health"
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    try:
                        response = await client.get(url)
                        logger.info(f"Keep-Alive Ping: Status {response.status_code}")
                    except Exception as e:
                        logger.warning(f"Keep-Alive Ping failed: {e}")
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Erreur non bloquante dans le scheduler.")
