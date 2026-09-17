"""Évènement 'subscription.created' : déclenché après initiation d'un abonnement (avant activation)."""
import uuid

from app.events.bus import publish


def emit(subscription_id: uuid.UUID, user_id: uuid.UUID, plan_code: str) -> None:
    publish("subscription.created", subscription_id=subscription_id, user_id=user_id, plan_code=plan_code)
