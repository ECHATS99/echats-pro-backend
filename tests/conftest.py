"""Fixtures pytest partagées.

Les tests unitaires (tests/unit/) ne dépendent d'aucune infrastructure (pas de DB, pas de
Redis, pas de réseau) et tournent avec un simple `pytest`.

Les tests d'intégration (tests/integration/) nécessitent une base PostgreSQL de test
(variable DATABASE_URL pointant vers une base dédiée, jamais la production) et sont prévus
pour être exécutés dans le pipeline CI (Partie 7.14/7.15 du SRS), pas dans un environnement
sans dépendances installées.
"""
import pytest


class FakeRedis:
    """Double de test minimal pour redis.Redis, suffisant pour rate_limit/cache_service."""

    def __init__(self):
        self._store: dict[str, str] = {}
        self._ttl: dict[str, int] = {}

    def incr(self, key: str) -> int:
        self._store[key] = str(int(self._store.get(key, "0")) + 1)
        return int(self._store[key])

    def expire(self, key: str, seconds: int) -> None:
        self._ttl[key] = seconds

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value: str, ex: int | None = None, nx: bool = False):
        if nx and key in self._store:
            return False
        self._store[key] = value
        if ex:
            self._ttl[key] = ex
        return True

    def getdel(self, key: str):
        value = self._store.pop(key, None)
        self._ttl.pop(key, None)
        return value

    def delete(self, *keys: str) -> None:
        for key in keys:
            self._store.pop(key, None)
            self._ttl.pop(key, None)


@pytest.fixture
def fake_redis() -> FakeRedis:
    return FakeRedis()
