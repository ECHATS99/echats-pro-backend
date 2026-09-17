"""Routes HTTP /api/v1/subscriptions."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.modules.subscriptions import service as subscriptions_service
from app.modules.subscriptions.schemas import PlanOut, SubscriptionCreate, SubscriptionOut, SubscriptionPaymentIntentOut

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/plans", response_model=list[PlanOut])
def list_plans(db: Session = Depends(get_db)):
    """Plans chargés dynamiquement depuis le backend (Partie 9 du SRS : rien en dur côté frontend)."""
    return subscriptions_service.list_plans(db)


@router.get("/me", response_model=SubscriptionOut | None)
def my_active_subscription(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return subscriptions_service.get_active_subscription(db, current.id)


@router.get("", response_model=list[SubscriptionOut])
def list_my_subscriptions(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return subscriptions_service.list_my_subscriptions(db, current.id)


@router.post("", response_model=SubscriptionPaymentIntentOut, status_code=201)
def subscribe(payload: SubscriptionCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return subscriptions_service.subscribe(db, payload, current.id)


@router.post("/{subscription_id}/cancel", response_model=SubscriptionOut)
def cancel(subscription_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return subscriptions_service.cancel_subscription(db, subscription_id, current.id)
