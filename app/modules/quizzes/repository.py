"""Accès aux données du domaine 'quizzes'."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.quiz import Answer, Question, Quiz


def get_by_id(db: Session, quiz_id: uuid.UUID) -> Quiz | None:
    stmt = (
        select(Quiz)
        .options(selectinload(Quiz.questions).selectinload(Question.answers))
        .where(Quiz.id == quiz_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_by_lesson(db: Session, lesson_id: uuid.UUID) -> Quiz | None:
    stmt = (
        select(Quiz)
        .options(selectinload(Quiz.questions).selectinload(Question.answers))
        .where(Quiz.lesson_id == lesson_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def create(db: Session, quiz: Quiz) -> Quiz:
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


def delete(db: Session, quiz: Quiz) -> None:
    db.delete(quiz)
    db.commit()
