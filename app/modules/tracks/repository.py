"""Accès aux données du domaine 'tracks'."""
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.models.track import Track


def get_by_id(db: Session, track_id: uuid.UUID) -> Track | None:
    stmt = (
        select(Track)
        .options(selectinload(Track.modules))
        .where(Track.id == track_id, Track.deleted_at.is_(None))
    )
    return db.execute(stmt).scalar_one_or_none()


def get_by_slug(db: Session, slug: str) -> Track | None:
    stmt = select(Track).where(Track.slug == slug, Track.deleted_at.is_(None))
    return db.execute(stmt).scalar_one_or_none()


def slug_exists(db: Session, slug: str) -> bool:
    stmt = select(func.count()).select_from(Track).where(Track.slug == slug)
    return db.execute(stmt).scalar_one() > 0


def list_tracks(
    db: Session, page: int, limit: int, *, difficulty: str | None = None,
    domain: str | None = None, published_only: bool = True,
) -> tuple[list[Track], int]:
    filters = [Track.deleted_at.is_(None)]
    if published_only:
        filters.append(Track.published.is_(True))
    if difficulty:
        filters.append(Track.difficulty == difficulty)
    if domain:
        filters.append(Track.domain == domain)

    total = db.execute(select(func.count()).select_from(Track).where(*filters)).scalar_one()
    stmt = (
        select(Track).where(*filters)
        .order_by(Track.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    results = db.execute(stmt).scalars().all()
    return list(results), total


def create(db: Session, track: Track) -> Track:
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


def update(db: Session, track: Track, fields: dict) -> Track:
    for key, value in fields.items():
        setattr(track, key, value)
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


def soft_delete(db: Session, track: Track) -> None:
    from app.utils.date import utcnow
    track.deleted_at = utcnow()
    db.add(track)
    db.commit()
