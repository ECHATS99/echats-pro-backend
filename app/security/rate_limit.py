"""Rate limiting Redis par route (login 5/min, IA selon plan, upload 50/jour, etc.
Voir Partie 4.17 du SRS). Implémentation par fenêtre glissante simple (INCR + EXPIRE).
"""
import redis

from app.core.exceptions import RateLimitedError


def check_rate_limit(redis_client: redis.Redis, key: str, max_requests: int, window_seconds: int) -> None:
    """Incrémente le compteur pour `key` et lève RateLimitedError si le quota est dépassé.

    `key` doit déjà inclure l'identifiant de l'utilisateur/IP et le nom de la route,
    ex: "ratelimit:login:1.2.3.4".
    """
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, window_seconds)
    if current > max_requests:
        raise RateLimitedError(f"Limite de {max_requests} requêtes atteinte, réessayez plus tard.")


def reset_rate_limit(redis_client: redis.Redis, key: str) -> None:
    """Réinitialise un compteur (ex: après connexion réussie)."""
    redis_client.delete(key)
