"""Schémas Pydantic pour le domaine 'notifications'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: uuid.UUID
    type: str
    title: str
    message: str
    read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationBroadcast(BaseModel):
    """Utilisé par l'admin pour diffuser une notification à un ou plusieurs utilisateurs."""
    user_ids: list[uuid.UUID] | None = None  # None = tous les utilisateurs
    type: str
    title: str
    message: str
