"""Logique métier du domaine 'audit'. Consultation paginée, filtrable, réservée aux admins."""
import uuid

from app.modules.audit import repository as audit_repo
from app.modules.audit.schemas import AuditLogOut
from app.utils.pagination import paginate


def list_logs(db, page: int, limit: int, module: str | None, action: str | None, user_id: uuid.UUID | None):
    items, total = audit_repo.list_logs(db, page, limit, module=module, action=action, user_id=user_id)
    return paginate([AuditLogOut.model_validate(i).model_dump() for i in items], page, limit, total)
