"""Schémas Pydantic (validation entrée/sortie) pour le domaine 'auth'."""
import uuid

from pydantic import BaseModel, EmailStr, Field


class FirebaseLoginRequest(BaseModel):
    """Corps de POST /api/v1/auth/login : le frontend envoie le ID token Firebase."""
    id_token: str = Field(..., min_length=10)


class TwoFactorVerifyRequest(BaseModel):
    id_token: str
    totp_code: str = Field(..., min_length=6, max_length=6)


class RefreshRequest(BaseModel):
    refresh_token: str


class UserPublicOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    role: str
    plan: str
    avatar_url: str | None = None
    xp: int
    level: int

    model_config = {"from_attributes": True}


class AuthTokensOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublicOut


class TwoFactorRequiredOut(BaseModel):
    two_factor_required: bool = True
    message: str = "Code TOTP requis pour ce rôle."
