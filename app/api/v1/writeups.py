"""Routes HTTP /api/v1/writeups."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.dependencies.roles import require_role
from app.modules.writeups import service as writeups_service
from app.modules.writeups.schemas import VoteRequest, WriteupCreate, WriteupOut, WriteupUpdate

router = APIRouter(prefix="/writeups", tags=["writeups"])


@router.get("")
def list_writeups(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), ctf_id: uuid.UUID | None = None, db: Session = Depends(get_db)):
    return writeups_service.list_writeups(db, page, limit, ctf_id)


@router.get("/{writeup_id}", response_model=WriteupOut)
def get_writeup(writeup_id: uuid.UUID, db: Session = Depends(get_db)):
    return writeups_service.get_writeup(db, writeup_id)


@router.post("", response_model=WriteupOut, status_code=201)
def create_writeup(payload: WriteupCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return writeups_service.create_writeup(db, payload, current.id)


@router.patch("/{writeup_id}", response_model=WriteupOut)
def update_writeup(writeup_id: uuid.UUID, payload: WriteupUpdate, current: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    is_moderator = current.primary_role_name in ("admin", "super_admin", "instructor", "mentor")
    return writeups_service.update_writeup(db, writeup_id, payload, current.id, is_moderator)


@router.delete("/{writeup_id}", status_code=204)
def delete_writeup(writeup_id: uuid.UUID, current: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    is_moderator = current.primary_role_name in ("admin", "super_admin", "instructor", "mentor")
    writeups_service.delete_writeup(db, writeup_id, current.id, is_moderator)


@router.post("/{writeup_id}/vote", response_model=WriteupOut)
def vote(writeup_id: uuid.UUID, payload: VoteRequest, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return writeups_service.vote(db, writeup_id, current.id, payload)
