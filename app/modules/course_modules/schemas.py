"""Schémas Pydantic pour le domaine 'modules' (contenu pédagogique)."""
import uuid

from pydantic import BaseModel, Field


class CourseModuleCreate(BaseModel):
    track_id: uuid.UUID
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    order: int = Field(default=0, ge=0)
    published: bool = False


class CourseModuleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    order: int | None = Field(default=None, ge=0)
    published: bool | None = None


class CourseModuleOut(BaseModel):
    id: uuid.UUID
    track_id: uuid.UUID
    title: str
    description: str | None = None
    order: int
    published: bool

    model_config = {"from_attributes": True}
