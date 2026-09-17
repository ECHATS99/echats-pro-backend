"""Accès aux données du domaine 'orders' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderItem


def get_by_id(db: Session, order_id: uuid.UUID) -> Order | None:
    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    return db.execute(stmt).scalar_one_or_none()


def list_for_user(db: Session, user_id: uuid.UUID) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.items)).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def create(db: Session, order: Order) -> Order:
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_status(db: Session, order: Order, status: str) -> Order:
    order.status = status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
