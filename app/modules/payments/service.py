"""Logique métier du domaine 'payments' : dispatch multi-fournisseur (Stripe/PayPal/Mobile Money),
webhooks, remboursements. C'est le SEUL module qui parle directement aux intégrations de paiement.
"""
import uuid

from app.core.exceptions import NotFoundError, ValidationError
from app.integrations.mobile_money.client import request_payment as mm_request_payment
from app.integrations.paypal.client import create_order as paypal_create_order
from app.integrations.stripe.client import construct_webhook_event, create_payment_intent, create_refund
from app.models.payment import Payment
from app.modules.payments import repository as payments_repo
from app.modules.payments.schemas import PaymentOut
from app.services.audit_service import log_action


def initiate_payment(db, *, user_id: uuid.UUID, amount: int, currency: str, provider: str,
                      order_id: uuid.UUID | None = None, subscription_id: uuid.UUID | None = None,
                      phone_number: str | None = None) -> tuple[Payment, dict]:
    """Crée l'enregistrement Payment (statut 'pending') et initie la transaction chez le
    fournisseur choisi. Retourne (payment, extra) où `extra` contient les champs nécessaires
    au frontend pour finaliser (client_secret Stripe, approval_url PayPal, transaction_id MM).
    """
    payment = payments_repo.create(db, Payment(
        user_id=user_id, order_id=order_id, subscription_id=subscription_id,
        provider=provider, currency=currency, amount=amount, status="pending",
    ))

    extra: dict = {}
    reference = str(order_id or subscription_id or payment.id)

    if provider == "stripe":
        intent = create_payment_intent(amount, currency, {"payment_id": str(payment.id), "reference": reference})
        payments_repo.update_status(db, payment, "pending", transaction_id=intent["id"])
        extra["client_secret"] = intent["client_secret"]

    elif provider == "paypal":
        amount_str = f"{amount / 100:.2f}"
        order = paypal_create_order(amount_str, currency, reference)
        payments_repo.update_status(db, payment, "pending", transaction_id=order["id"])
        approval = next((l["href"] for l in order.get("links", []) if l.get("rel") == "approve"), None)
        extra["approval_url"] = approval

    elif provider in ("mtn", "airtel", "wave"):
        if not phone_number:
            raise ValidationError("Un numéro de téléphone est requis pour Mobile Money.")
        result = mm_request_payment(provider, phone_number, amount, currency, reference)
        payments_repo.update_status(db, payment, "pending", transaction_id=result["transaction_id"])
        extra["transaction_id"] = result["transaction_id"]

    else:
        raise ValidationError(f"Fournisseur de paiement inconnu : {provider}")

    return payment, extra


def mark_succeeded(db, transaction_id: str) -> Payment | None:
    payment = payments_repo.get_by_transaction_id(db, transaction_id)
    if payment is None:
        return None
    payment = payments_repo.update_status(db, payment, "succeeded")
    log_action(db, user_id=payment.user_id, action="payment.succeeded", module="payments", resource="payment", resource_id=str(payment.id))

    if payment.subscription_id:
        from app.modules.subscriptions import service as subscriptions_service
        subscriptions_service.activate_subscription(db, payment.subscription_id)
    elif payment.order_id:
        from app.modules.orders import repository as orders_repo
        order = orders_repo.get_by_id(db, payment.order_id)
        if order:
            orders_repo.update_status(db, order, "paid")

    return payment


def mark_failed(db, transaction_id: str) -> Payment | None:
    payment = payments_repo.get_by_transaction_id(db, transaction_id)
    if payment is None:
        return None
    payment = payments_repo.update_status(db, payment, "failed")
    log_action(db, user_id=payment.user_id, action="payment.failed", module="payments", resource="payment", resource_id=str(payment.id))
    return payment


def handle_stripe_webhook(db, payload: bytes, sig_header: str) -> dict:
    event = construct_webhook_event(payload, sig_header)
    event_type = event["type"]
    intent = event["data"]["object"]

    if event_type == "payment_intent.succeeded":
        mark_succeeded(db, intent["id"])
    elif event_type in ("payment_intent.payment_failed", "payment_intent.canceled"):
        mark_failed(db, intent["id"])

    return {"received": True}


def refund_payment(db, payment_id: uuid.UUID, actor_id: uuid.UUID, amount: int | None = None) -> PaymentOut:
    payment = payments_repo.get_by_id(db, payment_id)
    if payment is None:
        raise NotFoundError("Paiement introuvable.")
    if payment.status != "succeeded":
        raise ValidationError("Seul un paiement réussi peut être remboursé.")

    if payment.provider == "stripe" and payment.transaction_id:
        create_refund(payment.transaction_id, amount)

    payment = payments_repo.update_status(db, payment, "refunded")
    log_action(db, user_id=actor_id, action="payment.refunded", module="payments", resource="payment", resource_id=str(payment.id))
    return PaymentOut.model_validate(payment)


def list_my_payments(db, user_id: uuid.UUID) -> list[PaymentOut]:
    return [PaymentOut.model_validate(p) for p in payments_repo.list_for_user(db, user_id)]
