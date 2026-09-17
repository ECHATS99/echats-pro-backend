"""Schémas Pydantic pour le domaine 'certificates'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class CertificateOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    track_id: uuid.UUID
    verification_code: str
    cloudinary_url: str | None = None
    issued_at: datetime

    model_config = {"from_attributes": True}


class CertificateVerifyOut(BaseModel):
    valid: bool
    track_title: str | None = None
    issued_at: datetime | None = None
    username: str | None = None
