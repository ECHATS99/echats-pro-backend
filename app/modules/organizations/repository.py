"""Accès aux données du domaine 'organizations' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.institution import Institution
from app.models.user import User


def get_by_id(db: Session, institution_id: uuid.UUID) -> Institution | None:
    stmt = select(Institution).where(Institution.id == institution_id, Institution.deleted_at.is_(None))
    return db.execute(stmt).scalar_one_or_none()


def list_all(db: Session, page: int, limit: int) -> tuple[list[Institution], int]:
    total = db.execute(select(func.count()).select_from(Institution).where(Institution.deleted_at.is_(None))).scalar_one()
    stmt = select(Institution).where(Institution.deleted_at.is_(None)).order_by(Institution.name).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def create(db: Session, institution: Institution) -> Institution:
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return institution


def update(db: Session, institution: Institution, fields: dict) -> Institution:
    for key, value in fields.items():
        setattr(institution, key, value)
    db.add(institution)
    db.commit()
    db.refresh(institution)
    return institution


def count_members(db: Session, institution_id: uuid.UUID) -> int:
    stmt = select(func.count()).select_from(User).where(User.institution_id == institution_id)
    return db.execute(stmt).scalar_one()


def list_members(db: Session, institution_id: uuid.UUID) -> list[User]:
    stmt = select(User).where(User.institution_id == institution_id)
    return list(db.execute(stmt).scalars().all())
