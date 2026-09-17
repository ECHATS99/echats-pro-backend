"""Schémas Pydantic pour le domaine 'badges'."""
import uuid

from pydantic import BaseModel, Field


class BadgeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    icon: str | None = None
    condition_type: str | None = Field(default=None, pattern="^(xp|ctf_solves|streak|track_completed)$")
    condition_value: int = Field(default=0, ge=0)
    xp_reward: int = Field(default=0, ge=0)


class BadgeOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    icon: str | None = None
    condition_type: str | None = None
    condition_value: int
    xp_reward: int

    model_config = {"from_attributes": True}


class UserBadgeOut(BaseModel):
    badge: BadgeOut
    earned_at: str

    model_config = {"from_attributes": True}
