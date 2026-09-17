"""Schémas Pydantic pour le domaine 'paraben'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ParabenCourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    domain: str = Field(pattern="^(mobile|computer|cloud)$")
    level: str = "niveau_1"
    description: str | None = None
    video_url: str | None = None
    pdf_url: str | None = None
    e3_required: bool = False
    language: str = "fr"
    published: bool = False


class ParabenCourseOut(BaseModel):
    id: uuid.UUID
    title: str
    domain: str
    level: str
    description: str | None = None
    video_url: str | None = None
    pdf_url: str | None = None
    e3_required: bool
    language: str
    published: bool

    model_config = {"from_attributes": True}


class ParabenProgressUpdate(BaseModel):
    progress_pct: int = Field(ge=0, le=100)
    completed: bool | None = None


class ParabenProgressOut(BaseModel):
    course_id: uuid.UUID
    progress_pct: int
    completed: bool
    trial_start: datetime | None = None
    trial_end: datetime | None = None

    model_config = {"from_attributes": True}


class ParabenRevenueReport(BaseModel):
    period: str
    total_amount: int
    echats_share: int
    paraben_share: int
    subscriptions_count: int
