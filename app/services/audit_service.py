"""Écriture centralisée dans audit_logs pour toute action sensible (Partie 4.15 / 7.7 du SRS)."""
import uuid

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    user_id: uuid.UUID | None,
    action: str,
    module: str | None = None,
    role: str | None = None,
    resource: str | None = None,
    resource_id: str | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    country: str | None = None,
) -> None:
    """Insère une ligne d'audit. Ne lève jamais d'exception bloquante pour l'action métier
    principale : une erreur d'audit ne doit pas empêcher l'action utilisateur (best effort),
    mais elle est tout de même journalisée via les logs applicatifs.
    """
    try:
        entry = AuditLog(
            user_id=user_id,
            role=role,
            action=action,
            module=module,
            resource=resource,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
            country=country,
        )
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()
        import logging
        logging.getLogger("echats.audit").exception("Échec de journalisation d'audit pour action=%s", action)
