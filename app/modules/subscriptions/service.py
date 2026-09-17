"""Logique métier du domaine 'subscriptions'. Plans (GO/CORE_I/PARABEN/CHAMBRE_CLOSE),
cycle de vie des abonnements, quotas associés. Ne contient aucune requête SQL directe :
passe par repository.py.
"""
import uuid
from datetime import datetime, timedelta, timezone

from app.core.exceptions import NotFoundError
from app.models.subscription import Subscription
from app.modules.subscriptions import repository as subscriptions_repo
from app.modules.subscriptions.schemas import (
    PlanOut, SubscriptionCreate, SubscriptionOut, SubscriptionPaymentIntentOut,
)
from app.services.audit_service import log_action


def list_plans(db) -> list[PlanOut]:
    return [PlanOut.model_validate(p) for p in subscriptions_repo.list_plans(db)]


def subscribe(db, payload: SubscriptionCreate, user_id: uuid.UUID) -> SubscriptionPaymentIntentOut:
    """Crée un abonnement en statut 'pending' et initie le paiement correspondant.
    L'abonnement passe à 'active' uniquement via `activate_subscription`, déclenché par la
    confirmation réelle du paiement (webhook), jamais directement par ce endpoint.
    """
    plan = subscriptions_repo.get_plan_by_code(db, payload.plan_code)
    if plan is None:
        raise NotFoundError("Plan introuvable.")

    subscription = subscriptions_repo.create(db, Subscription(user_id=user_id, plan_id=plan.id, status="pending", payment_provider=payload.payment_provider))

    from app.modules.payments import service as payments_service
    amount_cents = int(float(plan.price) * 100)
    payment, extra = payments_service.initiate_payment(
        db, user_id=user_id, amount=amount_cents, currency=plan.currency, provider=payload.payment_provider,
        subscription_id=subscription.id, phone_number=payload.phone_number,
    )

    log_action(db, user_id=user_id, action="subscription.initiated", module="subscriptions", resource="subscription", resource_id=str(subscription.id))
    return SubscriptionPaymentIntentOut(subscription=SubscriptionOut.model_validate(subscription), **extra)


def activate_subscription(db, subscription_id: uuid.UUID) -> Subscription | None:
    """Active un abonnement suite à confirmation de paiement. Met aussi à jour le rôle
    utilisateur si le plan correspond au tier Paraben (Partie 3 du SRS)."""
    subscription = subscriptions_repo.get_by_id(db, subscription_id)
    if subscription is None:
        return None

    now = datetime.now(timezone.utc)
    plan = subscription.plan
    expires_at = now + timedelta(days=plan.duration_days) if plan.duration_days else None

    subscription = subscriptions_repo.update(db, subscription, {"status": "active", "starts_at": now, "expires_at": expires_at})

    if plan.code == "PARABEN_NIVEAU_1":
        _record_paraben_revenue_split(db, subscription)

    log_action(db, user_id=subscription.user_id, action="subscription.activated", module="subscriptions", resource="subscription", resource_id=str(subscription.id))
    return subscription


def _record_paraben_revenue_split(db, subscription: Subscription) -> None:
    """Trace le partage 50/50 des revenus Paraben (Partie 6 du SRS)."""
    from app.models.paraben import ParabenRevenue
    from app.utils.date import to_period_str

    amount = int(float(subscription.plan.price) * 100)
    half = amount // 2
    db.add(ParabenRevenue(
        subscription_id=subscription.id, amount=amount,
        echats_share=amount - half, paraben_share=half, period=to_period_str(),
    ))
    db.commit()


def list_my_subscriptions(db, user_id: uuid.UUID) -> list[SubscriptionOut]:
    return [SubscriptionOut.model_validate(s) for s in subscriptions_repo.list_for_user(db, user_id)]


def get_active_subscription(db, user_id: uuid.UUID) -> SubscriptionOut | None:
    subscription = subscriptions_repo.get_active_for_user(db, user_id)
    return SubscriptionOut.model_validate(subscription) if subscription else None


def cancel_subscription(db, subscription_id: uuid.UUID, user_id: uuid.UUID) -> SubscriptionOut:
    subscription = subscriptions_repo.get_by_id(db, subscription_id)
    if subscription is None or subscription.user_id != user_id:
        raise NotFoundError("Abonnement introuvable.")
    subscription = subscriptions_repo.update(db, subscription, {"status": "cancelled", "renewal": False})
    log_action(db, user_id=user_id, action="subscription.cancelled", module="subscriptions", resource="subscription", resource_id=str(subscription_id))
    return SubscriptionOut.model_validate(subscription)
