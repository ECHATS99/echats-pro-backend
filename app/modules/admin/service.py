"""Logique métier du domaine 'admin'. Paramètres globaux, feature flags, messages système,
maintenance. Toutes les actions sont auditées (Partie 4.20 du SRS)."""
import uuid

from app.models.admin_settings import SystemMessage
from app.modules.admin import repository as admin_repo
from app.modules.admin.schemas import (
    AdminSettingOut, AdminSettingUpdate, FeatureFlagOut, FeatureFlagUpdate,
    MaintenanceUpdate, SystemMessageCreate, SystemMessageOut,
)
from app.services.audit_service import log_action
from app.services.cache_service import cache_delete_prefix


def get_all_settings(db) -> list[AdminSettingOut]:
    return [AdminSettingOut.model_validate(s) for s in admin_repo.list_settings(db)]


def update_setting(db, payload: AdminSettingUpdate, actor_id: uuid.UUID) -> AdminSettingOut:
    setting = admin_repo.upsert_setting(db, payload.key, payload.value)
    log_action(db, user_id=actor_id, action="admin.setting_updated", module="admin", resource="setting", resource_id=payload.key, new_value={"value": payload.value})
    return AdminSettingOut.model_validate(setting)


def list_feature_flags(db) -> list[FeatureFlagOut]:
    return [FeatureFlagOut.model_validate(f) for f in admin_repo.list_flags(db)]


def update_feature_flag(db, payload: FeatureFlagUpdate, actor_id: uuid.UUID) -> FeatureFlagOut:
    flag = admin_repo.upsert_flag(db, payload.key, payload.enabled, payload.description)
    log_action(db, user_id=actor_id, action="admin.feature_flag_updated", module="admin", resource="feature_flag", resource_id=payload.key, new_value={"enabled": payload.enabled})
    return FeatureFlagOut.model_validate(flag)


def create_system_message(db, payload: SystemMessageCreate, actor_id: uuid.UUID) -> SystemMessageOut:
    message = admin_repo.create_message(db, SystemMessage(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="admin.system_message_created", module="admin", resource="system_message", resource_id=str(message.id))
    return SystemMessageOut.model_validate(message)


def list_active_system_messages(db) -> list[SystemMessageOut]:
    return [SystemMessageOut.model_validate(m) for m in admin_repo.list_active_messages(db)]


def set_maintenance(db, payload: MaintenanceUpdate, actor_id: uuid.UUID) -> dict:
    window = admin_repo.upsert_maintenance(db, payload.active, payload.message)
    cache_delete_prefix("leaderboard:")  # évite un état de cache incohérent pendant la maintenance
    log_action(db, user_id=actor_id, action="admin.maintenance_toggled", module="admin", resource="maintenance", new_value={"active": payload.active})
    return {"active": window.active, "message": window.message}


def list_application_logs(module: str | None) -> dict:
    """Les logs applicatifs bruts (fichiers logs/*.log) ne sont pas exposés tels quels via
    l'API pour des raisons de sécurité (Partie 8.13 du SRS : jamais de secrets en clair dans
    les réponses API). Utiliser /admin/audit pour la traçabilité structurée en base.
    """
    return {"message": "Consultez /api/v1/admin/audit pour les journaux structurés. Les fichiers logs bruts ne sont pas exposés via l'API.", "module_filter": module}
