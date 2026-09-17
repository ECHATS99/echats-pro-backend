"""Accès aux données du domaine 'exercises'."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.exercise import Exercise
from app.models.flag import Flag, Submission


def get_by_id(db: Session, exercise_id: uuid.UUID) -> Exercise | None:
    stmt = select(Exercise).options(selectinload(Exercise.flag)).where(Exercise.id == exercise_id)
    return db.execute(stmt).scalar_one_or_none()


def list_by_lesson(db: Session, lesson_id: uuid.UUID) -> list[Exercise]:
    stmt = select(Exercise).where(Exercise.lesson_id == lesson_id)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, exercise: Exercise) -> Exercise:
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def update(db: Session, exercise: Exercise, fields: dict) -> Exercise:
    for key, value in fields.items():
        setattr(exercise, key, value)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete(db: Session, exercise: Exercise) -> None:
    db.delete(exercise)
    db.commit()


def upsert_flag(db: Session, exercise_id: uuid.UUID, flag_hash: str, salt: str) -> Flag:
    stmt = select(Flag).where(Flag.exercise_id == exercise_id)
    flag = db.execute(stmt).scalar_one_or_none()
    if flag is None:
        flag = Flag(exercise_id=exercise_id, hash=flag_hash, salt=salt)
    else:
        flag.hash = flag_hash
        flag.salt = salt
    db.add(flag)
    db.commit()
    return flag


def get_user_submission_count(db: Session, exercise_id: uuid.UUID, user_id: uuid.UUID) -> int:
    stmt = select(Submission).where(Submission.exercise_id == exercise_id, Submission.user_id == user_id)
    return len(db.execute(stmt).scalars().all())


def get_or_create_submission(db: Session, exercise_id: uuid.UUID, user_id: uuid.UUID) -> Submission:
    stmt = select(Submission).where(Submission.exercise_id == exercise_id, Submission.user_id == user_id)
    submission = db.execute(stmt).scalar_one_or_none()
    if submission is None:
        submission = Submission(exercise_id=exercise_id, user_id=user_id)
        db.add(submission)
        db.commit()
        db.refresh(submission)
    return submission


def save_submission(db: Session, submission: Submission) -> Submission:
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
