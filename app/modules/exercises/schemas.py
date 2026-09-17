"""Schémas Pydantic pour le domaine 'exercises'."""
import uuid

from pydantic import BaseModel, Field


class ExerciseCreate(BaseModel):
    lesson_id: uuid.UUID | None = None
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    difficulty: str = Field(default="easy", pattern="^(easy|medium|hard|insane)$")
    points: int = Field(default=10, ge=0)
    type: str = Field(default="code", pattern="^(code|quiz|lab)$")
    docker_image: str | None = None
    judge0_language: str | None = None
    hints: str | None = None
    flag: str | None = Field(default=None, description="Flag en clair, transmis une seule fois à la création (jamais restocké en clair).")


class ExerciseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    difficulty: str | None = Field(default=None, pattern="^(easy|medium|hard|insane)$")
    points: int | None = Field(default=None, ge=0)
    hints: str | None = None
    flag: str | None = None


class ExerciseOut(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    difficulty: str
    points: int
    type: str
    judge0_language: str | None = None
    hints: str | None = None
    has_flag: bool = False

    model_config = {"from_attributes": True}


class CodeSubmission(BaseModel):
    source_code: str = Field(min_length=1, max_length=20000)
    stdin: str = ""


class FlagSubmission(BaseModel):
    flag: str = Field(min_length=1, max_length=500)


class SubmissionResult(BaseModel):
    correct: bool
    score: int
    attempts: int
    stdout: str | None = None
    stderr: str | None = None
    message: str
