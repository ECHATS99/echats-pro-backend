"""Accès aux données du domaine 'search' via SQLAlchemy (recherche full-text simple ILIKE ;
migrable vers un index dédié — MongoDB `search_history`/Elastic — si le volume l'exige)."""
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.ctf import CTFChallenge
from app.models.product import Product
from app.models.track import Track
from app.models.user import User

SEARCH_LIMIT = 10


def search_tracks(db: Session, q: str) -> list[Track]:
    stmt = select(Track).where(Track.published.is_(True), Track.title.ilike(f"%{q}%")).limit(SEARCH_LIMIT)
    return list(db.execute(stmt).scalars().all())


def search_ctf(db: Session, q: str) -> list[CTFChallenge]:
    stmt = select(CTFChallenge).where(CTFChallenge.published.is_(True), CTFChallenge.title.ilike(f"%{q}%")).limit(SEARCH_LIMIT)
    return list(db.execute(stmt).scalars().all())


def search_products(db: Session, q: str) -> list[Product]:
    stmt = select(Product).where(Product.available.is_(True), Product.name.ilike(f"%{q}%")).limit(SEARCH_LIMIT)
    return list(db.execute(stmt).scalars().all())


def search_users(db: Session, q: str) -> list[User]:
    stmt = select(User).where(or_(User.username.ilike(f"%{q}%"), User.email.ilike(f"%{q}%"))).limit(SEARCH_LIMIT)
    return list(db.execute(stmt).scalars().all())
