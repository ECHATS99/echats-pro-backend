"""Attribution automatique des badges selon les conditions remplies."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.badge import Badge, UserBadge
from app.models.user import User


def _has_badge(db: Session, user_id: uuid.UUID, badge_id: uuid.UUID) -> bool:
    stmt = select(UserBadge).where(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
    return db.execute(stmt).scalar_one_or_none() is not None


def evaluate_badges_for_condition(db: Session, user_id: uuid.UUID, condition_type: str, current_value: int) -> list[Badge]:
    """Évalue tous les badges d'un type de condition donné (ex: 'xp', 'ctf_solves', 'streak')
    et attribue ceux dont le seuil est atteint et non encore obtenus. Retourne les badges
    nouvellement débloqués.
    """
    stmt = select(Badge).where(Badge.condition_type == condition_type, Badge.condition_value <= current_value)
    candidates = db.execute(stmt).scalars().all()

    unlocked: list[Badge] = []
    for badge in candidates:
        if _has_badge(db, user_id, badge.id):
            continue
        db.add(UserBadge(user_id=user_id, badge_id=badge.id))
        if badge.xp_reward:
            from app.services.xp_service import award_xp
            award_xp(db, user_id, badge.xp_reward, f"badge:{badge.name}")
        unlocked.append(badge)

    if unlocked:
        db.commit()
        from app.services.websocket_service import broadcast_notification
        for badge in unlocked:
            broadcast_notification(user_id, "badge", "Badge obtenu !", f"Vous avez débloqué le badge « {badge.name} ».")

    return unlocked
