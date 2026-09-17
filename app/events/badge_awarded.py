"""Évènement 'badge.awarded' : déclenché par badge_service après attribution d'un badge."""
import uuid

from app.events.bus import publish


def emit(user_id: uuid.UUID, badge_name: str) -> None:
    publish("badge.awarded", user_id=user_id, badge_name=badge_name)
