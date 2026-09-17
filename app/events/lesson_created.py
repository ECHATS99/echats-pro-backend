"""Évènement 'lesson.created' : synchronise la nouvelle leçon vers api.echats.ai (RAG cyber)."""
import uuid

from app.events.bus import publish, subscribe


def emit(lesson_id: uuid.UUID, title: str) -> None:
    publish("lesson.created", lesson_id=lesson_id, title=title)


def _sync_to_ia(lesson_id: uuid.UUID, title: str) -> None:
    from app.integrations.echats_ai.client import sync_knowledge
    sync_knowledge({"type": "lesson", "id": str(lesson_id), "title": title})


subscribe("lesson.created", _sync_to_ia)
