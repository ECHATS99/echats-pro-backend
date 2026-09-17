"""Diffusion des évènements temps réel (notifications, activité, classement, classroom, terminal).

Phase 2 : la diffusion effective passe par app.websocket.manager (connexions actives en mémoire
du process). Ce service est le point d'entrée unique utilisé par tous les domaines métier pour
ne jamais coupler leur logique au protocole WebSocket lui-même.
"""
import uuid

from app.websocket.manager import connection_manager


def broadcast_notification(user_id: uuid.UUID, type_: str, title: str, message: str) -> None:
    """Pousse une notification temps réel à un utilisateur connecté (best effort, non bloquant)."""
    connection_manager.send_to_user(user_id, {
        "channel": "notifications",
        "type": type_,
        "title": title,
        "message": message,
    })


def broadcast_leaderboard_update(payload: dict) -> None:
    connection_manager.broadcast_channel("leaderboard", {"channel": "leaderboard", **payload})


def broadcast_activity(payload: dict) -> None:
    connection_manager.broadcast_channel("activity", {"channel": "activity", **payload})


def broadcast_classroom(classroom_id: uuid.UUID, payload: dict) -> None:
    connection_manager.broadcast_room(f"classroom:{classroom_id}", {"channel": "classroom", **payload})
