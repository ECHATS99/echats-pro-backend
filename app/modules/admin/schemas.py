"""Schémas Pydantic pour le domaine 'admin'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AdminSettingUpdate(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    value: str


class AdminSettingOut(BaseModel):
    key: str
    value: str | None = None

    model_config = {"from_attributes": True}


class FeatureFlagUpdate(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    enabled: bool
    description: str | None = None


class FeatureFlagOut(BaseModel):
    key: str
    enabled: bool
    description: str | None = None

    model_config = {"from_attributes": True}


class SystemMessageCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1)
    level: str = Field(default="info", pattern="^(info|warning|critical)$")


class SystemMessageOut(BaseModel):
    id: uuid.UUID
    title: str
    message: str
    level: str
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MaintenanceUpdate(BaseModel):
    active: bool
    message: str | None = None
