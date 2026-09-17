"""Routes HTTP /api/v1/paraben (module Paraben / Chambre Close)."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.models.user import User
from app.modules.paraben import service as paraben_service
from app.modules.paraben.schemas import (
    ParabenCourseCreate, ParabenCourseOut, ParabenProgressOut, ParabenProgressUpdate, ParabenRevenueReport,
)

router = APIRouter(prefix="/paraben", tags=["paraben"])


@router.get("/courses", response_model=list[ParabenCourseOut])
def list_courses(user: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    """Accès contrôlé côté serveur (Zero Trust) : abonnement Paraben ou institution partenaire."""
    return paraben_service.list_courses(db, user)


@router.post("/courses", response_model=ParabenCourseOut, status_code=201)
def create_course(
    payload: ParabenCourseCreate,
    current=Depends(require_permission("paraben.manage")),
    db: Session = Depends(get_db),
):
    return paraben_service.create_course(db, payload, current.id)


@router.patch("/courses/{course_id}/progress", response_model=ParabenProgressOut)
def update_progress(
    course_id: uuid.UUID, payload: ParabenProgressUpdate,
    user: User = Depends(get_current_db_user), db: Session = Depends(get_db),
):
    return paraben_service.update_progress(db, user, course_id, payload)


@router.get("/revenue", response_model=ParabenRevenueReport)
def revenue_report(
    period: str, current=Depends(require_permission("paraben.manage")), db: Session = Depends(get_db),
):
    """Rapport mensuel de revenus, format 'YYYY-MM' (Partie 6 du SRS)."""
    return paraben_service.revenue_report(db, period)
