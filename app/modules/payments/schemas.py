"""Schémas Pydantic pour le domaine 'payments'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class PaymentOut(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID | None = None
    subscription_id: uuid.UUID | None = None
    user_id: uuid.UUID
    provider: str
    transaction_id: str | None = None
    status: str
    currency: str
    amount: int
    created_at: datetime

    model_config = {"from_attributes": True}


class RefundRequest(BaseModel):
    amount: int | None = None
    reason: str | None = None
