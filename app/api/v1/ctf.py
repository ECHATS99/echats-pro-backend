"""Routes HTTP /api/v1/ctf."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.dependencies.redis import get_redis
from app.modules.ctf import service as ctf_service
from app.modules.ctf.schemas import (
    CTFCategoryOut, CTFChallengeCreate, CTFChallengeOut, CTFChallengeUpdate,
    CTFEventOut, CTFFlagSubmission, CTFLeaderboardEntry, CTFSubmitResult,
)

router = APIRouter(prefix="/ctf", tags=["ctf"])


@router.get("/events", response_model=list[CTFEventOut])
def list_events(db: Session = Depends(get_db)):
    return ctf_service.list_events(db)


@router.get("/categories", response_model=list[CTFCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return ctf_service.list_categories(db)


@router.get("/leaderboard", response_model=list[CTFLeaderboardEntry])
def leaderboard(db: Session = Depends(get_db)):
    return ctf_service.get_leaderboard(db)


@router.get("/challenges", response_model=list[CTFChallengeOut])
def list_challenges(
    category_id: uuid.UUID | None = None, event_id: uuid.UUID | None = None,
    current: CurrentUser | None = Depends(get_current_user), db: Session = Depends(get_db),
):
    return ctf_service.list_challenges(db, current.id if current else None, category_id, event_id)


@router.get("/challenges/{challenge_id}", response_model=CTFChallengeOut)
def get_challenge(
    challenge_id: uuid.UUID,
    current: CurrentUser | None = Depends(get_current_user), db: Session = Depends(get_db),
):
    return ctf_service.get_challenge(db, challenge_id, current.id if current else None)


@router.post("/challenges", response_model=CTFChallengeOut, status_code=201)
def create_challenge(
    payload: CTFChallengeCreate,
    current: CurrentUser = Depends(require_permission("ctf.create")),
    db: Session = Depends(get_db),
):
    return ctf_service.create_challenge(db, payload, current.id)


@router.patch("/challenges/{challenge_id}", response_model=CTFChallengeOut)
def update_challenge(
    challenge_id: uuid.UUID, payload: CTFChallengeUpdate,
    current: CurrentUser = Depends(require_permission("ctf.create")),
    db: Session = Depends(get_db),
):
    return ctf_service.update_challenge(db, challenge_id, payload, current.id)


@router.delete("/challenges/{challenge_id}", status_code=204)
def delete_challenge(
    challenge_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("ctf.create")),
    db: Session = Depends(get_db),
):
    ctf_service.delete_challenge(db, challenge_id, current.id)


@router.post("/submit", response_model=CTFSubmitResult)
def submit_flag(
    challenge_id: uuid.UUID, payload: CTFFlagSubmission,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db), redis_client=Depends(get_redis),
):
    """Endpoint générique de soumission (Partie 5.15 du SRS : POST /ctf/submit)."""
    return ctf_service.submit_flag(db, redis_client, challenge_id, current.id, payload)
