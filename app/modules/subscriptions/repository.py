"""Accès aux données du domaine 'subscriptions' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan import Plan
from app.models.subscription import Subscription


def list_plans(db: Session) -> list[Plan]:
    return list(db.execute(select(Plan)).scalars().all())


def get_plan_by_code(db: Session, code: str) -> Plan | None:
    stmt = select(Plan).where(Plan.code == code)
    return db.execute(stmt).scalar_one_or_none()


def get_by_id(db: Session, subscription_id: uuid.UUID) -> Subscription | None:
    return db.get(Subscription, subscription_id)


def get_active_for_user(db: Session, user_id: uuid.UUID) -> Subscription | None:
    stmt = select(Subscription).where(Subscription.user_id == user_id, Subscription.status == "active").order_by(Subscription.created_at.desc())
    return db.execute(stmt).scalars().first()


def list_for_user(db: Session, user_id: uuid.UUID) -> list[Subscription]:
    stmt = select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def create(db: Session, subscription: Subscription) -> Subscription:
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def update(db: Session, subscription: Subscription, fields: dict) -> Subscription:
    for key, value in fields.items():
        setattr(subscription, key, value)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription
