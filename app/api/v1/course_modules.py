"""Routes HTTP /api/v1/modules."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.course_modules import service as modules_service
from app.modules.course_modules.schemas import CourseModuleCreate, CourseModuleOut, CourseModuleUpdate

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/by-track/{track_id}", response_model=list[CourseModuleOut])
def list_modules(track_id: uuid.UUID, db: Session = Depends(get_db)):
    return modules_service.list_modules_for_track(db, track_id)


@router.get("/{module_id}", response_model=CourseModuleOut)
def get_module(module_id: uuid.UUID, db: Session = Depends(get_db)):
    return modules_service.get_module(db, module_id)


@router.post("", response_model=CourseModuleOut, status_code=201)
def create_module(
    payload: CourseModuleCreate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return modules_service.create_module(db, payload, current.id)


@router.patch("/{module_id}", response_model=CourseModuleOut)
def update_module(
    module_id: uuid.UUID, payload: CourseModuleUpdate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return modules_service.update_module(db, module_id, payload, current.id)


@router.delete("/{module_id}", status_code=204)
def delete_module(
    module_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    modules_service.delete_module(db, module_id, current.id)
