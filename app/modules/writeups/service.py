"""Logique métier du domaine 'writeups'. Rédaction, publication, votes."""
import uuid

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.writeup import Writeup
from app.modules.writeups import repository as writeups_repo
from app.modules.writeups.schemas import VoteRequest, WriteupCreate, WriteupOut, WriteupUpdate
from app.services.audit_service import log_action
from app.utils.pagination import paginate


def list_writeups(db, page: int, limit: int, ctf_id: uuid.UUID | None):
    items, total = writeups_repo.list_published(db, page, limit, ctf_id)
    return paginate([WriteupOut.model_validate(w).model_dump() for w in items], page, limit, total)


def get_writeup(db, writeup_id: uuid.UUID) -> WriteupOut:
    writeup = writeups_repo.get_by_id(db, writeup_id)
    if writeup is None:
        raise NotFoundError("Writeup introuvable.")
    return WriteupOut.model_validate(writeup)


def create_writeup(db, payload: WriteupCreate, user_id: uuid.UUID) -> WriteupOut:
    writeup = writeups_repo.create(db, Writeup(user_id=user_id, **payload.model_dump()))
    log_action(db, user_id=user_id, action="writeup.created", module="writeups", resource="writeup", resource_id=str(writeup.id))
    return WriteupOut.model_validate(writeup)


def update_writeup(db, writeup_id: uuid.UUID, payload: WriteupUpdate, user_id: uuid.UUID, is_moderator: bool = False) -> WriteupOut:
    writeup = writeups_repo.get_by_id(db, writeup_id)
    if writeup is None:
        raise NotFoundError("Writeup introuvable.")
    if writeup.user_id != user_id and not is_moderator:
        raise ForbiddenError("Vous ne pouvez modifier que vos propres writeups.")
    fields = payload.model_dump(exclude_unset=True)
    writeup = writeups_repo.update(db, writeup, fields)
    return WriteupOut.model_validate(writeup)


def delete_writeup(db, writeup_id: uuid.UUID, user_id: uuid.UUID, is_moderator: bool = False) -> None:
    writeup = writeups_repo.get_by_id(db, writeup_id)
    if writeup is None:
        raise NotFoundError("Writeup introuvable.")
    if writeup.user_id != user_id and not is_moderator:
        raise ForbiddenError("Vous ne pouvez supprimer que vos propres writeups.")
    writeups_repo.delete(db, writeup)
    log_action(db, user_id=user_id, action="writeup.deleted", module="writeups", resource="writeup", resource_id=str(writeup_id))


def vote(db, writeup_id: uuid.UUID, user_id: uuid.UUID, payload: VoteRequest) -> WriteupOut:
    writeup = writeups_repo.get_by_id(db, writeup_id)
    if writeup is None:
        raise NotFoundError("Writeup introuvable.")
    writeup = writeups_repo.upsert_vote(db, writeup, user_id, payload.value)
    return WriteupOut.model_validate(writeup)
