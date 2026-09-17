"""Schémas Pydantic pour le domaine 'lessons'."""
import uuid

from pydantic import BaseModel, Field


class LessonCreate(BaseModel):
    module_id: uuid.UUID
    title: str = Field(min_length=3, max_length=200)
    content: str | None = None
    video: str | None = None
    duration_minutes: int = Field(default=0, ge=0)
    order: int = Field(default=0, ge=0)
    published: bool = False


class LessonUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    content: str | None = None
    video: str | None = None
    duration_minutes: int | None = Field(default=None, ge=0)
    order: int | None = Field(default=None, ge=0)
    published: bool | None = None


class LessonListOut(BaseModel):
    """Vue allégée (catalogue), sans le contenu complet."""
    id: uuid.UUID
    module_id: uuid.UUID
    title: str
    duration_minutes: int
    order: int
    published: bool

    model_config = {"from_attributes": True}


class LessonDetailOut(LessonListOut):
    """Vue complète, avec le contenu (10 000+ mots potentiellement)."""
    content: str | None = None
    video: str | None = None


class ProgressUpdate(BaseModel):
    progress: int = Field(ge=0, le=100)
    time_spent_seconds: int = Field(default=0, ge=0)
    completed: bool | None = None
