"""Routes HTTP /api/v1/notifications."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.notifications import service as notifications_service
from app.modules.notifications.schemas import NotificationBroadcast, NotificationOut

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), unread_only: bool = False,
    current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db),
):
    return notifications_service.list_my_notifications(db, current.id, page, limit, unread_only)


@router.get("/unread-count")
def unread_count(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"count": notifications_service.unread_count(db, current.id)}


@router.patch("/read", response_model=NotificationOut)
def mark_read(notification_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return notifications_service.mark_read(db, notification_id, current.id)


@router.patch("/read-all", status_code=204)
def mark_all_read(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications_service.mark_all_read(db, current.id)


@router.delete("/{notification_id}", status_code=204)
def delete_notification(notification_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications_service.delete_notification(db, notification_id, current.id)


@router.post("/broadcast")
def broadcast(
    payload: NotificationBroadcast,
    current: CurrentUser = Depends(require_permission("notifications.send")),
    db: Session = Depends(get_db),
):
    count = notifications_service.broadcast(db, payload, current.id)
    return {"sent": count}
