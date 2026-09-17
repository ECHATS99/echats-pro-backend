"""Tables ctf_events, ctf_categories, ctf_challenges, ctf_solves."""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Text, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


class CTFEvent(Base):
    __tablename__ = "ctf_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="upcoming")  # upcoming|active|ended

    challenges = relationship("CTFChallenge", back_populates="event", cascade="all, delete-orphan")


class CTFCategory(Base):
    __tablename__ = "ctf_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    challenges = relationship("CTFChallenge", back_populates="category")


class CTFChallenge(Base):
    __tablename__ = "ctf_challenges"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ctf_categories.id", ondelete="SET NULL"))
    event_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ctf_events.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(20), default="easy")
    points: Mapped[int] = mapped_column(Integer, default=50)
    docker_image: Mapped[str | None] = mapped_column(String(255))
    image_url: Mapped[str | None] = mapped_column(String(500))
    published: Mapped[bool] = mapped_column(default=False)

    flag_hash: Mapped[str | None] = mapped_column(String(255))
    flag_salt: Mapped[str | None] = mapped_column(String(64))
    terminal_commands: Mapped[list[dict[str, str]]] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    default_output: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category = relationship("CTFCategory", back_populates="challenges")
    event = relationship("CTFEvent", back_populates="challenges")
    solves = relationship("CTFSolve", back_populates="challenge", cascade="all, delete-orphan")


class CTFSolve(Base):
    __tablename__ = "ctf_solves"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ctf_challenges.id", ondelete="CASCADE"), nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    challenge = relationship("CTFChallenge", back_populates="solves")
