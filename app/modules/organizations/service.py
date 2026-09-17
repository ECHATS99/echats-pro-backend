"""Logique métier du domaine 'organizations' (institutions / Chambre Close). Isolation
stricte des données par institution_id (Partie 4.11 du SRS)."""
import uuid

from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.models.institution import Institution
from app.modules.organizations import repository as orgs_repo
from app.modules.organizations.schemas import (
    InstitutionCreate, InstitutionMemberOut, InstitutionOut, InstitutionUpdate,
)
from app.services.audit_service import log_action
from app.utils.pagination import paginate


def list_institutions(db, page: int, limit: int):
    items, total = orgs_repo.list_all(db, page, limit)
    return paginate([InstitutionOut.model_validate(i).model_dump() for i in items], page, limit, total)


def get_institution(db, institution_id: uuid.UUID, requester) -> InstitutionOut:
    institution = orgs_repo.get_by_id(db, institution_id)
    if institution is None:
        raise NotFoundError("Institution introuvable.")
    if requester.primary_role_name not in {"admin", "super_admin"}:
        assert_same_institution(requester.institution_id, institution_id)
    return InstitutionOut.model_validate(institution)


def create_institution(db, payload: InstitutionCreate, actor_id: uuid.UUID) -> InstitutionOut:
    institution = orgs_repo.create(db, Institution(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="institution.created", module="institution", resource="institution", resource_id=str(institution.id))
    return InstitutionOut.model_validate(institution)


def update_institution(db, institution_id: uuid.UUID, payload: InstitutionUpdate, actor_id: uuid.UUID) -> InstitutionOut:
    institution = orgs_repo.get_by_id(db, institution_id)
    if institution is None:
        raise NotFoundError("Institution introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    institution = orgs_repo.update(db, institution, fields)
    log_action(db, user_id=actor_id, action="institution.updated", module="institution", resource="institution", resource_id=str(institution.id), new_value=fields)
    return InstitutionOut.model_validate(institution)


def assert_same_institution(requester_institution_id: uuid.UUID | None, target_institution_id: uuid.UUID) -> None:
    """Vérifie l'isolation stricte : une institution ne peut jamais consulter les données
    d'une autre (Partie 4.11 du SRS : institution_id == user.institution_id avant toute réponse)."""
    if requester_institution_id != target_institution_id:
        raise ForbiddenError("Accès refusé : cette ressource appartient à une autre institution.")


def list_members(db, institution_id: uuid.UUID, requester_institution_id: uuid.UUID | None) -> list[InstitutionMemberOut]:
    assert_same_institution(requester_institution_id, institution_id)
    return [InstitutionMemberOut(id=u.id, username=u.username, email=u.email, role="member") for u in orgs_repo.list_members(db, institution_id)]


def check_capacity(db, institution_id: uuid.UUID) -> None:
    institution = orgs_repo.get_by_id(db, institution_id)
    if institution is None:
        raise NotFoundError("Institution introuvable.")
    if orgs_repo.count_members(db, institution_id) >= institution.max_users:
        raise ValidationError("Le nombre maximal d'utilisateurs pour cette institution est atteint.")
