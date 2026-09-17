"""Schémas Pydantic pour le domaine 'writeups'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class WriteupCreate(BaseModel):
    ctf_id: uuid.UUID | None = None
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)
    published: bool = True


class WriteupUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    content: str | None = None
    published: bool | None = None


class WriteupOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ctf_id: uuid.UUID | None = None
    title: str
    content: str
    published: bool
    votes: int
    created_at: datetime

    model_config = {"from_attributes": True}


class VoteRequest(BaseModel):
    value: int = Field(ge=-1, le=1)
