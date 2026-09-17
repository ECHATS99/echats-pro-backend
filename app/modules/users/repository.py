"""Accès aux données du domaine 'users' via SQLAlchemy. Seul endroit qui interroge la base
pour ce domaine.
"""
import uuid

from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session, selectinload

from app.models.user import User


def get_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    stmt = (
        select(User)
        .options(selectinload(User.roles), selectinload(User.subscriptions))
        .where(User.id == user_id, User.deleted_at.is_(None))
    )
    return db.execute(stmt).scalar_one_or_none()


def update_profile_fields(db: Session, user: User, fields: dict) -> User:
    """Applique les champs modifiables (username/country/city/language/timezone/bio).
    N'accepte jamais xp/level/role/plan ici : ces champs sont gérés par des services dédiés
    (xp_service, subscriptions, admin).
    """
    for key, value in fields.items():
        if value is not None:
            setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def search_users(db: Session, query: str, page: int, limit: int) -> tuple[list[User], int]:
    """Recherche paginée d'utilisateurs par username/email (partiel, insensible à la casse)."""
    filters = (
        User.deleted_at.is_(None),
        or_(User.username.ilike(f"%{query}%"), User.email.ilike(f"%{query}%")),
    )
    total = db.execute(select(func.count()).select_from(User).where(*filters)).scalar_one()
    stmt = select(User).where(*filters).order_by(User.username).offset((page - 1) * limit).limit(limit)
    results = db.execute(stmt).scalars().all()
    return list(results), total
