"""Accès aux données du domaine 'mentoring' via SQLAlchemy."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mentor import Mentor, MentorSession


def list_mentors(db: Session) -> list[Mentor]:
    return list(db.execute(select(Mentor)).scalars().all())


def get_mentor(db: Session, mentor_id: uuid.UUID) -> Mentor | None:
    return db.get(Mentor, mentor_id)


def get_mentor_by_user(db: Session, user_id: uuid.UUID) -> Mentor | None:
    stmt = select(Mentor).where(Mentor.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def create_mentor(db: Session, mentor: Mentor) -> Mentor:
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor


def create_session(db: Session, session: MentorSession) -> MentorSession:
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: uuid.UUID) -> MentorSession | None:
    return db.get(MentorSession, session_id)


def update_session(db: Session, session: MentorSession, fields: dict) -> MentorSession:
    for key, value in fields.items():
        setattr(session, key, value)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session: MentorSession) -> None:
    db.delete(session)
    db.commit()


def list_queue_for_mentor(db: Session, mentor_id: uuid.UUID) -> list[MentorSession]:
    stmt = select(MentorSession).where(MentorSession.mentor_id == mentor_id, MentorSession.status == "pending")
    return list(db.execute(stmt).scalars().all())


def list_for_student(db: Session, student_id: uuid.UUID) -> list[MentorSession]:
    stmt = select(MentorSession).where(MentorSession.student_id == student_id)
    return list(db.execute(stmt).scalars().all())
