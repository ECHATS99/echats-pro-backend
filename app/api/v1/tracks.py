"""Routes HTTP /api/v1/tracks."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.tracks import service as tracks_service
from app.modules.tracks.schemas import TrackCreate, TrackOut, TrackUpdate
from app.utils.pagination import paginate

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("")
def list_tracks(
    page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
    difficulty: str | None = None, domain: str | None = None,
    db: Session = Depends(get_db),
):
    """Catalogue public des tracks publiés (filtres niveau/domaine)."""
    tracks, total = tracks_service.list_tracks(db, page, limit, difficulty, domain, published_only=True)
    return paginate([t.model_dump() for t in tracks], page, limit, total)


@router.get("/slug/{slug}", response_model=TrackOut)
def get_track_by_slug(slug: str, db: Session = Depends(get_db)):
    """Résolution par slug (URLs conviviales côté frontend, ex: /tracks/pentest-web-owasp)."""
    return tracks_service.get_track_by_slug(db, slug)


@router.get("/{track_id}", response_model=TrackOut)
def get_track(track_id: uuid.UUID, db: Session = Depends(get_db)):
    return tracks_service.get_track(db, track_id)


@router.post("", response_model=TrackOut, status_code=201)
def create_track(
    payload: TrackCreate,
    current: CurrentUser = Depends(require_permission("tracks.create")),
    db: Session = Depends(get_db),
):
    return tracks_service.create_track(db, payload, current.id)


@router.patch("/{track_id}", response_model=TrackOut)
def update_track(
    track_id: uuid.UUID, payload: TrackUpdate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return tracks_service.update_track(db, track_id, payload, current.id)


@router.delete("/{track_id}", status_code=204)
def delete_track(
    track_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    tracks_service.delete_track(db, track_id, current.id)
