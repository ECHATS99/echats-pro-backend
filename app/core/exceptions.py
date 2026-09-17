"""Exceptions métier personnalisées + handler global qui formate les erreurs selon le format
standardisé (voir Partie 5.4 du SRS). Ne jamais exposer stack trace / secrets / SQL en réponse.
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.constants import ErrorCode

logger = logging.getLogger("echats.exceptions")


class AppError(Exception):
    """Exception métier de base. Toutes les exceptions applicatives en héritent."""

    def __init__(self, message: str, code: ErrorCode = ErrorCode.INTERNAL_ERROR,
                 status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Ressource introuvable."):
        super().__init__(message, ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentification requise."):
        super().__init__(message, ErrorCode.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Accès refusé."):
        super().__init__(message, ErrorCode.FORBIDDEN, status.HTTP_403_FORBIDDEN)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflit sur la ressource."):
        super().__init__(message, ErrorCode.CONFLICT, status.HTTP_409_CONFLICT)


class ValidationError(AppError):
    def __init__(self, message: str = "Requête invalide."):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)


class RateLimitedError(AppError):
    def __init__(self, message: str = "Trop de requêtes, réessayez plus tard."):
        super().__init__(message, ErrorCode.RATE_LIMITED, status.HTTP_429_TOO_MANY_REQUESTS)


class InvalidTokenError(AppError):
    def __init__(self, message: str = "Token invalide."):
        super().__init__(message, ErrorCode.INVALID_TOKEN, status.HTTP_401_UNAUTHORIZED)


class TokenExpiredError(AppError):
    def __init__(self, message: str = "Token expiré."):
        super().__init__(message, ErrorCode.TOKEN_EXPIRED, status.HTTP_401_UNAUTHORIZED)


class AccountSuspendedError(AppError):
    def __init__(self, message: str = "Compte suspendu."):
        super().__init__(message, ErrorCode.ACCOUNT_SUSPENDED, status.HTTP_403_FORBIDDEN)


class TwoFactorRequiredError(AppError):
    def __init__(self, message: str = "Authentification à deux facteurs requise."):
        super().__init__(message, ErrorCode.TWO_FACTOR_REQUIRED, status.HTTP_401_UNAUTHORIZED)


class QuotaExceededError(AppError):
    def __init__(self, message: str = "Quota dépassé pour votre abonnement."):
        super().__init__(message, ErrorCode.QUOTA_EXCEEDED, status.HTTP_403_FORBIDDEN)


def _error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={
        "success": False,
        "error": {"code": code, "message": message},
    })


def register_exception_handlers(app: FastAPI) -> None:
    """Enregistre les handlers d'exceptions globaux sur l'app FastAPI."""

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        return _error_response(exc.code.value, exc.message, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return _error_response(
            ErrorCode.VALIDATION_ERROR.value,
            "Les données envoyées sont invalides.",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        # Jamais de stack trace / message interne exposé au client (Partie 8.12 du SRS)
        logger.exception("Erreur interne non gérée")
        return _error_response(
            ErrorCode.INTERNAL_ERROR.value,
            "Une erreur interne est survenue.",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
