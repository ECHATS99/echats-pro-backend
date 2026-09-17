"""Schémas Pydantic pour le domaine 'audit'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None = None
    role: str | None = None
    action: str
    module: str | None = None
    resource: str | None = None
    resource_id: str | None = None
    ip_address: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
