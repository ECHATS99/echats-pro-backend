"""Logique métier du domaine 'exercises' : soumission de code (Judge0) et de flags
(hash SHA256+sel, rate limiting anti-bruteforce 10 tentatives/heure — Partie 7 du SRS).
"""
import uuid

import redis

from app.core.exceptions import NotFoundError, ValidationError
from app.integrations.judge0.client import submit_code
from app.integrations.judge0.exceptions import Judge0Error
from app.models.exercise import Exercise
from app.modules.exercises import repository as exercises_repo
from app.modules.exercises.schemas import (
    CodeSubmission, ExerciseCreate, ExerciseOut, ExerciseUpdate, FlagSubmission, SubmissionResult,
)
from app.security.hash import generate_salt, hash_flag, verify_flag
from app.security.rate_limit import check_rate_limit
from app.services.audit_service import log_action
from app.services.badge_service import evaluate_badges_for_condition
from app.services.xp_service import award_xp
from app.services.websocket_service import broadcast_activity

FLAG_RATE_LIMIT_MAX = 10
FLAG_RATE_LIMIT_WINDOW_SECONDS = 3600


def _to_out(exercise: Exercise) -> ExerciseOut:
    data = ExerciseOut.model_validate(exercise)
    data.has_flag = exercise.flag is not None
    return data


def get_exercise(db, exercise_id: uuid.UUID) -> ExerciseOut:
    exercise = exercises_repo.get_by_id(db, exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")
    return _to_out(exercise)


def list_exercises_for_lesson(db, lesson_id: uuid.UUID) -> list[ExerciseOut]:
    return [_to_out(e) for e in exercises_repo.list_by_lesson(db, lesson_id)]


def create_exercise(db, payload: ExerciseCreate, actor_id: uuid.UUID) -> ExerciseOut:
    fields = payload.model_dump(exclude={"flag"})
    exercise = exercises_repo.create(db, Exercise(**fields))

    if payload.flag:
        salt = generate_salt()
        exercises_repo.upsert_flag(db, exercise.id, hash_flag(payload.flag, salt), salt)

    log_action(db, user_id=actor_id, action="exercise.created", module="exercises", resource="exercise", resource_id=str(exercise.id))
    return get_exercise(db, exercise.id)


def update_exercise(db, exercise_id: uuid.UUID, payload: ExerciseUpdate, actor_id: uuid.UUID) -> ExerciseOut:
    exercise = exercises_repo.get_by_id(db, exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")

    fields = payload.model_dump(exclude={"flag"}, exclude_unset=True)
    exercise = exercises_repo.update(db, exercise, fields)

    if payload.flag:
        salt = generate_salt()
        exercises_repo.upsert_flag(db, exercise.id, hash_flag(payload.flag, salt), salt)

    log_action(db, user_id=actor_id, action="exercise.updated", module="exercises", resource="exercise", resource_id=str(exercise.id), new_value=fields)
    return get_exercise(db, exercise.id)


def delete_exercise(db, exercise_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    exercise = exercises_repo.get_by_id(db, exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")
    exercises_repo.delete(db, exercise)
    log_action(db, user_id=actor_id, action="exercise.deleted", module="exercises", resource="exercise", resource_id=str(exercise_id))


def run_code(db, exercise_id: uuid.UUID, payload: CodeSubmission) -> SubmissionResult:
    """Exécute le code soumis dans une sandbox Judge0 (ne valide pas le flag ici,
    seulement l'exécution — utile pour les exercices de type 'code' sans flag).
    """
    exercise = exercises_repo.get_by_id(db, exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")
    if not exercise.judge0_language:
        raise ValidationError("Cet exercice n'accepte pas de soumission de code.")

    try:
        result = submit_code(payload.source_code, exercise.judge0_language, payload.stdin)
    except Judge0Error as exc:
        return SubmissionResult(correct=False, score=0, attempts=0, message=str(exc))

    success = result["status"] == "Accepted"
    return SubmissionResult(
        correct=success, score=exercise.points if success else 0, attempts=1,
        stdout=result.get("stdout"), stderr=result.get("stderr"),
        message="Exécution réussie." if success else f"Statut Judge0 : {result['status']}",
    )


def submit_flag(db, redis_client: redis.Redis, exercise_id: uuid.UUID, user_id: uuid.UUID, payload: FlagSubmission) -> SubmissionResult:
    """Valide un flag soumis contre son hash SHA256+sel. Protégé par rate limiting
    anti-bruteforce (10 tentatives/heure/utilisateur/exercice) et audit systématique.
    """
    exercise = exercises_repo.get_by_id(db, exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")
    if exercise.flag is None:
        raise ValidationError("Cet exercice n'a pas de flag configuré.")

    check_rate_limit(
        redis_client, f"ratelimit:flag_submit:{user_id}:{exercise_id}",
        FLAG_RATE_LIMIT_MAX, FLAG_RATE_LIMIT_WINDOW_SECONDS,
    )

    submission = exercises_repo.get_or_create_submission(db, exercise_id, user_id)
    submission.attempts += 1

    is_correct = verify_flag(payload.flag, exercise.flag.salt, exercise.flag.hash)
    already_solved = submission.correct

    if is_correct and not already_solved:
        submission.correct = True
        submission.score = exercise.points
        exercises_repo.save_submission(db, submission)

        award_xp(db, user_id, exercise.points, f"exercise_solved:{exercise_id}")
        from app.models.progress import XPHistory
        from sqlalchemy import select, func
        total_xp = db.execute(select(func.coalesce(func.sum(XPHistory.amount), 0)).where(XPHistory.user_id == user_id)).scalar_one()
        evaluate_badges_for_condition(db, user_id, "xp", int(total_xp))
        broadcast_activity({"user_id": str(user_id), "event": "exercise_solved", "exercise_id": str(exercise_id)})

        log_action(db, user_id=user_id, action="exercise.flag_correct", module="exercises", resource="exercise", resource_id=str(exercise_id))
        return SubmissionResult(correct=True, score=exercise.points, attempts=submission.attempts, message="Flag correct !")

    exercises_repo.save_submission(db, submission)
    log_action(db, user_id=user_id, action="exercise.flag_incorrect", module="exercises", resource="exercise", resource_id=str(exercise_id))

    if already_solved and is_correct:
        return SubmissionResult(correct=True, score=0, attempts=submission.attempts, message="Déjà résolu.")
    return SubmissionResult(correct=False, score=0, attempts=submission.attempts, message="Flag incorrect.")
