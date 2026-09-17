"""Routes HTTP /api/v1/institutions (organisations / Chambre Close)."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.models.user import User
from app.modules.organizations import service as organizations_service
from app.modules.organizations.schemas import (
    InstitutionCreate, InstitutionMemberOut, InstitutionOut, InstitutionUpdate,
)

router = APIRouter(prefix="/institutions", tags=["organizations"])


@router.get("")
def list_institutions(
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
    current: CurrentUser = Depends(require_permission("institution.manage")), db: Session = Depends(get_db),
):
    return organizations_service.list_institutions(db, page, limit)


@router.post("", response_model=InstitutionOut, status_code=201)
def create_institution(
    payload: InstitutionCreate,
    current: CurrentUser = Depends(require_permission("institution.manage")), db: Session = Depends(get_db),
):
    return organizations_service.create_institution(db, payload, current.id)


@router.get("/{institution_id}", response_model=InstitutionOut)
def get_institution(
    institution_id: uuid.UUID,
    user: User = Depends(get_current_db_user),
    db: Session = Depends(get_db),
):
    return organizations_service.get_institution(db, institution_id, user)


@router.patch("/{institution_id}", response_model=InstitutionOut)
def update_institution(
    institution_id: uuid.UUID, payload: InstitutionUpdate,
    current: CurrentUser = Depends(require_permission("institution.manage")), db: Session = Depends(get_db),
):
    return organizations_service.update_institution(db, institution_id, payload, current.id)


@router.get("/{institution_id}/members", response_model=list[InstitutionMemberOut])
def list_members(institution_id: uuid.UUID, user: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    """Isolation stricte : seuls les membres de la même institution y accèdent (sauf admin)."""
    return organizations_service.list_members(db, institution_id, user.institution_id)
