"""Évènement 'ctf.published' : notifie tous les utilisateurs (Partie 14 du SRS)."""
import uuid

from app.events.bus import publish, subscribe


def emit(challenge_id: uuid.UUID, title: str) -> None:
    publish("ctf.published", challenge_id=challenge_id, title=title)


def _notify_all(challenge_id: uuid.UUID, title: str) -> None:
    from app.core.database import SessionLocal
    from app.modules.notifications.schemas import NotificationBroadcast
    from app.modules.notifications.service import broadcast

    db = SessionLocal()
    try:
        broadcast(db, NotificationBroadcast(type="new_ctf", title="Nouveau challenge CTF", message=title), actor_id=None)
    finally:
        db.close()


subscribe("ctf.published", _notify_all)
