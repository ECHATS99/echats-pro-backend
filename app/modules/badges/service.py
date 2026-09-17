"""Logique métier du domaine 'badges'."""
import uuid

from app.core.exceptions import NotFoundError
from app.models.badge import Badge
from app.modules.badges import repository as badges_repo
from app.modules.badges.schemas import BadgeCreate, BadgeOut, UserBadgeOut
from app.services.audit_service import log_action


def list_badges(db) -> list[BadgeOut]:
    return [BadgeOut.model_validate(b) for b in badges_repo.list_all(db)]


def create_badge(db, payload: BadgeCreate, actor_id: uuid.UUID) -> BadgeOut:
    badge = badges_repo.create(db, Badge(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="badge.created", module="badges", resource="badge", resource_id=str(badge.id))
    return BadgeOut.model_validate(badge)


def delete_badge(db, badge_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    badge = badges_repo.get_by_id(db, badge_id)
    if badge is None:
        raise NotFoundError("Badge introuvable.")
    badges_repo.delete(db, badge)
    log_action(db, user_id=actor_id, action="badge.deleted", module="badges", resource="badge", resource_id=str(badge_id))


def list_user_badges(db, user_id: uuid.UUID) -> list[UserBadgeOut]:
    return [UserBadgeOut(badge=BadgeOut.model_validate(ub.badge), earned_at=ub.earned_at.isoformat()) for ub in badges_repo.list_for_user(db, user_id)]
