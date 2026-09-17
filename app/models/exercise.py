"""Table exercises : lien lesson, difficulté, points, type, image docker."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(20), default="easy")  # easy|medium|hard|insane
    points: Mapped[int] = mapped_column(Integer, default=10)
    type: Mapped[str] = mapped_column(String(30), default="code")  # code|quiz|lab
    docker_image: Mapped[str | None] = mapped_column(String(255))
    judge0_language: Mapped[str | None] = mapped_column(String(50))
    hints: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lesson = relationship("Lesson", back_populates="exercises")
    flag = relationship("Flag", back_populates="exercise", uselist=False, cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="exercise", cascade="all, delete-orphan")
