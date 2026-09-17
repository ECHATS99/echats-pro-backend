"""Routes HTTP /api/v1/payments."""
import uuid

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.payments import service as payments_service
from app.modules.payments.schemas import PaymentOut, RefundRequest

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/history", response_model=list[PaymentOut])
def history(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return payments_service.list_my_payments(db, current.id)


@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default=""), db: Session = Depends(get_db)):
    """Point d'entrée unique des webhooks Stripe. La signature est vérifiée avant tout
    traitement (Partie 8.11 du SRS : ne jamais faire confiance à un webhook non signé).
    """
    payload = await request.body()
    return payments_service.handle_stripe_webhook(db, payload, stripe_signature)


@router.post("/refund", response_model=PaymentOut)
def refund(
    payment_id: uuid.UUID, payload: RefundRequest,
    current: CurrentUser = Depends(require_permission("payments.refund")),
    db: Session = Depends(get_db),
):
    return payments_service.refund_payment(db, payment_id, current.id, payload.amount)
