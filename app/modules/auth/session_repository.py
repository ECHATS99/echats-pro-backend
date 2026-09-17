"""Persistance des sessions de refresh token."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.refresh_session import RefreshSession


def create(
    db: Session,
    *,
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    token_hash: str,
    expires_at: datetime,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> RefreshSession:
    session = RefreshSession(
        user_id=user_id,
        session_id=session_id,
        token_hash=token_hash,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_by_session_id(db: Session, session_id: uuid.UUID) -> RefreshSession | None:
    return db.execute(
        select(RefreshSession).where(RefreshSession.session_id == session_id)
    ).scalar_one_or_none()


def get_by_session_id_for_update(db: Session, session_id: uuid.UUID) -> RefreshSession | None:
    """Verrouille la ligne jusqu'au commit de la rotation."""
    return db.execute(
        select(RefreshSession)
        .where(RefreshSession.session_id == session_id)
        .with_for_update()
    ).scalar_one_or_none()


def revoke(
    db: Session,
    session: RefreshSession,
    *,
    replaced_by_session_id: uuid.UUID | None = None,
) -> None:
    session.revoked_at = datetime.now(timezone.utc)
    session.replaced_by_session_id = replaced_by_session_id
    session.last_used_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()


def revoke_all(db: Session, user_id: uuid.UUID) -> None:
    db.execute(
        update(RefreshSession)
        .where(RefreshSession.user_id == user_id, RefreshSession.revoked_at.is_(None))
        .values(revoked_at=datetime.now(timezone.utc))
    )
    db.commit()
