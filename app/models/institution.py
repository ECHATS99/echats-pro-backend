"""Table institutions : Chambre Close (écoles, universités, partenaires)."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identité
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str | None] = mapped_column(String(30), unique=True, index=True)
    slug: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    prefix: Mapped[str | None] = mapped_column(String(10))  # PRBN, ECHT, etc.

    # Présentation
    tagline: Mapped[str | None] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str | None] = mapped_column(String(50))  # ACADEMIC | PARABEN_CORP | COMPANY...
    logo: Mapped[str | None] = mapped_column(String(500))
    cover_image: Mapped[str | None] = mapped_column(String(500))
    accent_color: Mapped[str] = mapped_column(String(20), default="#CCFF00")

    # Localisation / contact
    country: Mapped[str | None] = mapped_column(String(2))
    contact_email: Mapped[str | None] = mapped_column(String(255))

    # Propriété
    owner_uid: Mapped[str | None] = mapped_column(String(100), index=True)
    owner_name: Mapped[str | None] = mapped_column(String(200))

    # Accès & permissions
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    requires_key: Mapped[bool] = mapped_column(Boolean, default=False)
    paraben_access: Mapped[bool] = mapped_column(Boolean, default=False)
    chamber_close_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # Limites
    max_users: Mapped[int] = mapped_column(Integer, default=50)

    # Compteurs (dénormalisés pour perf)
    members_count: Mapped[int] = mapped_column(Integer, default=0)
    visitors_count: Mapped[int] = mapped_column(Integer, default=0)

    # Statut
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Audit
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    users = relationship("User", back_populates="institution")
