"""Schémas Pydantic pour le domaine 'media'."""
from pydantic import BaseModel


class MediaUploadOut(BaseModel):
    url: str
    public_id: str
    bytes: int | None = None
    format: str | None = None
