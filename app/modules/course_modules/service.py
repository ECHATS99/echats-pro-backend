"""Logique métier du domaine 'modules'."""
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.course_module import CourseModule
from app.modules.course_modules import repository as modules_repo
from app.modules.course_modules.schemas import CourseModuleCreate, CourseModuleOut, CourseModuleUpdate
from app.modules.tracks import repository as tracks_repo
from app.services.audit_service import log_action
from app.services.cache_service import cache_delete_prefix, cache_get, cache_set

CACHE_TTL_SECONDS = 300


def list_modules_for_track(db: Session, track_id: uuid.UUID) -> list[CourseModuleOut]:
    cache_key = f"modules:by_track:{track_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return [CourseModuleOut.model_validate(m) for m in cached]
    if tracks_repo.get_by_id(db, track_id) is None:
        raise NotFoundError("Track introuvable.")
    result = [CourseModuleOut.model_validate(m) for m in modules_repo.list_by_track(db, track_id)]
    cache_set(cache_key, [m.model_dump(mode="json") for m in result], ttl=CACHE_TTL_SECONDS)
    return result


def get_module(db: Session, module_id: uuid.UUID) -> CourseModuleOut:
    cache_key = f"modules:by_id:{module_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return CourseModuleOut.model_validate(cached)
    module = modules_repo.get_by_id(db, module_id)
    if module is None:
        raise NotFoundError("Module introuvable.")
    result = CourseModuleOut.model_validate(module)
    cache_set(cache_key, result.model_dump(mode="json"), ttl=CACHE_TTL_SECONDS)
    return result


def create_module(db: Session, payload: CourseModuleCreate, actor_id: uuid.UUID) -> CourseModuleOut:
    if tracks_repo.get_by_id(db, payload.track_id) is None:
        raise NotFoundError("Track introuvable.")
    module = modules_repo.create(db, CourseModule(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="module.created", module="course_modules", resource="module", resource_id=str(module.id))
    cache_delete_prefix("modules:")
    return CourseModuleOut.model_validate(module)


def update_module(db: Session, module_id: uuid.UUID, payload: CourseModuleUpdate, actor_id: uuid.UUID) -> CourseModuleOut:
    module = modules_repo.get_by_id(db, module_id)
    if module is None:
        raise NotFoundError("Module introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    module = modules_repo.update(db, module, fields)
    log_action(db, user_id=actor_id, action="module.updated", module="course_modules", resource="module", resource_id=str(module.id), new_value=fields)
    cache_delete_prefix("modules:")
    return CourseModuleOut.model_validate(module)


def delete_module(db: Session, module_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    module = modules_repo.get_by_id(db, module_id)
    if module is None:
        raise NotFoundError("Module introuvable.")
    modules_repo.delete(db, module)
    log_action(db, user_id=actor_id, action="module.deleted", module="course_modules", resource="module", resource_id=str(module_id))
    cache_delete_prefix("modules:")
