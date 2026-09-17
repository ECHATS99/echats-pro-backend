"""Constantes globales de l'application (rôles, plans, statuts, codes d'erreur)."""
from enum import Enum


class RoleName(str, Enum):
    STUDENT = "student"
    PREMIUM = "premium"
    MENTOR = "mentor"
    INSTRUCTOR = "instructor"
    INSTITUTION_MANAGER = "institution_manager"
    PARABEN_MANAGER = "paraben_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class PlanCode(str, Enum):
    GO = "GO"
    CORE_I = "CORE_I"
    PARABEN_NIVEAU_1 = "PARABEN_NIVEAU_1"
    CHAMBRE_CLOSE = "CHAMBRE_CLOSE"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"
    TRIAL = "trial"


class UserStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"


class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    MTN_MOMO = "mtn_momo"
    AIRTEL_MONEY = "airtel_money"
    WAVE = "wave"


# Rôles nécessitant obligatoirement le 2FA (voir Partie 4.12 du SRS)
ROLES_REQUIRING_2FA = {
    RoleName.ADMIN,
    RoleName.SUPER_ADMIN,
    RoleName.INSTITUTION_MANAGER,
    RoleName.PARABEN_MANAGER,
}

DEFAULT_ROLE_ON_REGISTER = RoleName.STUDENT
DEFAULT_PLAN_ON_REGISTER = PlanCode.GO

# Codes d'erreur standardisés (voir Partie 5.4 / 8.12 du SRS)
class ErrorCode(str, Enum):
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"
    ACCOUNT_BANNED = "ACCOUNT_BANNED"
    TWO_FACTOR_REQUIRED = "TWO_FACTOR_REQUIRED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
