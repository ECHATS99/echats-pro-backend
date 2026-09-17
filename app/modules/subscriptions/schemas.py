"""Schémas Pydantic pour le domaine 'subscriptions'."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class PlanOut(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    price: float
    currency: str
    duration_days: int | None = None
    features: dict
    max_ai_requests_per_day: int
    max_storage_mb: int

    model_config = {"from_attributes": True}


class SubscriptionCreate(BaseModel):
    plan_code: str
    payment_provider: str
    phone_number: str | None = None


class SubscriptionOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_id: uuid.UUID
    status: str
    payment_provider: str | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None
    renewal: bool

    model_config = {"from_attributes": True}


class SubscriptionPaymentIntentOut(BaseModel):
    subscription: SubscriptionOut
    client_secret: str | None = None
    approval_url: str | None = None
    transaction_id: str | None = None
