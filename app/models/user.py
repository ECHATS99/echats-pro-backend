"""Table users : firebase_uid, profil, xp, level, streak, institution_id.
Le rôle et le plan effectif de l'utilisateur sont TOUJOURS déterminés depuis cette table
et ses relations (roles, subscriptions) — jamais depuis les claims Firebase (Partie 3 du SRS).
"""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.role_permission import user_roles


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    avatar_url: Mapped[str | None] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(2))
    city: Mapped[str | None] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(String(5), default="fr")
    timezone: Mapped[str] = mapped_column(String(50), default="Africa/Brazzaville")
    bio: Mapped[str | None] = mapped_column(String(1000))

    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    streak: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[str] = mapped_column(String(30), default="active")  # active|suspended|banned|pending_verification

    # 2FA (Partie 4.12 du SRS) — secret chiffré, jamais en clair
    totp_secret_encrypted: Mapped[str | None] = mapped_column(String(500))
    totp_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    institution_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="SET NULL"))

    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_ip: Mapped[str | None] = mapped_column(String(45))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    institution = relationship("Institution", back_populates="users")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    subscriptions = relationship("Subscription", back_populates="user", order_by="desc(Subscription.created_at)")

    @property
    def primary_role_name(self) -> str:
        """Rôle principal : le plus privilégié parmi les rôles assignés (utilisé pour l'affichage)."""
        if not self.roles:
            return "student"
        priority = [
            "super_admin", "admin", "paraben_manager", "institution_manager",
            "instructor", "mentor", "premium", "student",
        ]
        role_names = {r.name for r in self.roles}
        for name in priority:
            if name in role_names:
                return name
        return next(iter(role_names))

    @property
    def is_active(self) -> bool:
        return self.status == "active" and self.deleted_at is None
