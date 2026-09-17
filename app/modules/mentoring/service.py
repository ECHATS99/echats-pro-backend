"""Logique métier du domaine 'mentoring'. File d'attente des reviews, notation, feedback."""
import uuid

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.mentor import Mentor, MentorSession
from app.modules.mentoring import repository as mentoring_repo
from app.modules.mentoring.schemas import (
    MentorOut, MentorSessionOut, MentorSessionRequest, MentorSessionUpdate,
)
from app.services.audit_service import log_action
from app.services.websocket_service import broadcast_notification
from app.services.xp_service import award_xp

MENTOR_RATING_XP = 10


def list_mentors(db) -> list[MentorOut]:
    return [MentorOut.model_validate(m) for m in mentoring_repo.list_mentors(db)]


def become_mentor(db, user_id: uuid.UUID) -> MentorOut:
    if mentoring_repo.get_mentor_by_user(db, user_id) is not None:
        raise ConflictError("Vous êtes déjà enregistré comme mentor.")
    mentor = mentoring_repo.create_mentor(db, Mentor(user_id=user_id))
    log_action(db, user_id=user_id, action="mentor.registered", module="mentoring", resource="mentor", resource_id=str(mentor.id))
    return MentorOut.model_validate(mentor)


def request_session(db, payload: MentorSessionRequest, student_id: uuid.UUID) -> MentorSessionOut:
    mentor = mentoring_repo.get_mentor(db, payload.mentor_id)
    if mentor is None:
        raise NotFoundError("Mentor introuvable.")
    session = mentoring_repo.create_session(db, MentorSession(
        mentor_id=payload.mentor_id, student_id=student_id,
        exercise_id=payload.exercise_id, meeting_date=payload.meeting_date, status="pending",
    ))
    broadcast_notification(mentor.user_id, "mentoring", "Nouvelle demande de mentorat", "Un étudiant attend votre review.")
    log_action(db, user_id=student_id, action="mentoring.requested", module="mentoring", resource="session", resource_id=str(session.id))
    return MentorSessionOut.model_validate(session)


def update_session(db, session_id: uuid.UUID, payload: MentorSessionUpdate, actor_id: uuid.UUID, is_mentor: bool) -> MentorSessionOut:
    session = mentoring_repo.get_session(db, session_id)
    if session is None:
        raise NotFoundError("Session de mentorat introuvable.")

    mentor = mentoring_repo.get_mentor(db, session.mentor_id)
    if not is_mentor and session.student_id != actor_id:
        raise ForbiddenError("Vous n'êtes pas autorisé à modifier cette session.")
    if is_mentor and mentor.user_id != actor_id:
        raise ForbiddenError("Vous n'êtes pas le mentor assigné à cette session.")

    fields = payload.model_dump(exclude_unset=True)
    was_completed = session.status == "completed"
    session = mentoring_repo.update_session(db, session, fields)

    if session.status == "completed" and not was_completed:
        award_xp(db, session.student_id, MENTOR_RATING_XP, f"mentoring_completed:{session.id}")
        if session.rating:
            mentor.rating = round(((mentor.rating * mentor.reviews_count) + session.rating) / (mentor.reviews_count + 1), 2)
            mentor.reviews_count += 1
            db.add(mentor)
            db.commit()

    log_action(db, user_id=actor_id, action="mentoring.session_updated", module="mentoring", resource="session", resource_id=str(session.id))
    return MentorSessionOut.model_validate(session)


def list_queue(db, mentor_user_id: uuid.UUID) -> list[MentorSessionOut]:
    mentor = mentoring_repo.get_mentor_by_user(db, mentor_user_id)
    if mentor is None:
        raise NotFoundError("Vous n'êtes pas enregistré comme mentor.")
    return [MentorSessionOut.model_validate(s) for s in mentoring_repo.list_queue_for_mentor(db, mentor.id)]


def list_my_sessions(db, student_id: uuid.UUID) -> list[MentorSessionOut]:
    return [MentorSessionOut.model_validate(s) for s in mentoring_repo.list_for_student(db, student_id)]
