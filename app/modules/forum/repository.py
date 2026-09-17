"""Accès aux données du domaine 'forum' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.forum import ForumLike, ForumPost, ForumReport, ForumTopic


def get_topic(db: Session, topic_id: uuid.UUID) -> ForumTopic | None:
    return db.get(ForumTopic, topic_id)


def list_topics(db: Session, page: int, limit: int, category: str | None = None) -> tuple[list[ForumTopic], int]:
    filters = []
    if category:
        filters.append(ForumTopic.category == category)
    total = db.execute(select(func.count()).select_from(ForumTopic).where(*filters)).scalar_one()
    stmt = select(ForumTopic).where(*filters).order_by(ForumTopic.pinned.desc(), ForumTopic.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def create_topic(db: Session, topic: ForumTopic) -> ForumTopic:
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def update_topic(db: Session, topic: ForumTopic, fields: dict) -> ForumTopic:
    for key, value in fields.items():
        setattr(topic, key, value)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic: ForumTopic) -> None:
    db.delete(topic)
    db.commit()


def list_posts(db: Session, topic_id: uuid.UUID) -> list[ForumPost]:
    stmt = select(ForumPost).options(selectinload(ForumPost.likes)).where(ForumPost.topic_id == topic_id).order_by(ForumPost.created_at)
    return list(db.execute(stmt).scalars().all())


def create_post(db: Session, post: ForumPost) -> ForumPost:
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: uuid.UUID) -> ForumPost | None:
    return db.get(ForumPost, post_id)


def toggle_like(db: Session, post_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    stmt = select(ForumLike).where(ForumLike.post_id == post_id, ForumLike.user_id == user_id)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        db.delete(existing)
        db.commit()
        return False
    db.add(ForumLike(post_id=post_id, user_id=user_id))
    db.commit()
    return True


def create_report(db: Session, report: ForumReport) -> ForumReport:
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def list_unresolved_reports(db: Session) -> list[ForumReport]:
    stmt = select(ForumReport).where(ForumReport.resolved.is_(False))
    return list(db.execute(stmt).scalars().all())
