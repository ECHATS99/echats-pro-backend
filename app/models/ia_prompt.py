"""Table ia_prompts : prompts système modifiables depuis l'admin, sans redéploiement
(Partie 5 du SRS : GET/POST /api/v1/ia/{cyber,go,nexo})."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class IAPrompt(Base):
    __tablename__ = "ia_prompts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    context: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # cyber|go|nexo
    model: Mapped[str | None] = mapped_column(String(50))
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
