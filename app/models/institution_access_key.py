"""Table institution_access_keys — clés d'accès à la Chambre Close."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class InstitutionAccessKey(Base):
    __tablename__ = "institution_access_keys"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    assigned_role: Mapped[str] = mapped_column(String(50), nullable=False, default="ELEVE")
    max_uses: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    current_uses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
