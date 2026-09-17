"""Routes HTTP /api/v1/users. Profil utilisateur, préférences, statistiques,
recherche d'utilisateurs.
Route fine : valide l'entrée, vérifie permissions, appelle modules/users/service.py.
Aucune logique métier ici.
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.redis import get_redis
from app.modules.users import service as users_service
from app.modules.users.schemas import (
    TwoFactorEnableRequest, TwoFactorSetupOut, TwoFactorStatusOut,
    UserProfileOut, UserProfileUpdate, UserSearchResultOut, UserStatisticsOut,
)
from app.utils.pagination import paginate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserProfileOut)
def get_my_profile(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retourne le profil complet de l'utilisateur authentifié."""
    return users_service.get_profile(db, current.id)


@router.patch("/profile", response_model=UserProfileOut)
def update_my_profile(
    payload: UserProfileUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Met à jour les préférences modifiables du profil (jamais xp/level/role/plan)."""
    return users_service.update_profile(db, current.id, payload)


@router.get("/statistics", response_model=UserStatisticsOut)
def get_my_statistics(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Statistiques de l'utilisateur : XP, niveau, streak, exercices/CTF résolus, badges, certificats."""
    return users_service.get_statistics(db, current.id)


@router.get("/search")
def search_users(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Recherche paginée d'utilisateurs par nom d'utilisateur ou email."""
    users, total = users_service.search(db, q, page, limit)
    results = [UserSearchResultOut.model_validate(u).model_dump() for u in users]
    return paginate(results, page, limit, total)


@router.get("/2fa/status", response_model=TwoFactorStatusOut)
def get_two_factor_status(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return users_service.get_two_factor_status(db, current.id)


@router.post("/2fa/setup", response_model=TwoFactorSetupOut)
def setup_two_factor(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Génère un secret TOTP + QR provisioning URI. Ne l'active pas encore : appeler
    /2fa/enable avec un premier code valide pour confirmer (Partie 4.12 du SRS)."""
    return users_service.setup_two_factor(db, current.id)


@router.post("/2fa/enable", response_model=TwoFactorStatusOut)
def enable_two_factor(
    payload: TwoFactorEnableRequest,
    request: Request,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
):
    client_ip = request.client.host if request.client else None
    return users_service.enable_two_factor(
        db, current.id, payload, redis_client=redis_client, client_ip=client_ip
    )


@router.post("/2fa/disable", response_model=TwoFactorStatusOut)
def disable_two_factor(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return users_service.disable_two_factor(db, current.id)
