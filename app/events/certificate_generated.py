"""Évènement 'certificate.generated' : déclenché après génération réussie d'un certificat PDF."""
import uuid

from app.events.bus import publish


def emit(certificate_id: uuid.UUID, user_id: uuid.UUID, track_title: str) -> None:
    publish("certificate.generated", certificate_id=certificate_id, user_id=user_id, track_title=track_title)
