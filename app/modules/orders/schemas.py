"""Schémas Pydantic pour le domaine 'orders'."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(default=1, ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)
    payment_provider: str = Field(pattern="^(stripe|paypal|mtn|airtel|wave)$")
    currency: str = "XAF"
    phone_number: str | None = Field(default=None, description="Requis pour Mobile Money.")


class OrderItemOut(BaseModel):
    product_id: uuid.UUID
    quantity: int
    unit_price: int

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    amount: int
    currency: str
    payment_provider: str | None = None
    created_at: datetime
    items: list[OrderItemOut] = []

    model_config = {"from_attributes": True}


class OrderPaymentIntentOut(BaseModel):
    order: OrderOut
    client_secret: str | None = None
    approval_url: str | None = None
    transaction_id: str | None = None
