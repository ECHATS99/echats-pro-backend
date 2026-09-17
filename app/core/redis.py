"""Connexion Redis : client utilisé par cache/sessions/rate_limit/leaderboard/websocket."""
from functools import lru_cache

import redis

from app.core.settings import settings


@lru_cache
def get_redis_client() -> redis.Redis:
    """Retourne un client Redis unique (pool de connexions géré par redis-py)."""
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis() -> redis.Redis:
    """Dépendance FastAPI : fournit le client Redis partagé."""
    return get_redis_client()
