"""Routes HTTP /api/v1/badges."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.badges import service as badges_service
from app.modules.badges.schemas import BadgeCreate, BadgeOut, UserBadgeOut

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("", response_model=list[BadgeOut])
def list_badges(db: Session = Depends(get_db)):
    return badges_service.list_badges(db)


@router.post("", response_model=BadgeOut, status_code=201)
def create_badge(
    payload: BadgeCreate,
    current: CurrentUser = Depends(require_permission("admin.access")),
    db: Session = Depends(get_db),
):
    return badges_service.create_badge(db, payload, current.id)


@router.delete("/{badge_id}", status_code=204)
def delete_badge(
    badge_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("admin.access")),
    db: Session = Depends(get_db),
):
    badges_service.delete_badge(db, badge_id, current.id)


@router.get("/me", response_model=list[UserBadgeOut])
def my_badges(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return badges_service.list_user_badges(db, current.id)
