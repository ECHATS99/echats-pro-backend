"""Schémas Pydantic pour le domaine 'news'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class NewsArticleOut(BaseModel):
    id: uuid.UUID
    title: str
    summary: str | None = None
    url: str
    image: str | None = None
    source: str
    category: str | None = None
    published_at: datetime | None = None

    model_config = {"from_attributes": True}
