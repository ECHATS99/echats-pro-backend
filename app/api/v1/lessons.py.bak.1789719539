"""Routes HTTP /api/v1/lessons."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.lessons import service as lessons_service
from app.modules.lessons.schemas import LessonCreate, LessonDetailOut, LessonListOut, LessonUpdate, ProgressUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/by-module/{module_id}", response_model=list[LessonListOut])
def list_lessons(module_id: uuid.UUID, db: Session = Depends(get_db)):
    return lessons_service.list_lessons_for_module(db, module_id)


@router.get("/{lesson_id}", response_model=LessonDetailOut)
def get_lesson(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    return lessons_service.get_lesson(db, lesson_id)


@router.post("", response_model=LessonDetailOut, status_code=201)
def create_lesson(
    payload: LessonCreate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return lessons_service.create_lesson(db, payload, current.id)


@router.patch("/{lesson_id}", response_model=LessonDetailOut)
def update_lesson(
    lesson_id: uuid.UUID, payload: LessonUpdate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return lessons_service.update_lesson(db, lesson_id, payload, current.id)


@router.delete("/{lesson_id}", status_code=204)
def delete_lesson(
    lesson_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    lessons_service.delete_lesson(db, lesson_id, current.id)


@router.post("/{lesson_id}/progress")
def update_progress(
    lesson_id: uuid.UUID, payload: ProgressUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Met à jour la progression de l'utilisateur authentifié sur cette leçon."""
    return lessons_service.update_progress(db, current.id, lesson_id, payload)
