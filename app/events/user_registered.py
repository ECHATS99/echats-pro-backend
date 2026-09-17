"""Évènement 'user.registered' : déclenché après création d'un compte (Partie 4.4 du SRS)."""
import uuid

from app.events.bus import publish


def emit(user_id: uuid.UUID, email: str, username: str) -> None:
    publish("user.registered", user_id=user_id, email=email, username=username)


def _send_welcome_email(user_id: uuid.UUID, email: str, username: str) -> None:
    from app.services.email_service import send_welcome_email
    send_welcome_email(email, username)


from app.events.bus import subscribe  # noqa: E402
subscribe("user.registered", _send_welcome_email)
