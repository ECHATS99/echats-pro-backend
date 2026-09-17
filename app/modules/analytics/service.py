"""Logique métier du domaine 'analytics'. Tableaux de bord agrégés pour l'admin, mis en
cache Redis (courte durée) pour ne pas surcharger PostgreSQL (Partie 7.4 du SRS)."""
from app.modules.analytics import repository as analytics_repo
from app.modules.analytics.schemas import CoursesAnalytics, CTFAnalytics, DashboardStats, PaymentsAnalytics, UsersAnalytics
from app.services.cache_service import cache_get, cache_set

CACHE_TTL_SECONDS = 60


def _cached(key: str, compute):
    cached = cache_get(key)
    if cached is not None:
        return cached
    value = compute()
    cache_set(key, value, CACHE_TTL_SECONDS)
    return value


def dashboard(db) -> DashboardStats:
    data = _cached("analytics:dashboard", lambda: analytics_repo.counts_overview(db))
    return DashboardStats(**data)


def users_analytics(db) -> UsersAnalytics:
    def compute():
        return {
            "total": analytics_repo.counts_overview(db)["total_users"],
            "by_role": analytics_repo.users_by_role(db),
            "by_country": analytics_repo.users_by_country(db),
            "new_last_30d": analytics_repo.new_users_last_30d(db),
        }
    return UsersAnalytics(**_cached("analytics:users", compute))


def courses_analytics(db) -> CoursesAnalytics:
    def compute():
        overview = analytics_repo.counts_overview(db)
        from sqlalchemy import select, func
        from app.models.lesson import Lesson
        from app.models.track import Track
        published = db.execute(select(func.count()).select_from(Track).where(Track.published.is_(True))).scalar_one()
        total_lessons = db.execute(select(func.count()).select_from(Lesson)).scalar_one()
        return {
            "total_tracks": overview["total_tracks"], "published_tracks": published,
            "total_lessons": total_lessons, "average_completion_rate": analytics_repo.average_completion_rate(db),
        }
    return CoursesAnalytics(**_cached("analytics:courses", compute))


def payments_analytics(db) -> PaymentsAnalytics:
    def compute():
        overview = analytics_repo.counts_overview(db)
        return {
            "total_revenue_fcfa": overview["total_revenue_fcfa"],
            "total_transactions": overview["total_orders"],
            "by_provider": analytics_repo.payments_by_provider(db),
        }
    return PaymentsAnalytics(**_cached("analytics:payments", compute))


def ctf_analytics(db) -> CTFAnalytics:
    def compute():
        overview = analytics_repo.counts_overview(db)
        return {
            "total_challenges": overview["total_ctf_challenges"],
            "total_solves": overview["total_ctf_solves"],
            "top_challenge_titles": analytics_repo.top_ctf_challenges(db),
        }
    return CTFAnalytics(**_cached("analytics:ctf", compute))
