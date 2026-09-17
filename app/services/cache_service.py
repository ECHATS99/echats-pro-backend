"""Couche de cache générique au-dessus de Redis."""
import json
from typing import Any

from app.core.redis import get_redis_client

DEFAULT_TTL_SECONDS = 300


def cache_get(key: str) -> Any | None:
    raw = get_redis_client().get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


def cache_set(key: str, value: Any, ttl: int = DEFAULT_TTL_SECONDS) -> None:
    payload = value if isinstance(value, str) else json.dumps(value, default=str)
    get_redis_client().set(key, payload, ex=ttl)


def cache_delete(*keys: str) -> None:
    if keys:
        get_redis_client().delete(*keys)


def cache_delete_prefix(prefix: str) -> None:
    """Supprime toutes les clés Redis commençant par `prefix` (utilise SCAN pour éviter de bloquer)."""
    client = get_redis_client()
    for key in client.scan_iter(f"{prefix}*"):
        client.delete(key)
