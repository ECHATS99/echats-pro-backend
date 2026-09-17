"""Accès aux données du domaine 'news' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.news import NewsArticle


def list_news(db: Session, page: int, limit: int, category: str | None = None) -> tuple[list[NewsArticle], int]:
    filters = []
    if category:
        filters.append(NewsArticle.category == category)
    total = db.execute(select(func.count()).select_from(NewsArticle).where(*filters)).scalar_one()
    stmt = select(NewsArticle).where(*filters).order_by(NewsArticle.published_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total


def list_latest(db: Session, limit: int = 10) -> list[NewsArticle]:
    stmt = select(NewsArticle).order_by(NewsArticle.published_at.desc()).limit(limit)
    return list(db.execute(stmt).scalars().all())
