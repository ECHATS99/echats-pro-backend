"""Accès aux données du domaine 'badges'."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.badge import Badge, UserBadge


def list_all(db: Session) -> list[Badge]:
    return list(db.execute(select(Badge)).scalars().all())


def create(db: Session, badge: Badge) -> Badge:
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


def delete(db: Session, badge: Badge) -> None:
    db.delete(badge)
    db.commit()


def get_by_id(db: Session, badge_id: uuid.UUID) -> Badge | None:
    return db.get(Badge, badge_id)


def list_for_user(db: Session, user_id: uuid.UUID) -> list[UserBadge]:
    stmt = select(UserBadge).options(selectinload(UserBadge.badge)).where(UserBadge.user_id == user_id)
    return list(db.execute(stmt).scalars().all())
