"""Routes HTTP /api/v1/leaderboard."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.modules.leaderboard import service as leaderboard_service
from app.modules.leaderboard.schemas import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
def get_leaderboard(limit: int = Query(50, ge=1, le=200), country: str | None = None, db: Session = Depends(get_db)):
    return leaderboard_service.get_leaderboard(db, limit, country)


@router.get("/me")
def my_rank(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return leaderboard_service.get_my_rank(db, current.id)
