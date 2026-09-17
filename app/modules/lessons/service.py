"""Logique métier du domaine 'lessons'."""
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.lesson import Lesson
from app.modules.course_modules import repository as modules_repo
from app.modules.lessons import repository as lessons_repo
from app.modules.lessons.schemas import LessonCreate, LessonDetailOut, LessonListOut, LessonUpdate, ProgressUpdate
from app.services.audit_service import log_action
from app.services.badge_service import evaluate_badges_for_condition
from app.services.cache_service import cache_delete_prefix, cache_get, cache_set
from app.services.xp_service import award_xp

LESSON_COMPLETION_XP = 20


def list_lessons_for_module(db: Session, module_id: uuid.UUID) -> list[LessonListOut]:
    cache_key = f"lessons:by_module:{module_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return [LessonListOut.model_validate(l) for l in cached]
    if modules_repo.get_by_id(db, module_id) is None:
        raise NotFoundError("Module introuvable.")
    result = [LessonListOut.model_validate(l) for l in lessons_repo.list_by_module(db, module_id)]
    cache_set(cache_key, [l.model_dump(mode="json") for l in result], ttl=300)
    return result


def get_lesson(db: Session, lesson_id: uuid.UUID) -> LessonDetailOut:
    lesson = lessons_repo.get_by_id(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Leçon introuvable.")
    return LessonDetailOut.model_validate(lesson)


def create_lesson(db: Session, payload: LessonCreate, actor_id: uuid.UUID) -> LessonDetailOut:
    if modules_repo.get_by_id(db, payload.module_id) is None:
        raise NotFoundError("Module introuvable.")
    lesson = lessons_repo.create(db, Lesson(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="lesson.created", module="lessons", resource="lesson", resource_id=str(lesson.id))
    cache_delete_prefix("lessons:")
    return LessonDetailOut.model_validate(lesson)


def update_lesson(db: Session, lesson_id: uuid.UUID, payload: LessonUpdate, actor_id: uuid.UUID) -> LessonDetailOut:
    lesson = lessons_repo.get_by_id(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Leçon introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    lesson = lessons_repo.update(db, lesson, fields)
    log_action(db, user_id=actor_id, action="lesson.updated", module="lessons", resource="lesson", resource_id=str(lesson.id), new_value=fields)
    cache_delete_prefix("lessons:")
    return LessonDetailOut.model_validate(lesson)


def delete_lesson(db: Session, lesson_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    lesson = lessons_repo.get_by_id(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Leçon introuvable.")
    lessons_repo.delete(db, lesson)
    log_action(db, user_id=actor_id, action="lesson.deleted", module="lessons", resource="lesson", resource_id=str(lesson_id))
    cache_delete_prefix("lessons:")


def update_progress(db: Session, user_id: uuid.UUID, lesson_id: uuid.UUID, payload: ProgressUpdate) -> dict:
    """Met à jour la progression d'un utilisateur sur une leçon. Si la leçon passe à
    complétée pour la première fois, attribue de l'XP et évalue les badges liés.
    """
    lesson = lessons_repo.get_by_id(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Leçon introuvable.")

    existing = lessons_repo.get_progress(db, user_id, lesson_id)
    was_completed = existing.completed if existing else False

    fields = payload.model_dump(exclude_unset=True)
    if payload.completed is None:
        fields["completed"] = fields.get("progress", 0) >= 100
    progress = lessons_repo.upsert_progress(db, user_id, lesson_id, fields)

    if progress.completed and not was_completed:
        award_xp(db, user_id, LESSON_COMPLETION_XP, f"lesson_completed:{lesson_id}")
        from app.models.progress import XPHistory
        from sqlalchemy import select, func
        total_xp = db.execute(select(func.coalesce(func.sum(XPHistory.amount), 0)).where(XPHistory.user_id == user_id)).scalar_one()
        evaluate_badges_for_condition(db, user_id, "xp", int(total_xp))

    return {
        "lesson_id": lesson_id, "completed": progress.completed,
        "progress": progress.progress, "time_spent_seconds": progress.time_spent_seconds,
    }
