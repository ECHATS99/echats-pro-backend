"""Accès aux données du domaine 'classroom' via SQLAlchemy. Seul endroit qui interroge la base pour ce domaine."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.classroom import Classroom, ClassroomAssignment, ClassroomMember


def get_by_id(db: Session, classroom_id: uuid.UUID) -> Classroom | None:
    return db.get(Classroom, classroom_id)


def get_by_access_code(db: Session, code: str) -> Classroom | None:
    stmt = select(Classroom).where(Classroom.access_code == code, Classroom.active.is_(True))
    return db.execute(stmt).scalar_one_or_none()


def list_for_teacher(db: Session, teacher_id: uuid.UUID) -> list[Classroom]:
    stmt = select(Classroom).where(Classroom.teacher_id == teacher_id)
    return list(db.execute(stmt).scalars().all())


def list_for_member(db: Session, user_id: uuid.UUID) -> list[Classroom]:
    stmt = (
        select(Classroom)
        .join(ClassroomMember, ClassroomMember.classroom_id == Classroom.id)
        .where(ClassroomMember.user_id == user_id)
    )
    return list(db.execute(stmt).scalars().all())


def create(db: Session, classroom: Classroom) -> Classroom:
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom


def get_membership(db: Session, classroom_id: uuid.UUID, user_id: uuid.UUID) -> ClassroomMember | None:
    stmt = select(ClassroomMember).where(ClassroomMember.classroom_id == classroom_id, ClassroomMember.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def add_member(db: Session, classroom_id: uuid.UUID, user_id: uuid.UUID, role: str = "student") -> ClassroomMember:
    member = ClassroomMember(classroom_id=classroom_id, user_id=user_id, role=role)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def remove_member(db: Session, member: ClassroomMember) -> None:
    db.delete(member)
    db.commit()


def list_members(db: Session, classroom_id: uuid.UUID) -> list[ClassroomMember]:
    stmt = select(ClassroomMember).where(ClassroomMember.classroom_id == classroom_id)
    return list(db.execute(stmt).scalars().all())


def create_assignment(db: Session, assignment: ClassroomAssignment) -> ClassroomAssignment:
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def list_assignments(db: Session, classroom_id: uuid.UUID) -> list[ClassroomAssignment]:
    stmt = select(ClassroomAssignment).where(ClassroomAssignment.classroom_id == classroom_id)
    return list(db.execute(stmt).scalars().all())
