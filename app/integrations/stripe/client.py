"""Client bas niveau pour stripe. Création de paiement, gestion des webhooks."""
import stripe

from app.core.settings import settings
from app.integrations.stripe.exceptions import StripeError

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount: int, currency: str, metadata: dict) -> dict:
    """Crée un PaymentIntent Stripe. `amount` en unité la plus petite (centimes)."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount, currency=currency.lower(), metadata=metadata,
            automatic_payment_methods={"enabled": True},
        )
    except Exception as exc:
        raise StripeError(f"Échec de création du PaymentIntent Stripe : {exc}") from exc

    return {"id": intent["id"], "client_secret": intent["client_secret"], "status": intent["status"]}


def retrieve_payment_intent(payment_intent_id: str) -> dict:
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except Exception as exc:
        raise StripeError(f"Échec de récupération du PaymentIntent Stripe : {exc}") from exc
    return {"id": intent["id"], "status": intent["status"], "amount": intent["amount"], "currency": intent["currency"]}


def create_refund(payment_intent_id: str, amount: int | None = None) -> dict:
    try:
        refund = stripe.Refund.create(payment_intent=payment_intent_id, amount=amount)
    except Exception as exc:
        raise StripeError(f"Échec du remboursement Stripe : {exc}") from exc
    return {"id": refund["id"], "status": refund["status"]}


def construct_webhook_event(payload: bytes, sig_header: str):
    """Vérifie la signature du webhook Stripe (Partie 5 / 8 du SRS : ne jamais faire
    confiance à un webhook non signé).
    """
    try:
        return stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception as exc:
        raise StripeError(f"Signature webhook Stripe invalide : {exc}") from exc
