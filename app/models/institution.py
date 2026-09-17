"""Table institutions : nom, pays, type, licences."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str | None] = mapped_column(String(2))
    type: Mapped[str | None] = mapped_column(String(50))  # school | university | company | agency | ministry
    contact_email: Mapped[str | None] = mapped_column(String(255))
    max_users: Mapped[int] = mapped_column(Integer, default=50)
    paraben_access: Mapped[bool] = mapped_column(Boolean, default=False)
    chamber_close_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    users = relationship("User", back_populates="institution")
