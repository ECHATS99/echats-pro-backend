"""Accès aux données du domaine 'lessons'."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.progress import UserProgress


def get_by_id(db: Session, lesson_id: uuid.UUID) -> Lesson | None:
    return db.get(Lesson, lesson_id)


def list_by_module(db: Session, module_id: uuid.UUID) -> list[Lesson]:
    stmt = select(Lesson).where(Lesson.module_id == module_id).order_by(Lesson.order)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, lesson: Lesson) -> Lesson:
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def update(db: Session, lesson: Lesson, fields: dict) -> Lesson:
    for key, value in fields.items():
        setattr(lesson, key, value)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


def delete(db: Session, lesson: Lesson) -> None:
    db.delete(lesson)
    db.commit()


def get_progress(db: Session, user_id: uuid.UUID, lesson_id: uuid.UUID) -> UserProgress | None:
    stmt = select(UserProgress).where(UserProgress.user_id == user_id, UserProgress.lesson_id == lesson_id)
    return db.execute(stmt).scalar_one_or_none()


def upsert_progress(db: Session, user_id: uuid.UUID, lesson_id: uuid.UUID, fields: dict) -> UserProgress:
    progress = get_progress(db, user_id, lesson_id)
    if progress is None:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id, **fields)
    else:
        for key, value in fields.items():
            setattr(progress, key, value)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress
