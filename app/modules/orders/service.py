"""Logique métier du domaine 'orders'. Crée la commande à partir du panier, calcule le
montant côté serveur (jamais confiance au prix envoyé par le frontend), puis délègue
l'initiation du paiement au module payments.
"""
import uuid

from app.core.exceptions import NotFoundError, ValidationError
from app.models.order import Order, OrderItem
from app.modules.orders import repository as orders_repo
from app.modules.orders.schemas import OrderCreate, OrderOut, OrderPaymentIntentOut
from app.modules.payments import service as payments_service
from app.modules.products import repository as products_repo
from app.services.audit_service import log_action


def create_order(db, payload: OrderCreate, user_id: uuid.UUID) -> OrderPaymentIntentOut:
    items: list[OrderItem] = []
    total = 0

    for entry in payload.items:
        product = products_repo.get_by_id(db, entry.product_id)
        if product is None or not product.available:
            raise NotFoundError(f"Produit introuvable ou indisponible : {entry.product_id}")
        if product.stock < entry.quantity:
            raise ValidationError(f"Stock insuffisant pour « {product.name} ».")
        items.append(OrderItem(product_id=product.id, quantity=entry.quantity, unit_price=product.price_fcfa))
        total += product.price_fcfa * entry.quantity

    order = Order(user_id=user_id, status="pending", amount=total, currency=payload.currency, payment_provider=payload.payment_provider)
    order.items = items
    order = orders_repo.create(db, order)

    for entry in payload.items:
        product = products_repo.get_by_id(db, entry.product_id)
        products_repo.decrement_stock(db, product, entry.quantity)

    payment, extra = payments_service.initiate_payment(
        db, user_id=user_id, amount=total, currency=payload.currency, provider=payload.payment_provider,
        order_id=order.id, phone_number=payload.phone_number,
    )

    log_action(db, user_id=user_id, action="order.created", module="orders", resource="order", resource_id=str(order.id))
    return OrderPaymentIntentOut(order=OrderOut.model_validate(order), **extra)


def get_order(db, order_id: uuid.UUID, user_id: uuid.UUID, is_admin: bool = False) -> OrderOut:
    order = orders_repo.get_by_id(db, order_id)
    if order is None:
        raise NotFoundError("Commande introuvable.")
    if order.user_id != user_id and not is_admin:
        raise NotFoundError("Commande introuvable.")
    return OrderOut.model_validate(order)


def list_my_orders(db, user_id: uuid.UUID) -> list[OrderOut]:
    return [OrderOut.model_validate(o) for o in orders_repo.list_for_user(db, user_id)]


def update_order_status(db, order_id: uuid.UUID, status: str, actor_id: uuid.UUID) -> OrderOut:
    order = orders_repo.get_by_id(db, order_id)
    if order is None:
        raise NotFoundError("Commande introuvable.")
    order = orders_repo.update_status(db, order, status)
    log_action(db, user_id=actor_id, action="order.status_updated", module="orders", resource="order", resource_id=str(order_id), new_value={"status": status})
    return OrderOut.model_validate(order)
