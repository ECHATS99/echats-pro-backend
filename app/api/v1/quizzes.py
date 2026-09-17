"""Routes HTTP /api/v1/quizzes."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.quizzes import service as quizzes_service
from app.modules.quizzes.schemas import QuizAttempt, QuizCreate, QuizPublicOut, QuizResult

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("/by-lesson/{lesson_id}", response_model=QuizPublicOut)
def get_quiz(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retourne le quiz sans révéler quelles réponses sont correctes."""
    return quizzes_service.get_quiz_for_lesson(db, lesson_id)


@router.post("", response_model=QuizPublicOut, status_code=201)
def create_quiz(
    payload: QuizCreate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return quizzes_service.create_quiz(db, payload, current.id)


@router.delete("/{quiz_id}", status_code=204)
def delete_quiz(
    quiz_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    quizzes_service.delete_quiz(db, quiz_id, current.id)


@router.post("/{quiz_id}/submit", response_model=QuizResult)
def submit_attempt(
    quiz_id: uuid.UUID, payload: QuizAttempt,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Corrige la tentative côté serveur et retourne le score."""
    return quizzes_service.submit_attempt(db, quiz_id, current.id, payload)
