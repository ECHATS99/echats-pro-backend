"""Routes HTTP /api/v1/classrooms."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.classroom import service as classroom_service
from app.modules.classroom.schemas import (
    AssignmentCreate, AssignmentOut, ClassroomCreate, ClassroomJoin, ClassroomMemberOut, ClassroomOut,
)

router = APIRouter(prefix="/classrooms", tags=["classroom"])


@router.get("", response_model=list[ClassroomOut])
def list_my_classrooms(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return classroom_service.list_my_classrooms(db, current.id)


@router.post("", response_model=ClassroomOut, status_code=201)
def create_classroom(
    payload: ClassroomCreate,
    current: CurrentUser = Depends(require_permission("classroom.create")),
    db: Session = Depends(get_db),
):
    return classroom_service.create_classroom(db, payload, current.id)


@router.get("/{classroom_id}", response_model=ClassroomOut)
def get_classroom(classroom_id: uuid.UUID, db: Session = Depends(get_db)):
    return classroom_service.get_classroom(db, classroom_id)


@router.post("/join", response_model=ClassroomMemberOut)
def join_classroom(payload: ClassroomJoin, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return classroom_service.join_classroom(db, payload, current.id)


@router.post("/{classroom_id}/leave", status_code=204)
def leave_classroom(classroom_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    classroom_service.leave_classroom(db, classroom_id, current.id)


@router.get("/{classroom_id}/members", response_model=list[ClassroomMemberOut])
def list_members(classroom_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return classroom_service.list_members(db, classroom_id, current.id)


@router.post("/{classroom_id}/assignments", response_model=AssignmentOut, status_code=201)
def create_assignment(
    classroom_id: uuid.UUID, payload: AssignmentCreate,
    current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db),
):
    return classroom_service.create_assignment(db, classroom_id, payload, current.id)


@router.get("/{classroom_id}/assignments", response_model=list[AssignmentOut])
def list_assignments(classroom_id: uuid.UUID, db: Session = Depends(get_db)):
    return classroom_service.list_assignments(db, classroom_id)
