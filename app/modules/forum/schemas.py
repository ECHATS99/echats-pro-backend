"""Schémas Pydantic pour le domaine 'forum'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TopicCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=3)
    category: str | None = None
    related_type: str | None = Field(default=None, pattern="^(exercise|module|general)$")
    related_id: uuid.UUID | None = None


class TopicOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content: str
    category: str | None = None
    pinned: bool
    locked: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    content: str = Field(min_length=1)


class PostOut(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    likes_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportCreate(BaseModel):
    post_id: uuid.UUID | None = None
    topic_id: uuid.UUID | None = None
    reason: str = Field(min_length=3, max_length=255)
