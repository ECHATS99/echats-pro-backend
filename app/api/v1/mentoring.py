"""Routes HTTP /api/v1/mentoring."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.modules.mentoring import service as mentoring_service
from app.modules.mentoring.schemas import MentorOut, MentorSessionOut, MentorSessionRequest, MentorSessionUpdate

router = APIRouter(prefix="/mentoring", tags=["mentoring"])


@router.get("/mentors", response_model=list[MentorOut])
def list_mentors(db: Session = Depends(get_db)):
    return mentoring_service.list_mentors(db)


@router.post("/mentors", response_model=MentorOut, status_code=201)
def become_mentor(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return mentoring_service.become_mentor(db, current.id)


@router.post("/request", response_model=MentorSessionOut, status_code=201)
def request_session(payload: MentorSessionRequest, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return mentoring_service.request_session(db, payload, current.id)


@router.get("/session", response_model=list[MentorSessionOut])
def my_sessions(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return mentoring_service.list_my_sessions(db, current.id)


@router.get("/queue", response_model=list[MentorSessionOut])
def my_queue(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """File d'attente des reviews à traiter par le mentor connecté."""
    return mentoring_service.list_queue(db, current.id)


@router.patch("/session/{session_id}", response_model=MentorSessionOut)
def update_session(
    session_id: uuid.UUID, payload: MentorSessionUpdate, is_mentor: bool = False,
    current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db),
):
    return mentoring_service.update_session(db, session_id, payload, current.id, is_mentor)


@router.delete("/session/{session_id}", status_code=204)
def cancel_session(session_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    mentoring_service.update_session(db, session_id, MentorSessionUpdate(status="cancelled"), current.id, False)
