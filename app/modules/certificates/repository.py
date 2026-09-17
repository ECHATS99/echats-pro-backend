"""Accès aux données du domaine 'certificates' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.certificate import Certificate


def get_by_user_and_track(db: Session, user_id: uuid.UUID, track_id: uuid.UUID) -> Certificate | None:
    stmt = select(Certificate).where(Certificate.user_id == user_id, Certificate.track_id == track_id)
    return db.execute(stmt).scalar_one_or_none()


def get_by_verification_code(db: Session, code: str) -> Certificate | None:
    stmt = select(Certificate).where(Certificate.verification_code == code)
    return db.execute(stmt).scalar_one_or_none()


def list_for_user(db: Session, user_id: uuid.UUID) -> list[Certificate]:
    stmt = select(Certificate).where(Certificate.user_id == user_id).order_by(Certificate.issued_at.desc())
    return list(db.execute(stmt).scalars().all())


def create(db: Session, certificate: Certificate) -> Certificate:
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate
