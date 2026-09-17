"""Schémas Pydantic pour le domaine 'mentoring'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class MentorOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    rating: float
    reviews_count: int

    model_config = {"from_attributes": True}


class MentorSessionRequest(BaseModel):
    mentor_id: uuid.UUID
    exercise_id: uuid.UUID | None = None
    meeting_date: datetime | None = None


class MentorSessionUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(pending|accepted|completed|cancelled)$")
    feedback: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    meeting_date: datetime | None = None


class MentorSessionOut(BaseModel):
    id: uuid.UUID
    mentor_id: uuid.UUID
    student_id: uuid.UUID
    exercise_id: uuid.UUID | None = None
    status: str
    feedback: str | None = None
    rating: int | None = None
    meeting_date: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
