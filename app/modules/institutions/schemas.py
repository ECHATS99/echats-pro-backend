"""Schemas Pydantic pour le domaine institutions (Chambre Close)."""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class InstitutionCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    code: str = Field(min_length=3, max_length=30)
    slug: str | None = None
    tagline: str | None = None
    description: str | None = None
    type: str = "ACADEMIC"
    is_private: bool = False
    requires_key: bool = False
    accent_color: str = "#CCFF00"
    logo: str | None = None
    cover_image: str | None = None


class InstitutionUpdate(BaseModel):
    name: str | None = None
    tagline: str | None = None
    description: str | None = None
    is_private: bool | None = None
    requires_key: bool | None = None
    accent_color: str | None = None


class InstitutionOut(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    slug: str | None = None
    prefix: str | None = None
    tagline: str | None = None
    description: str | None = None
    type: str
    logo: str | None = None
    cover_image: str | None = None
    owner_uid: str | None = None
    owner_name: str | None = None
    is_private: bool
    requires_key: bool
    accent_color: str
    members_count: int = 0
    visitors_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class AccessKeyCreate(BaseModel):
    assigned_role: str = Field(pattern="^(ELEVE|FORMATEUR)$")
    max_uses: int = Field(default=20, ge=1, le=1000)
    days_valid: int = Field(default=30, ge=1, le=365)


class AccessKeyOut(BaseModel):
    id: uuid.UUID
    key: str
    institution_id: uuid.UUID
    assigned_role: str
    max_uses: int
    current_uses: int
    expires_at: datetime | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class JoinWithKeyRequest(BaseModel):
    key: str = Field(min_length=4, max_length=32)


class JoinResult(BaseModel):
    success: bool
    institution_id: uuid.UUID | None = None
    institution_name: str | None = None
    role: str | None = None
    message: str
