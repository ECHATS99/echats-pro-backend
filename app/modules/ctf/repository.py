"""Accès aux données du domaine 'ctf' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ctf import CTFCategory, CTFChallenge, CTFEvent, CTFSolve
from app.models.user import User


def list_events(db: Session) -> list[CTFEvent]:
    return list(db.execute(select(CTFEvent).order_by(CTFEvent.start.desc())).scalars().all())


def list_categories(db: Session) -> list[CTFCategory]:
    return list(db.execute(select(CTFCategory).order_by(CTFCategory.name)).scalars().all())


def get_challenge(db: Session, challenge_id: uuid.UUID) -> CTFChallenge | None:
    return db.get(CTFChallenge, challenge_id)


def list_challenges(db: Session, *, category_id: uuid.UUID | None = None, event_id: uuid.UUID | None = None, published_only: bool = True) -> list[CTFChallenge]:
    filters = []
    if published_only:
        filters.append(CTFChallenge.published.is_(True))
    if category_id:
        filters.append(CTFChallenge.category_id == category_id)
    if event_id:
        filters.append(CTFChallenge.event_id == event_id)
    stmt = select(CTFChallenge).where(*filters).order_by(CTFChallenge.points)
    return list(db.execute(stmt).scalars().all())


def create_challenge(db: Session, challenge: CTFChallenge) -> CTFChallenge:
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def update_challenge(db: Session, challenge: CTFChallenge, fields: dict) -> CTFChallenge:
    for key, value in fields.items():
        setattr(challenge, key, value)
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def delete_challenge(db: Session, challenge: CTFChallenge) -> None:
    db.delete(challenge)
    db.commit()


def has_solved(db: Session, user_id: uuid.UUID, challenge_id: uuid.UUID) -> bool:
    stmt = select(CTFSolve).where(CTFSolve.user_id == user_id, CTFSolve.challenge_id == challenge_id)
    return db.execute(stmt).scalar_one_or_none() is not None


def solved_challenge_ids_for_user(db: Session, user_id: uuid.UUID) -> set[uuid.UUID]:
    stmt = select(CTFSolve.challenge_id).where(CTFSolve.user_id == user_id)
    return set(db.execute(stmt).scalars().all())


def record_solve(db: Session, user_id: uuid.UUID, challenge_id: uuid.UUID, points: int) -> CTFSolve:
    solve = CTFSolve(user_id=user_id, challenge_id=challenge_id, points=points)
    db.add(solve)
    db.commit()
    db.refresh(solve)
    return solve


def user_solve_count(db: Session, user_id: uuid.UUID) -> int:
    stmt = select(func.count()).select_from(CTFSolve).where(CTFSolve.user_id == user_id)
    return db.execute(stmt).scalar_one()


def leaderboard(db: Session, limit: int = 50) -> list[tuple]:
    stmt = (
        select(User.id, User.username, func.coalesce(func.sum(CTFSolve.points), 0).label("total_points"), func.count(CTFSolve.id).label("solves_count"))
        .join(CTFSolve, CTFSolve.user_id == User.id)
        .group_by(User.id, User.username)
        .order_by(func.sum(CTFSolve.points).desc())
        .limit(limit)
    )
    return list(db.execute(stmt).all())
