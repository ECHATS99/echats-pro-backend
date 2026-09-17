"""Schémas Pydantic pour le domaine 'classroom'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ClassroomCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    institution_id: uuid.UUID | None = None


class ClassroomOut(BaseModel):
    id: uuid.UUID
    institution_id: uuid.UUID | None = None
    teacher_id: uuid.UUID
    title: str
    access_code: str
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ClassroomJoin(BaseModel):
    access_code: str = Field(min_length=4, max_length=12)


class ClassroomMemberOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    role: str
    joined_at: datetime

    model_config = {"from_attributes": True}


class AssignmentCreate(BaseModel):
    content_type: str = Field(pattern="^(track|lesson|exercise|ctf)$")
    content_id: uuid.UUID
    deadline: datetime | None = None


class AssignmentOut(BaseModel):
    id: uuid.UUID
    classroom_id: uuid.UUID
    content_type: str
    content_id: uuid.UUID
    deadline: datetime | None = None

    model_config = {"from_attributes": True}
