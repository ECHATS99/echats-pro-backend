"""Schémas Pydantic pour le domaine 'ctf'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TerminalCommand(BaseModel):
    command: str = Field(min_length=1, max_length=500)
    output: str = Field(default="", max_length=10_000)


class CTFEventOut(BaseModel):
    id: uuid.UUID
    title: str
    start: datetime | None = None
    end: datetime | None = None
    status: str

    model_config = {"from_attributes": True}


class CTFCategoryOut(BaseModel):
    id: uuid.UUID
    name: str

    model_config = {"from_attributes": True}


class CTFChallengeCreate(BaseModel):
    category_id: uuid.UUID | None = None
    event_id: uuid.UUID | None = None
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    difficulty: str = Field(default="easy", pattern="^(easy|medium|hard|insane)$")
    points: int = Field(default=50, ge=0)
    docker_image: str | None = None
    image_url: str | None = None
    published: bool = False
    flag: str = Field(min_length=1, max_length=500)
    terminal_commands: list[TerminalCommand] = Field(default_factory=list, max_length=100)
    default_output: str | None = Field(default=None, max_length=10_000)


class CTFChallengeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    difficulty: str | None = Field(default=None, pattern="^(easy|medium|hard|insane)$")
    points: int | None = Field(default=None, ge=0)
    published: bool | None = None
    flag: str | None = None
    terminal_commands: list[TerminalCommand] | None = Field(default=None, max_length=100)
    default_output: str | None = Field(default=None, max_length=10_000)


class CTFChallengeOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    event_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    difficulty: str
    points: int
    image_url: str | None = None
    published: bool
    solved_by_me: bool = False
    terminal_commands: list[TerminalCommand] = Field(default_factory=list)
    default_output: str | None = None

    model_config = {"from_attributes": True}


class CTFFlagSubmission(BaseModel):
    flag: str = Field(min_length=1, max_length=500)


class CTFSubmitResult(BaseModel):
    correct: bool
    points: int
    message: str


class CTFLeaderboardEntry(BaseModel):
    user_id: uuid.UUID
    username: str
    total_points: int
    solves_count: int
