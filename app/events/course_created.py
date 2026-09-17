"""Évènement 'course.created' : synchronise le nouveau contenu vers api.echats.ai
(RAG cyber) et notifie les utilisateurs intéressés."""
import uuid

from app.events.bus import publish, subscribe


def emit(track_id: uuid.UUID, title: str) -> None:
    publish("course.created", track_id=track_id, title=title)


def _sync_to_ia(track_id: uuid.UUID, title: str) -> None:
    from app.integrations.echats_ai.client import sync_knowledge
    sync_knowledge({"type": "track", "id": str(track_id), "title": title})


subscribe("course.created", _sync_to_ia)
