"""Accès aux données du domaine 'audit' via SQLAlchemy. Lecture seule : aucun audit n'est
jamais supprimé (Partie 7.7 du SRS)."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def list_logs(db: Session, page: int, limit: int, *, module: str | None = None, action: str | None = None, user_id=None) -> tuple[list[AuditLog], int]:
    filters = []
    if module:
        filters.append(AuditLog.module == module)
    if action:
        filters.append(AuditLog.action == action)
    if user_id:
        filters.append(AuditLog.user_id == user_id)

    total = db.execute(select(func.count()).select_from(AuditLog).where(*filters)).scalar_one()
    stmt = select(AuditLog).where(*filters).order_by(AuditLog.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(db.execute(stmt).scalars().all()), total
