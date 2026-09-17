"""Routes HTTP /api/v1/analytics (réservées à l'administration)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.analytics import service as analytics_service
from app.modules.analytics.schemas import CoursesAnalytics, CTFAnalytics, DashboardStats, PaymentsAnalytics, UsersAnalytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(current: CurrentUser = Depends(require_permission("analytics.read")), db: Session = Depends(get_db)):
    return analytics_service.dashboard(db)


@router.get("/users", response_model=UsersAnalytics)
def users(current: CurrentUser = Depends(require_permission("analytics.read")), db: Session = Depends(get_db)):
    return analytics_service.users_analytics(db)


@router.get("/courses", response_model=CoursesAnalytics)
def courses(current: CurrentUser = Depends(require_permission("analytics.read")), db: Session = Depends(get_db)):
    return analytics_service.courses_analytics(db)


@router.get("/payments", response_model=PaymentsAnalytics)
def payments(current: CurrentUser = Depends(require_permission("analytics.read")), db: Session = Depends(get_db)):
    return analytics_service.payments_analytics(db)


@router.get("/ctf", response_model=CTFAnalytics)
def ctf(current: CurrentUser = Depends(require_permission("analytics.read")), db: Session = Depends(get_db)):
    return analytics_service.ctf_analytics(db)
