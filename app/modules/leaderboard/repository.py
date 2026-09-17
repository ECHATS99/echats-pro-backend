"""Accès aux données du domaine 'leaderboard' via SQLAlchemy."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def top_users(db: Session, limit: int = 50, country: str | None = None) -> list[User]:
    stmt = select(User).where(User.status == "active")
    if country:
        stmt = stmt.where(User.country == country)
    stmt = stmt.order_by(User.xp.desc()).limit(limit)
    return list(db.execute(stmt).scalars().all())


def user_rank(db: Session, user_id: uuid.UUID) -> int | None:
    user = db.get(User, user_id)
    if user is None:
        return None
    stmt = select(User).where(User.xp > user.xp, User.status == "active")
    higher_count = len(db.execute(stmt).scalars().all())
    return higher_count + 1
