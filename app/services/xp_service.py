"""Calcul et attribution de l'XP, changements de niveau."""
import uuid

from sqlalchemy.orm import Session

from app.models.progress import XPHistory
from app.models.user import User

# Courbe de progression : niveau n requiert n * LEVEL_XP_STEP XP cumulés.
LEVEL_XP_STEP = 500


def level_for_xp(xp: int) -> int:
    """Calcule le niveau à partir de l'XP total cumulé."""
    level = 1
    threshold = LEVEL_XP_STEP
    while xp >= threshold:
        level += 1
        threshold += LEVEL_XP_STEP * level
    return level


def award_xp(db: Session, user_id: uuid.UUID, amount: int, reason: str) -> User:
    """Ajoute de l'XP à un utilisateur, recalcule son niveau, journalise dans xp_history.
    N'effectue jamais de commit destructif : lève simplement les valeurs et laisse
    l'appelant décider du commit final (mais commit ici pour rester atomique et simple).
    """
    user = db.get(User, user_id)
    if user is None:
        return None

    user.xp = max(0, user.xp + amount)
    new_level = level_for_xp(user.xp)
    leveled_up = new_level > user.level
    user.level = new_level

    db.add(XPHistory(user_id=user_id, amount=amount, reason=reason))
    db.add(user)
    db.commit()
    db.refresh(user)

    if leveled_up:
        from app.services.websocket_service import broadcast_notification
        broadcast_notification(user_id, "level_up", "Niveau supérieur !", f"Vous êtes maintenant niveau {new_level}.")

    return user
