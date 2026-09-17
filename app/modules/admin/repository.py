"""Accès aux données du domaine 'admin' via SQLAlchemy."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin_settings import AdminSetting, FeatureFlag, MaintenanceWindow, SystemMessage


def list_settings(db: Session) -> list[AdminSetting]:
    return list(db.execute(select(AdminSetting)).scalars().all())


def upsert_setting(db: Session, key: str, value: str) -> AdminSetting:
    stmt = select(AdminSetting).where(AdminSetting.key == key)
    setting = db.execute(stmt).scalar_one_or_none()
    if setting is None:
        setting = AdminSetting(key=key, value=value)
    else:
        setting.value = value
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def list_flags(db: Session) -> list[FeatureFlag]:
    return list(db.execute(select(FeatureFlag)).scalars().all())


def upsert_flag(db: Session, key: str, enabled: bool, description: str | None) -> FeatureFlag:
    stmt = select(FeatureFlag).where(FeatureFlag.key == key)
    flag = db.execute(stmt).scalar_one_or_none()
    if flag is None:
        flag = FeatureFlag(key=key, enabled=enabled, description=description)
    else:
        flag.enabled = enabled
        if description is not None:
            flag.description = description
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return flag


def create_message(db: Session, message: SystemMessage) -> SystemMessage:
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_active_messages(db: Session) -> list[SystemMessage]:
    stmt = select(SystemMessage).where(SystemMessage.active.is_(True)).order_by(SystemMessage.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def get_maintenance(db: Session) -> MaintenanceWindow | None:
    return db.execute(select(MaintenanceWindow)).scalars().first()


def upsert_maintenance(db: Session, active: bool, message: str | None) -> MaintenanceWindow:
    window = get_maintenance(db)
    if window is None:
        window = MaintenanceWindow(active=active, message=message)
    else:
        window.active = active
        window.message = message
    db.add(window)
    db.commit()
    db.refresh(window)
    return window
