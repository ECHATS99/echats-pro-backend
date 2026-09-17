"""Schémas Pydantic pour le domaine 'tracks'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TrackCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    difficulty: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    domain: str | None = None
    duration_minutes: int = Field(default=0, ge=0)
    cover_image: str | None = None
    published: bool = False


class TrackUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    difficulty: str | None = Field(default=None, pattern="^(beginner|intermediate|advanced)$")
    domain: str | None = None
    duration_minutes: int | None = Field(default=None, ge=0)
    cover_image: str | None = None
    published: bool | None = None


class TrackOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    description: str | None = None
    difficulty: str
    domain: str | None = None
    duration_minutes: int
    cover_image: str | None = None
    published: bool
    created_at: datetime

    model_config = {"from_attributes": True}
