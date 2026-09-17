"""Accès aux données du domaine 'paraben' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.paraben import ParabenCourse, ParabenProgress, ParabenRevenue

TRIAL_DURATION_DAYS = 30  # essai E3 30 jours (Partie 8 du SRS)


def list_courses(db: Session, domain: str | None = None, published_only: bool = True) -> list[ParabenCourse]:
    filters = []
    if published_only:
        filters.append(ParabenCourse.published.is_(True))
    if domain:
        filters.append(ParabenCourse.domain == domain)
    return list(db.execute(select(ParabenCourse).where(*filters)).scalars().all())


def get_course(db: Session, course_id: uuid.UUID) -> ParabenCourse | None:
    return db.get(ParabenCourse, course_id)


def create_course(db: Session, course: ParabenCourse) -> ParabenCourse:
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_progress(db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> ParabenProgress | None:
    stmt = select(ParabenProgress).where(ParabenProgress.user_id == user_id, ParabenProgress.course_id == course_id)
    return db.execute(stmt).scalar_one_or_none()


def upsert_progress(db: Session, user_id: uuid.UUID, course_id: uuid.UUID, fields: dict) -> ParabenProgress:
    progress = get_progress(db, user_id, course_id)
    if progress is None:
        now = datetime.now(timezone.utc)
        progress = ParabenProgress(
            user_id=user_id, course_id=course_id, trial_start=now,
            trial_end=now + timedelta(days=TRIAL_DURATION_DAYS), **fields,
        )
    else:
        for key, value in fields.items():
            setattr(progress, key, value)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def revenue_report(db: Session, period: str) -> dict:
    stmt = select(
        func.coalesce(func.sum(ParabenRevenue.amount), 0),
        func.coalesce(func.sum(ParabenRevenue.echats_share), 0),
        func.coalesce(func.sum(ParabenRevenue.paraben_share), 0),
        func.count(ParabenRevenue.id),
    ).where(ParabenRevenue.period == period)
    total, echats_share, paraben_share, count = db.execute(stmt).one()
    return {"total_amount": total, "echats_share": echats_share, "paraben_share": paraben_share, "subscriptions_count": count}
