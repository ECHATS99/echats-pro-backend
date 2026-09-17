"""Évènement 'product.added' : notifie les utilisateurs d'un nouveau produit boutique."""
import uuid

from app.events.bus import publish, subscribe


def emit(product_id: uuid.UUID, name: str) -> None:
    publish("product.added", product_id=product_id, name=name)


def _notify_all(product_id: uuid.UUID, name: str) -> None:
    from app.core.database import SessionLocal
    from app.modules.notifications.schemas import NotificationBroadcast
    from app.modules.notifications.service import broadcast

    db = SessionLocal()
    try:
        broadcast(db, NotificationBroadcast(type="product", title="Nouveau produit BLACKHAWK LAB", message=name), actor_id=None)
    finally:
        db.close()


subscribe("product.added", _notify_all)
