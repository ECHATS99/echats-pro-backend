"""Schémas Pydantic pour le domaine 'leaderboard'."""
import uuid

from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: uuid.UUID
    username: str
    avatar: str | None = None
    xp: int
    level: int
    country: str | None = None
