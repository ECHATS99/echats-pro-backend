"""Routes HTTP /api/v1/admin (paramètres, feature flags, logs, audit, maintenance, système)."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.admin import service as admin_service
from app.modules.admin.schemas import (
    AdminSettingUpdate, FeatureFlagOut, FeatureFlagUpdate, MaintenanceUpdate, SystemMessageCreate, SystemMessageOut,
)
from app.modules.audit import service as audit_service
from app.modules.audit.schemas import AuditLogOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/logs")
def logs(
    page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), module: str | None = None,
    current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db),
):
    return admin_service.list_application_logs(module)


@router.get("/audit")
def audit(
    page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200),
    module: str | None = None, action: str | None = None, user_id: uuid.UUID | None = None,
    current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db),
):
    return audit_service.list_logs(db, page, limit, module, action, user_id)


@router.get("/settings")
def get_settings(current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.get_all_settings(db)


@router.patch("/settings")
def update_settings(payload: AdminSettingUpdate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.update_setting(db, payload, current.id)


@router.get("/feature-flags", response_model=list[FeatureFlagOut])
def list_flags(current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.list_feature_flags(db)


@router.patch("/feature-flags", response_model=FeatureFlagOut)
def update_flag(payload: FeatureFlagUpdate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.update_feature_flag(db, payload, current.id)


@router.post("/system-messages", response_model=SystemMessageOut, status_code=201)
def create_system_message(payload: SystemMessageCreate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.create_system_message(db, payload, current.id)


@router.get("/system", response_model=list[SystemMessageOut])
def list_system_messages(db: Session = Depends(get_db)):
    return admin_service.list_active_system_messages(db)


@router.post("/maintenance")
def set_maintenance(payload: MaintenanceUpdate, current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return admin_service.set_maintenance(db, payload, current.id)
