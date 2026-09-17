"""Accès aux données du domaine 'auth' via SQLAlchemy. Seul endroit qui interroge la base
pour ce domaine (auto-provisioning, rôle par défaut, plan par défaut, mise à jour de session)."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.constants import DEFAULT_ROLE_ON_REGISTER, DEFAULT_PLAN_ON_REGISTER
from app.models.plan import Plan
from app.models.role_permission import Role
from app.models.subscription import Subscription
from app.models.user import User


def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> User | None:
    """Recherche un utilisateur par son firebase_uid, avec ses rôles préchargés."""
    stmt = (
        select(User)
        .options(selectinload(User.roles), selectinload(User.subscriptions))
        .where(User.firebase_uid == firebase_uid, User.deleted_at.is_(None))
    )
    return db.execute(stmt).scalar_one_or_none()


def _generate_unique_username(db: Session, email: str) -> str:
    base = email.split("@")[0].lower()
    base = "".join(c for c in base if c.isalnum() or c == "_") or "user"
    candidate = base
    suffix = 0
    while db.execute(select(User).where(User.username == candidate)).scalar_one_or_none():
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


def create_user_from_firebase(db: Session, firebase_uid: str, email: str) -> User:
    """Auto-provisioning au premier accès (Partie 4.4 du SRS) :
    crée le compte, attribue le rôle 'student' et le plan 'GO' par défaut.
    """
    default_role = db.execute(
        select(Role).where(Role.name == DEFAULT_ROLE_ON_REGISTER.value)
    ).scalar_one_or_none()
    if default_role is None:
        # Le rôle par défaut doit être seedé (scripts/seed.py) avant le premier login.
        raise RuntimeError(
            f"Rôle par défaut '{DEFAULT_ROLE_ON_REGISTER.value}' introuvable — exécutez scripts/seed.py"
        )

    user = User(
        id=uuid.uuid4(),
        firebase_uid=firebase_uid,
        email=email,
        username=_generate_unique_username(db, email),
        status="active",
    )
    user.roles.append(default_role)
    db.add(user)
    db.flush()  # pour obtenir user.id avant de créer l'abonnement

    default_plan = db.execute(
        select(Plan).where(Plan.code == DEFAULT_PLAN_ON_REGISTER.value)
    ).scalar_one_or_none()
    if default_plan is not None:
        db.add(Subscription(
            id=uuid.uuid4(),
            user_id=user.id,
            plan_id=default_plan.id,
            status="active",
            payment_provider=None,
            starts_at=datetime.now(timezone.utc),
            expires_at=None,
        ))

    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user: User, ip_address: str | None) -> None:
    """Met à jour la date/IP de dernière connexion."""
    user.last_login = datetime.now(timezone.utc)
    user.last_login_ip = ip_address
    db.add(user)
    db.commit()
