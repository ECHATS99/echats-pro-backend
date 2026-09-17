"""Schémas Pydantic pour le domaine 'organizations' (institutions / Chambre Close)."""
import uuid

from pydantic import BaseModel, Field


class InstitutionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    type: str | None = Field(default=None, pattern="^(school|university|company|agency|ministry)$")
    contact_email: str | None = None
    max_users: int = Field(default=50, ge=1)
    paraben_access: bool = False


class InstitutionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    contact_email: str | None = None
    max_users: int | None = Field(default=None, ge=1)
    paraben_access: bool | None = None
    chamber_close_enabled: bool | None = None
    active: bool | None = None


class InstitutionOut(BaseModel):
    id: uuid.UUID
    name: str
    country: str | None = None
    type: str | None = None
    contact_email: str | None = None
    max_users: int
    paraben_access: bool
    chamber_close_enabled: bool
    active: bool

    model_config = {"from_attributes": True}


class InstitutionMemberOut(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    role: str

    model_config = {"from_attributes": True}
