"""Schémas Pydantic pour le domaine 'analytics'."""
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    active_users_30d: int
    total_tracks: int
    total_ctf_challenges: int
    total_ctf_solves: int
    total_revenue_fcfa: int
    total_orders: int
    active_subscriptions: int


class UsersAnalytics(BaseModel):
    total: int
    by_role: dict[str, int]
    by_country: dict[str, int]
    new_last_30d: int


class CoursesAnalytics(BaseModel):
    total_tracks: int
    published_tracks: int
    total_lessons: int
    average_completion_rate: float


class PaymentsAnalytics(BaseModel):
    total_revenue_fcfa: int
    total_transactions: int
    by_provider: dict[str, int]


class CTFAnalytics(BaseModel):
    total_challenges: int
    total_solves: int
    top_challenge_titles: list[str]
