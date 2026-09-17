"""Accès aux données du domaine 'modules'."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course_module import CourseModule


def get_by_id(db: Session, module_id: uuid.UUID) -> CourseModule | None:
    return db.get(CourseModule, module_id)


def list_by_track(db: Session, track_id: uuid.UUID) -> list[CourseModule]:
    stmt = select(CourseModule).where(CourseModule.track_id == track_id).order_by(CourseModule.order)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, module: CourseModule) -> CourseModule:
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def update(db: Session, module: CourseModule, fields: dict) -> CourseModule:
    for key, value in fields.items():
        setattr(module, key, value)
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def delete(db: Session, module: CourseModule) -> None:
    db.delete(module)
    db.commit()
