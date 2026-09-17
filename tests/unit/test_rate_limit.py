"""Tests unitaires : rate limiting anti-bruteforce (Partie 7/4.17 du SRS)."""
import pytest

from app.core.exceptions import RateLimitedError
from app.security.rate_limit import check_rate_limit, reset_rate_limit
from tests.conftest import FakeRedis


def test_allows_requests_under_the_limit():
    redis_client = FakeRedis()
    for _ in range(10):
        check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)


def test_blocks_requests_over_the_limit():
    redis_client = FakeRedis()
    for _ in range(10):
        check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)
    with pytest.raises(RateLimitedError):
        check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)


def test_limits_are_isolated_per_key():
    redis_client = FakeRedis()
    for _ in range(10):
        check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)
    # Un autre utilisateur (clé différente) ne doit pas être affecté par le quota de user1.
    check_rate_limit(redis_client, "ratelimit:test:user2", max_requests=10, window_seconds=3600)


def test_reset_rate_limit_clears_counter():
    redis_client = FakeRedis()
    for _ in range(10):
        check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)
    reset_rate_limit(redis_client, "ratelimit:test:user1")
    check_rate_limit(redis_client, "ratelimit:test:user1", max_requests=10, window_seconds=3600)
