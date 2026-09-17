"""Logique métier du domaine 'classroom'. Salles de classe : création, membres, rôles,
devoirs assignés, deadlines. Ne contient aucune requête SQL directe : passe par repository.py.
"""
import uuid

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.classroom import Classroom, ClassroomAssignment
from app.modules.classroom import repository as classroom_repo
from app.modules.classroom.schemas import (
    AssignmentCreate, AssignmentOut, ClassroomCreate, ClassroomJoin, ClassroomMemberOut, ClassroomOut,
)
from app.services.audit_service import log_action
from app.services.websocket_service import broadcast_classroom
from app.utils.strings import generate_access_code


def _generate_unique_code(db) -> str:
    code = generate_access_code()
    while classroom_repo.get_by_access_code(db, code) is not None:
        code = generate_access_code()
    return code


def create_classroom(db, payload: ClassroomCreate, teacher_id: uuid.UUID) -> ClassroomOut:
    classroom = Classroom(
        title=payload.title, institution_id=payload.institution_id,
        teacher_id=teacher_id, access_code=_generate_unique_code(db),
    )
    classroom = classroom_repo.create(db, classroom)
    classroom_repo.add_member(db, classroom.id, teacher_id, role="teacher")
    log_action(db, user_id=teacher_id, action="classroom.created", module="classroom", resource="classroom", resource_id=str(classroom.id))
    return ClassroomOut.model_validate(classroom)


def get_classroom(db, classroom_id: uuid.UUID) -> ClassroomOut:
    classroom = classroom_repo.get_by_id(db, classroom_id)
    if classroom is None:
        raise NotFoundError("Classroom introuvable.")
    return ClassroomOut.model_validate(classroom)


def list_my_classrooms(db, user_id: uuid.UUID) -> list[ClassroomOut]:
    owned = classroom_repo.list_for_teacher(db, user_id)
    joined = classroom_repo.list_for_member(db, user_id)
    merged = {c.id: c for c in owned + joined}
    return [ClassroomOut.model_validate(c) for c in merged.values()]


def join_classroom(db, payload: ClassroomJoin, user_id: uuid.UUID) -> ClassroomMemberOut:
    classroom = classroom_repo.get_by_access_code(db, payload.access_code)
    if classroom is None:
        raise NotFoundError("Code d'accès invalide.")
    if classroom_repo.get_membership(db, classroom.id, user_id) is not None:
        raise ConflictError("Vous êtes déjà membre de cette classroom.")

    member = classroom_repo.add_member(db, classroom.id, user_id, role="student")
    broadcast_classroom(classroom.id, {"event": "member_joined", "user_id": str(user_id)})
    log_action(db, user_id=user_id, action="classroom.joined", module="classroom", resource="classroom", resource_id=str(classroom.id))
    return ClassroomMemberOut.model_validate(member)


def leave_classroom(db, classroom_id: uuid.UUID, user_id: uuid.UUID) -> None:
    member = classroom_repo.get_membership(db, classroom_id, user_id)
    if member is None:
        raise NotFoundError("Vous n'êtes pas membre de cette classroom.")
    classroom_repo.remove_member(db, member)
    log_action(db, user_id=user_id, action="classroom.left", module="classroom", resource="classroom", resource_id=str(classroom_id))


def list_members(db, classroom_id: uuid.UUID, requester_id: uuid.UUID) -> list[ClassroomMemberOut]:
    _assert_instructor(db, classroom_id, requester_id)
    return [ClassroomMemberOut.model_validate(m) for m in classroom_repo.list_members(db, classroom_id)]


def _assert_instructor(db, classroom_id: uuid.UUID, user_id: uuid.UUID) -> Classroom:
    classroom = classroom_repo.get_by_id(db, classroom_id)
    if classroom is None:
        raise NotFoundError("Classroom introuvable.")
    if classroom.teacher_id != user_id:
        member = classroom_repo.get_membership(db, classroom_id, user_id)
        if member is None or member.role not in ("teacher", "assistant"):
            raise ForbiddenError("Seul l'enseignant ou un assistant peut effectuer cette action.")
    return classroom


def create_assignment(db, classroom_id: uuid.UUID, payload: AssignmentCreate, requester_id: uuid.UUID) -> AssignmentOut:
    _assert_instructor(db, classroom_id, requester_id)
    assignment = classroom_repo.create_assignment(db, ClassroomAssignment(classroom_id=classroom_id, **payload.model_dump()))
    broadcast_classroom(classroom_id, {"event": "assignment_created", "assignment_id": str(assignment.id)})
    log_action(db, user_id=requester_id, action="classroom.assignment_created", module="classroom", resource="classroom", resource_id=str(classroom_id))
    return AssignmentOut.model_validate(assignment)


def list_assignments(db, classroom_id: uuid.UUID) -> list[AssignmentOut]:
    return [AssignmentOut.model_validate(a) for a in classroom_repo.list_assignments(db, classroom_id)]
