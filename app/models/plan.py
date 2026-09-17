"""Table plans : nom, prix, devise, durée, features, quotas."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Numeric, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # GO / CORE_I / PARABEN_NIVEAU_1 / CHAMBRE_CLOSE
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    currency: Mapped[str] = mapped_column(String(3), default="XAF")
    duration_days: Mapped[int | None] = mapped_column(Integer)  # null = illimité (ex: GO)
    features: Mapped[dict] = mapped_column(JSON, default=dict)
    max_ai_requests_per_day: Mapped[int] = mapped_column(Integer, default=10)
    max_storage_mb: Mapped[int] = mapped_column(Integer, default=100)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    subscriptions = relationship("Subscription", back_populates="plan")
