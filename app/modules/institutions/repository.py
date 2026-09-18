"""Accès base de données pour institutions."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.institution import Institution
from app.models.institution_access_key import InstitutionAccessKey
from app.models.user import User


def list_institutions(db: Session) -> list[Institution]:
    stmt = select(Institution).where(Institution.active.is_(True)).order_by(Institution.created_at)
    return list(db.execute(stmt).scalars().all())


def get_institution(db: Session, inst_id: uuid.UUID) -> Institution | None:
    return db.get(Institution, inst_id)


def get_by_slug_or_code(db: Session, value: str) -> Institution | None:
    stmt = select(Institution).where(
        (Institution.slug == value) | (Institution.code == value)
    )
    return db.execute(stmt).scalar_one_or_none()


def create_institution(db: Session, data: dict) -> Institution:
    inst = Institution(**data)
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


def update_institution(db: Session, inst: Institution, fields: dict) -> Institution:
    for k, v in fields.items():
        if hasattr(inst, k):
            setattr(inst, k, v)
    db.add(inst)
    db.commit()
    db.refresh(inst)
    return inst


def count_members(db: Session, inst_id: uuid.UUID) -> int:
    return db.execute(
        select(func.count()).select_from(User).where(User.institution_id == inst_id)
    ).scalar_one()


def increment_visitors(db: Session, inst: Institution) -> None:
    inst.visitors_count = (inst.visitors_count or 0) + 1
    db.add(inst)
    db.commit()


# --- Access Keys ---
def create_access_key(db: Session, data: dict) -> InstitutionAccessKey:
    k = InstitutionAccessKey(**data)
    db.add(k)
    db.commit()
    db.refresh(k)
    return k


def get_access_key_by_value(db: Session, key: str) -> InstitutionAccessKey | None:
    stmt = select(InstitutionAccessKey).where(InstitutionAccessKey.key == key)
    return db.execute(stmt).scalar_one_or_none()


def list_access_keys(db: Session, inst_id: uuid.UUID) -> list[InstitutionAccessKey]:
    stmt = select(InstitutionAccessKey).where(
        InstitutionAccessKey.institution_id == inst_id
    ).order_by(InstitutionAccessKey.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def revoke_access_key(db: Session, k: InstitutionAccessKey) -> None:
    k.is_active = False
    db.add(k)
    db.commit()


def key_exists(db: Session, key: str) -> bool:
    return db.execute(
        select(InstitutionAccessKey).where(InstitutionAccessKey.key == key)
    ).scalar_one_or_none() is not None


def consume_key_use(db: Session, k: InstitutionAccessKey) -> None:
    k.current_uses += 1
    if k.current_uses >= k.max_uses:
        k.is_active = False
    db.add(k)
    db.commit()
