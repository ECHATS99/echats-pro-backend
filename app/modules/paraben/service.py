"""Logique métier du domaine 'paraben' (Chambre Close). Accès réservé aux abonnés
institutionnels ou au tier Paraben Niveau 1 (Partie 8 du SRS)."""
import uuid

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.institution import Institution
from app.models.paraben import ParabenCourse
from app.models.user import User
from app.modules.paraben import repository as paraben_repo
from app.modules.paraben.schemas import (
    ParabenCourseCreate, ParabenCourseOut, ParabenProgressOut, ParabenProgressUpdate, ParabenRevenueReport,
)
from app.modules.subscriptions import repository as subscriptions_repo
from app.services.audit_service import log_action


def assert_paraben_access(db, user: User) -> None:
    """Vérifie l'accès à la Chambre Close : abonnement Paraben actif OU institution
    avec paraben_access=True (Partie 8 du SRS : ouvert à toute institution, pas
    réservé à Paraben). Ne fait jamais confiance à un rôle envoyé par le frontend.
    """
    subscription = subscriptions_repo.get_active_for_user(db, user.id)
    if subscription is not None and subscription.plan.code == "PARABEN_NIVEAU_1":
        return

    if user.institution_id:
        institution = db.get(Institution, user.institution_id)
        if institution is not None and institution.paraben_access and institution.active:
            return

    raise ForbiddenError("Accès réservé aux abonnés Paraben Niveau 1 ou aux institutions partenaires (Chambre Close).")


def list_courses(db, user: User) -> list[ParabenCourseOut]:
    assert_paraben_access(db, user)
    return [ParabenCourseOut.model_validate(c) for c in paraben_repo.list_courses(db)]


def create_course(db, payload: ParabenCourseCreate, actor_id: uuid.UUID) -> ParabenCourseOut:
    course = paraben_repo.create_course(db, ParabenCourse(**payload.model_dump()))
    log_action(db, user_id=actor_id, action="paraben.course_created", module="paraben", resource="course", resource_id=str(course.id))
    return ParabenCourseOut.model_validate(course)


def update_progress(db, user: User, course_id: uuid.UUID, payload: ParabenProgressUpdate) -> ParabenProgressOut:
    assert_paraben_access(db, user)
    if paraben_repo.get_course(db, course_id) is None:
        raise NotFoundError("Cours Paraben introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    progress = paraben_repo.upsert_progress(db, user.id, course_id, fields)
    return ParabenProgressOut.model_validate(progress)


def revenue_report(db, period: str) -> ParabenRevenueReport:
    """Rapport mensuel du partage de revenus 50/50, exportable depuis l'admin (Partie 6 du SRS)."""
    data = paraben_repo.revenue_report(db, period)
    return ParabenRevenueReport(period=period, **data)
