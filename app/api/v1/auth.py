"""Routes HTTP d'authentification : Firebase, 2FA, sessions et logout."""
from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.dependencies.database import get_db
from app.dependencies.redis import get_redis
from app.modules.auth import service as auth_service
from app.modules.auth.service import get_active_plan_code
from app.modules.auth.schemas import (
    AuthTokensOut, FirebaseLoginRequest, RefreshRequest, TwoFactorVerifyRequest, UserPublicOut,
)
from app.security.rate_limit import check_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _user_agent(request: Request) -> str | None:
    value = request.headers.get("user-agent")
    return value[:500] if value else None


def _to_tokens_out(user, access_token: str, refresh_token: str) -> AuthTokensOut:
    return AuthTokensOut(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserPublicOut(
            id=user.id, email=user.email, username=user.username,
            role=user.primary_role_name, plan=get_active_plan_code(user), avatar_url=user.avatar_url,
            xp=user.xp, level=user.level,
        ),
    )


@router.post("/login", response_model=AuthTokensOut)
def login(
    payload: FirebaseLoginRequest,
    request: Request,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
):
    ip = _client_ip(request)
    check_rate_limit(redis_client, f"ratelimit:login:{ip}", settings.RATE_LIMIT_LOGIN_PER_MINUTE, 60)

    user, access_token, refresh_token = auth_service.authenticate_with_firebase(
        db,
        payload.id_token,
        totp_code=None,
        client_ip=ip,
        redis_client=redis_client,
        user_agent=_user_agent(request),
    )
    return _to_tokens_out(user, access_token, refresh_token)


@router.post("/2fa/verify", response_model=AuthTokensOut)
def verify_2fa(
    payload: TwoFactorVerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
):
    """Complète l'authentification avec rate limit IP + compte et code à usage unique."""
    ip = _client_ip(request)
    user, access_token, refresh_token = auth_service.authenticate_with_firebase(
        db,
        payload.id_token,
        totp_code=payload.totp_code,
        client_ip=ip,
        redis_client=redis_client,
        user_agent=_user_agent(request),
    )
    return _to_tokens_out(user, access_token, refresh_token)


@router.post("/refresh")
def refresh(
    payload: RefreshRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Fait tourner le refresh token et invalide immédiatement l'ancien."""
    access_token, new_refresh_token = auth_service.refresh_access_token(
        db,
        payload.refresh_token,
        client_ip=_client_ip(request),
        user_agent=_user_agent(request),
    )
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(
    payload: RefreshRequest | None = Body(default=None),
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Révoque le refresh token fourni ; l'absence de body reste rétrocompatible."""
    if payload is not None:
        auth_service.revoke_refresh_token(db, payload.refresh_token, current.id)
    return {"success": True, "message": "Déconnecté."}


@router.get("/me", response_model=UserPublicOut)
def me(user=Depends(get_current_db_user)):
    return UserPublicOut(
        id=user.id, email=user.email, username=user.username,
        role=user.primary_role_name, plan=get_active_plan_code(user), avatar_url=user.avatar_url,
        xp=user.xp, level=user.level,
    )
