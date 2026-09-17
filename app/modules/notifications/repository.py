"""Accès aux données du domaine 'notifications' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select, update as sa_update
from sqlalchemy.orm import Session

from app.models.notification import Notification


def list_for_user(db: Session, user_id: uuid.UUID, page: int, limit: int, unread_only: bool = False) -> tuple[list[Notification], int]:
    filters = [Notification.user_id == user_id]
    if unread_only:
        filters.append(Notification.read.is_(False))
    total = db.execute(select(func.count()).select_from(Notification).where(*filters)).scalar_one()
    stmt = select(Notification).where(*filters).order_by(Notification.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def get_by_id(db: Session, notification_id: uuid.UUID) -> Notification | None:
    return db.get(Notification, notification_id)


def create(db: Session, notification: Notification) -> Notification:
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def mark_read(db: Session, notification: Notification) -> Notification:
    notification.read = True
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def mark_all_read(db: Session, user_id: uuid.UUID) -> None:
    db.execute(sa_update(Notification).where(Notification.user_id == user_id, Notification.read.is_(False)).values(read=True))
    db.commit()


def delete(db: Session, notification: Notification) -> None:
    db.delete(notification)
    db.commit()


def unread_count(db: Session, user_id: uuid.UUID) -> int:
    stmt = select(func.count()).select_from(Notification).where(Notification.user_id == user_id, Notification.read.is_(False))
    return db.execute(stmt).scalar_one()
