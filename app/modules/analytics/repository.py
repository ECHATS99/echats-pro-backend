"""Accès aux données du domaine 'analytics' via SQLAlchemy (agrégations lourdes — Partie 7.5 du SRS ;
migrable vers un worker analytics_worker si le volume l'exige)."""
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ctf import CTFChallenge, CTFSolve
from app.models.lesson import Lesson
from app.models.order import Order
from app.models.payment import Payment
from app.models.progress import UserProgress
from app.models.subscription import Subscription
from app.models.track import Track
from app.models.user import User


def counts_overview(db: Session) -> dict:
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return {
        "total_users": db.execute(select(func.count()).select_from(User)).scalar_one(),
        "active_users_30d": db.execute(select(func.count()).select_from(User).where(User.last_login >= thirty_days_ago)).scalar_one(),
        "total_tracks": db.execute(select(func.count()).select_from(Track)).scalar_one(),
        "total_ctf_challenges": db.execute(select(func.count()).select_from(CTFChallenge)).scalar_one(),
        "total_ctf_solves": db.execute(select(func.count()).select_from(CTFSolve)).scalar_one(),
        "total_revenue_fcfa": db.execute(select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.status == "succeeded")).scalar_one(),
        "total_orders": db.execute(select(func.count()).select_from(Order)).scalar_one(),
        "active_subscriptions": db.execute(select(func.count()).select_from(Subscription).where(Subscription.status == "active")).scalar_one(),
    }


def users_by_role(db: Session) -> dict[str, int]:
    from app.models.role_permission import Role, user_roles
    stmt = select(Role.name, func.count(user_roles.c.user_id)).join(user_roles, user_roles.c.role_id == Role.id).group_by(Role.name)
    return {name: count for name, count in db.execute(stmt).all()}


def users_by_country(db: Session) -> dict[str, int]:
    stmt = select(User.country, func.count(User.id)).where(User.country.is_not(None)).group_by(User.country)
    return {country: count for country, count in db.execute(stmt).all()}


def new_users_last_30d(db: Session) -> int:
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return db.execute(select(func.count()).select_from(User).where(User.created_at >= thirty_days_ago)).scalar_one()


def average_completion_rate(db: Session) -> float:
    total = db.execute(select(func.count()).select_from(UserProgress)).scalar_one()
    if total == 0:
        return 0.0
    completed = db.execute(select(func.count()).select_from(UserProgress).where(UserProgress.completed.is_(True))).scalar_one()
    return round((completed / total) * 100, 2)


def payments_by_provider(db: Session) -> dict[str, int]:
    stmt = select(Payment.provider, func.count(Payment.id)).where(Payment.status == "succeeded").group_by(Payment.provider)
    return {provider: count for provider, count in db.execute(stmt).all()}


def top_ctf_challenges(db: Session, limit: int = 5) -> list[str]:
    stmt = (
        select(CTFChallenge.title, func.count(CTFSolve.id).label("solves"))
        .join(CTFSolve, CTFSolve.challenge_id == CTFChallenge.id)
        .group_by(CTFChallenge.title).order_by(func.count(CTFSolve.id).desc()).limit(limit)
    )
    return [title for title, _ in db.execute(stmt).all()]
