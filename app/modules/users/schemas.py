"""Schémas Pydantic (validation entrée/sortie) pour le domaine 'users'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserProfileOut(BaseModel):
    id: uuid.UUID
    email: str
    username: str
    avatar_url: str | None = None
    country: str | None = None
    city: str | None = None
    language: str
    timezone: str
    bio: str | None = None
    xp: int
    level: int
    streak: int
    role: str
    plan: str
    institution_id: uuid.UUID | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileUpdate(BaseModel):
    """Champs modifiables par l'utilisateur lui-même (jamais xp/level/role/plan)."""
    username: str | None = Field(default=None, min_length=3, max_length=50)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    city: str | None = Field(default=None, max_length=100)
    language: str | None = Field(default=None, max_length=5)
    timezone: str | None = Field(default=None, max_length=50)
    bio: str | None = Field(default=None, max_length=1000)


class TwoFactorSetupOut(BaseModel):
    """Secret + QR provisioning URI à afficher une seule fois lors de l'activation du 2FA
    (Partie 4.12 du SRS). Le secret n'est jamais renvoyé une seconde fois après activation."""
    secret: str
    provisioning_uri: str


class TwoFactorEnableRequest(BaseModel):
    totp_code: str = Field(min_length=6, max_length=6)


class TwoFactorStatusOut(BaseModel):
    enabled: bool


class UserStatisticsOut(BaseModel):
    xp: int
    level: int
    streak: int
    exercises_solved: int
    ctf_solved: int
    certificates_count: int
    badges_count: int


class UserSearchResultOut(BaseModel):
    id: uuid.UUID
    username: str
    avatar_url: str | None = None
    level: int
    country: str | None = None

    model_config = {"from_attributes": True}
