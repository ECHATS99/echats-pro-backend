"""Persistance des sessions de labs éphémères dans Redis (aucune donnée métier permanente,
conformément à la Partie 7.4 du SRS). Clé : lab_session:<lab_id>."""
import json
import uuid

from app.core.redis import get_redis_client

LAB_SESSION_TTL_SECONDS = 1800  # 30 minutes d'inactivité (Partie 7 du SRS)


def save_session(lab_id: str, data: dict) -> None:
    get_redis_client().set(f"lab_session:{lab_id}", json.dumps(data, default=str), ex=LAB_SESSION_TTL_SECONDS)


def get_session(lab_id: str) -> dict | None:
    raw = get_redis_client().get(f"lab_session:{lab_id}")
    return json.loads(raw) if raw else None


def touch_session(lab_id: str) -> None:
    """Prolonge le TTL à chaque interaction (reset de l'inactivité)."""
    get_redis_client().expire(f"lab_session:{lab_id}", LAB_SESSION_TTL_SECONDS)


def delete_session(lab_id: str) -> None:
    get_redis_client().delete(f"lab_session:{lab_id}")
