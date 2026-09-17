"""Accès aux données du domaine 'writeups' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.writeup import Writeup, WriteupVote


def get_by_id(db: Session, writeup_id: uuid.UUID) -> Writeup | None:
    return db.get(Writeup, writeup_id)


def list_published(db: Session, page: int, limit: int, ctf_id: uuid.UUID | None = None) -> tuple[list[Writeup], int]:
    filters = [Writeup.published.is_(True)]
    if ctf_id:
        filters.append(Writeup.ctf_id == ctf_id)
    total = db.execute(select(func.count()).select_from(Writeup).where(*filters)).scalar_one()
    stmt = select(Writeup).where(*filters).order_by(Writeup.votes.desc(), Writeup.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def create(db: Session, writeup: Writeup) -> Writeup:
    db.add(writeup)
    db.commit()
    db.refresh(writeup)
    return writeup


def update(db: Session, writeup: Writeup, fields: dict) -> Writeup:
    for key, value in fields.items():
        setattr(writeup, key, value)
    db.add(writeup)
    db.commit()
    db.refresh(writeup)
    return writeup


def delete(db: Session, writeup: Writeup) -> None:
    db.delete(writeup)
    db.commit()


def get_vote(db: Session, writeup_id: uuid.UUID, user_id: uuid.UUID) -> WriteupVote | None:
    stmt = select(WriteupVote).where(WriteupVote.writeup_id == writeup_id, WriteupVote.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def upsert_vote(db: Session, writeup: Writeup, user_id: uuid.UUID, value: int) -> Writeup:
    existing = get_vote(db, writeup.id, user_id)
    if existing is None:
        db.add(WriteupVote(writeup_id=writeup.id, user_id=user_id, value=value))
        writeup.votes += value
    else:
        writeup.votes += value - existing.value
        existing.value = value
        db.add(existing)
    db.add(writeup)
    db.commit()
    db.refresh(writeup)
    return writeup
