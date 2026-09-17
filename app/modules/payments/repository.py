"""Accès aux données du domaine 'payments' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


def get_by_id(db: Session, payment_id: uuid.UUID) -> Payment | None:
    return db.get(Payment, payment_id)


def get_by_transaction_id(db: Session, transaction_id: str) -> Payment | None:
    stmt = select(Payment).where(Payment.transaction_id == transaction_id)
    return db.execute(stmt).scalar_one_or_none()


def list_for_user(db: Session, user_id: uuid.UUID) -> list[Payment]:
    stmt = select(Payment).where(Payment.user_id == user_id).order_by(Payment.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def create(db: Session, payment: Payment) -> Payment:
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def update_status(db: Session, payment: Payment, status: str, transaction_id: str | None = None) -> Payment:
    payment.status = status
    if transaction_id:
        payment.transaction_id = transaction_id
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
