"""Routes HTTP /api/v1/orders."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.dependencies.permissions import require_permission
from app.modules.orders import service as orders_service
from app.modules.orders.schemas import OrderCreate, OrderOut, OrderPaymentIntentOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
def list_my_orders(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return orders_service.list_my_orders(db, current.id)


@router.post("", response_model=OrderPaymentIntentOut, status_code=201)
def create_order(payload: OrderCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return orders_service.create_order(db, payload, current.id)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: uuid.UUID, current: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    is_admin = current.primary_role_name in ("admin", "super_admin")
    return orders_service.get_order(db, order_id, current.id, is_admin)


@router.patch("/{order_id}", response_model=OrderOut)
def update_status(order_id: uuid.UUID, status: str, current: CurrentUser = Depends(require_permission("payments.manage")), db: Session = Depends(get_db)):
    return orders_service.update_order_status(db, order_id, status, current.id)
