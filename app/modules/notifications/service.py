"""Logique métier du domaine 'notifications'. Création, diffusion en masse, lecture temps réel."""
import uuid

from sqlalchemy import select

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.notification import Notification
from app.models.user import User
from app.modules.notifications import repository as notifications_repo
from app.modules.notifications.schemas import NotificationBroadcast, NotificationOut
from app.services.audit_service import log_action
from app.services.websocket_service import broadcast_notification
from app.utils.pagination import paginate


def create_and_push(db, user_id: uuid.UUID, type_: str, title: str, message: str) -> NotificationOut:
    """Crée une notification en base ET la pousse en temps réel (utilisé par les autres
    domaines : nouveau CTF, nouveau cours, badge, certificat, produit, annonce...).
    """
    notification = notifications_repo.create(db, Notification(user_id=user_id, type=type_, title=title, message=message))
    broadcast_notification(user_id, type_, title, message)
    return NotificationOut.model_validate(notification)


def list_my_notifications(db, user_id: uuid.UUID, page: int, limit: int, unread_only: bool):
    items, total = notifications_repo.list_for_user(db, user_id, page, limit, unread_only)
    return paginate([NotificationOut.model_validate(n).model_dump() for n in items], page, limit, total)


def mark_read(db, notification_id: uuid.UUID, user_id: uuid.UUID) -> NotificationOut:
    notification = notifications_repo.get_by_id(db, notification_id)
    if notification is None:
        raise NotFoundError("Notification introuvable.")
    if notification.user_id != user_id:
        raise ForbiddenError("Cette notification ne vous appartient pas.")
    notification = notifications_repo.mark_read(db, notification)
    return NotificationOut.model_validate(notification)


def mark_all_read(db, user_id: uuid.UUID) -> None:
    notifications_repo.mark_all_read(db, user_id)


def delete_notification(db, notification_id: uuid.UUID, user_id: uuid.UUID) -> None:
    notification = notifications_repo.get_by_id(db, notification_id)
    if notification is None:
        raise NotFoundError("Notification introuvable.")
    if notification.user_id != user_id:
        raise ForbiddenError("Cette notification ne vous appartient pas.")
    notifications_repo.delete(db, notification)


def unread_count(db, user_id: uuid.UUID) -> int:
    return notifications_repo.unread_count(db, user_id)


def broadcast(db, payload: NotificationBroadcast, actor_id: uuid.UUID) -> int:
    """Diffuse une notification à une liste d'utilisateurs, ou à tous si `user_ids` est vide
    (Partie 14 du SRS : nouveau CTF, cours publié, promotion, maintenance...).
    """
    user_ids = payload.user_ids
    if not user_ids:
        user_ids = list(db.execute(select(User.id)).scalars().all())

    for uid in user_ids:
        create_and_push(db, uid, payload.type, payload.title, payload.message)

    log_action(db, user_id=actor_id, action="notification.broadcast", module="notifications", resource="notification", new_value={"count": len(user_ids)})
    return len(user_ids)
