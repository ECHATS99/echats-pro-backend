"""Routes HTTP /api/v1/exercises."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.dependencies.redis import get_redis
from app.modules.exercises import service as exercises_service
from app.modules.exercises.schemas import (
    CodeSubmission, ExerciseCreate, ExerciseOut, ExerciseUpdate, FlagSubmission, SubmissionResult,
)

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/by-lesson/{lesson_id}", response_model=list[ExerciseOut])
def list_exercises(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    return exercises_service.list_exercises_for_lesson(db, lesson_id)


@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(exercise_id: uuid.UUID, db: Session = Depends(get_db)):
    return exercises_service.get_exercise(db, exercise_id)


@router.post("", response_model=ExerciseOut, status_code=201)
def create_exercise(
    payload: ExerciseCreate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return exercises_service.create_exercise(db, payload, current.id)


@router.patch("/{exercise_id}", response_model=ExerciseOut)
def update_exercise(
    exercise_id: uuid.UUID, payload: ExerciseUpdate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return exercises_service.update_exercise(db, exercise_id, payload, current.id)


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    exercises_service.delete_exercise(db, exercise_id, current.id)


@router.post("/{exercise_id}/run", response_model=SubmissionResult)
def run_code(
    exercise_id: uuid.UUID, payload: CodeSubmission,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Exécute le code soumis dans une sandbox Judge0 isolée."""
    return exercises_service.run_code(db, exercise_id, payload)


@router.post("/{exercise_id}/submit", response_model=SubmissionResult)
def submit_flag(
    exercise_id: uuid.UUID, payload: FlagSubmission,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db), redis_client=Depends(get_redis),
):
    """Soumet un flag (rate limité à 10 tentatives/heure/exercice)."""
    return exercises_service.submit_flag(db, redis_client, exercise_id, current.id, payload)
