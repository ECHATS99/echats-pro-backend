"""Logique métier du domaine 'certificates'. Génération de certificats PDF signés,
vérification par code public. Ne contient aucune requête SQL directe : passe par repository.py.
"""
import uuid

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from app.models.certificate import Certificate
from app.models.course_module import CourseModule
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User
from app.modules.certificates import repository as certificates_repo
from app.modules.certificates.schemas import CertificateOut, CertificateVerifyOut
from app.modules.tracks import repository as tracks_repo
from app.services.audit_service import log_action
from app.services.certificate_service import generate_certificate_pdf, verify_signature
from app.services.email_service import send_certificate_email


def _track_fully_completed(db, user_id: uuid.UUID, track_id: uuid.UUID) -> bool:
    from sqlalchemy import select
    lesson_ids = db.execute(
        select(Lesson.id).join(CourseModule, CourseModule.id == Lesson.module_id).where(CourseModule.track_id == track_id)
    ).scalars().all()
    if not lesson_ids:
        return False
    completed = db.execute(
        select(UserProgress).where(UserProgress.user_id == user_id, UserProgress.lesson_id.in_(lesson_ids), UserProgress.completed.is_(True))
    ).scalars().all()
    return len(completed) >= len(lesson_ids)


def generate_certificate(db, user_id: uuid.UUID, track_id: uuid.UUID) -> CertificateOut:
    track = tracks_repo.get_by_id(db, track_id)
    if track is None:
        raise NotFoundError("Track introuvable.")
    if certificates_repo.get_by_user_and_track(db, user_id, track_id) is not None:
        raise ConflictError("Un certificat existe déjà pour ce track.")
    if not _track_fully_completed(db, user_id, track_id):
        raise ValidationError("Toutes les leçons du track doivent être complétées avant de générer le certificat.")

    user = db.get(User, user_id)
    pdf_data = generate_certificate_pdf(user_id, user.username, track_id, track.title)

    certificate = certificates_repo.create(db, Certificate(user_id=user_id, track_id=track_id, **pdf_data))
    send_certificate_email(user.email, user.username, track.title, f"/certificates/verify/{certificate.verification_code}")
    log_action(db, user_id=user_id, action="certificate.generated", module="certificates", resource="certificate", resource_id=str(certificate.id))
    return CertificateOut.model_validate(certificate)


def list_my_certificates(db, user_id: uuid.UUID) -> list[CertificateOut]:
    return [CertificateOut.model_validate(c) for c in certificates_repo.list_for_user(db, user_id)]


def verify_certificate(db, code: str) -> CertificateVerifyOut:
    certificate = certificates_repo.get_by_verification_code(db, code)
    if certificate is None:
        return CertificateVerifyOut(valid=False)

    is_valid = verify_signature(certificate.verification_code, certificate.user_id, certificate.track_id, certificate.signature or "")
    if not is_valid:
        return CertificateVerifyOut(valid=False)

    track = tracks_repo.get_by_id(db, certificate.track_id)
    user = db.get(User, certificate.user_id)
    return CertificateVerifyOut(
        valid=True, track_title=track.title if track else None,
        issued_at=certificate.issued_at, username=user.username if user else None,
    )
