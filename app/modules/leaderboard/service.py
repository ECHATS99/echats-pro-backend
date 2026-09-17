"""Logique métier du domaine 'leaderboard'. Classement global basé sur l'XP cumulé,
mis en cache Redis (Partie 7.4 du SRS) car interrogé très fréquemment."""
import uuid

from app.modules.leaderboard import repository as leaderboard_repo
from app.modules.leaderboard.schemas import LeaderboardEntry
from app.services.cache_service import cache_get, cache_set

CACHE_KEY = "leaderboard:global"
CACHE_TTL_SECONDS = 30


def get_leaderboard(db, limit: int = 50, country: str | None = None) -> list[LeaderboardEntry]:
    cache_key = f"{CACHE_KEY}:{country or 'all'}:{limit}"
    cached = cache_get(cache_key)
    if cached is not None:
        return [LeaderboardEntry(**e) for e in cached]

    users = leaderboard_repo.top_users(db, limit, country)
    entries = [
        LeaderboardEntry(rank=i + 1, user_id=u.id, username=u.username, avatar=u.avatar_url, xp=u.xp, level=u.level, country=u.country)
        for i, u in enumerate(users)
    ]
    cache_set(cache_key, [e.model_dump() for e in entries], CACHE_TTL_SECONDS)
    return entries


def get_my_rank(db, user_id: uuid.UUID) -> dict:
    rank = leaderboard_repo.user_rank(db, user_id)
    return {"rank": rank}
