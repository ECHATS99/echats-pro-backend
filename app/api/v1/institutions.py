"""Routes /api/v1/institutions — Chambre Close."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.models.user import User
from app.modules.institutions import service as inst_service
from app.modules.institutions.schemas import (
    InstitutionCreate, InstitutionOut, InstitutionUpdate,
    AccessKeyCreate, AccessKeyOut, JoinWithKeyRequest, JoinResult,
)

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get("", response_model=list[InstitutionOut])
def list_institutions(db: Session = Depends(get_db)):
    return inst_service.list_institutions(db)


@router.get("/{id_or_slug}", response_model=InstitutionOut)
def get_institution(id_or_slug: str, db: Session = Depends(get_db)):
    return inst_service.get_institution(db, id_or_slug)


@router.post("", response_model=InstitutionOut, status_code=201)
def create_institution(
    payload: InstitutionCreate,
    current: CurrentUser = Depends(require_permission("institutions.manage")),
    db: Session = Depends(get_db),
):
    return inst_service.create_institution(db, payload, current.id)


@router.patch("/{inst_id}", response_model=InstitutionOut)
def update_institution(
    inst_id: uuid.UUID, payload: InstitutionUpdate,
    current: CurrentUser = Depends(require_permission("institutions.manage")),
    db: Session = Depends(get_db),
):
    return inst_service.update_institution(db, inst_id, payload, current.id)


@router.get("/{inst_id}/members")
def list_members(inst_id: uuid.UUID, db: Session = Depends(get_db)):
    return inst_service.list_members(db, inst_id)


# --- ACCESS KEYS ---

@router.post("/{inst_id}/keys", response_model=AccessKeyOut, status_code=201)
def generate_key(
    inst_id: uuid.UUID, payload: AccessKeyCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return inst_service.generate_access_key(db, inst_id, payload, current.id)


@router.get("/{inst_id}/keys", response_model=list[AccessKeyOut])
def list_keys(
    inst_id: uuid.UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return inst_service.list_keys(db, inst_id)


@router.delete("/keys/{key_id}")
def revoke_key(
    key_id: uuid.UUID,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return inst_service.revoke_key(db, key_id, current.id)


@router.post("/join", response_model=JoinResult)
def join_with_key(
    payload: JoinWithKeyRequest,
    user: User = Depends(get_current_db_user),
    db: Session = Depends(get_db),
):
    return inst_service.join_with_key(db, payload.key, user)


@router.post("/{inst_id}/join-direct", response_model=JoinResult)
def join_direct(
    inst_id: uuid.UUID,
    user: User = Depends(get_current_db_user),
    db: Session = Depends(get_db),
):
    return inst_service.join_direct(db, inst_id, user)
