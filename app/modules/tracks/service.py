"""Logique métier du domaine 'tracks'."""
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.track import Track
from app.modules.tracks import repository as tracks_repo
from app.modules.tracks.schemas import TrackCreate, TrackOut, TrackUpdate
from app.services.audit_service import log_action
from app.services.cache_service import cache_delete_prefix, cache_get, cache_set
from app.utils.slug import make_unique_slug

CACHE_TTL_SECONDS = 300  # catalogue peu volatile ; évite un aller-retour DB à chaque visite


def get_track(db: Session, track_id: uuid.UUID) -> TrackOut:
    cache_key = f"tracks:by_id:{track_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return TrackOut.model_validate(cached)
    track = tracks_repo.get_by_id(db, track_id)
    if track is None:
        raise NotFoundError("Track introuvable.")
    result = TrackOut.model_validate(track)
    cache_set(cache_key, result.model_dump(mode="json"), ttl=CACHE_TTL_SECONDS)
    return result


def get_track_by_slug(db: Session, slug: str) -> TrackOut:
    cache_key = f"tracks:by_slug:{slug}"
    cached = cache_get(cache_key)
    if cached is not None:
        return TrackOut.model_validate(cached)
    track = tracks_repo.get_by_slug(db, slug)
    if track is None:
        raise NotFoundError("Track introuvable.")
    result = TrackOut.model_validate(track)
    cache_set(cache_key, result.model_dump(mode="json"), ttl=CACHE_TTL_SECONDS)
    return result


def list_tracks(db: Session, page: int, limit: int, difficulty: str | None, domain: str | None, published_only: bool = True):
    cache_key = f"tracks:list:{page}:{limit}:{difficulty}:{domain}:{published_only}"
    cached = cache_get(cache_key)
    if cached is not None:
        return [TrackOut.model_validate(t) for t in cached["tracks"]], cached["total"]
    tracks, total = tracks_repo.list_tracks(db, page, limit, difficulty=difficulty, domain=domain, published_only=published_only)
    result = [TrackOut.model_validate(t) for t in tracks]
    cache_set(cache_key, {"tracks": [t.model_dump(mode="json") for t in result], "total": total}, ttl=CACHE_TTL_SECONDS)
    return result, total


def create_track(db: Session, payload: TrackCreate, actor_id: uuid.UUID) -> TrackOut:
    slug = make_unique_slug(payload.title, lambda s: tracks_repo.slug_exists(db, s))
    track = Track(**payload.model_dump(), slug=slug)
    track = tracks_repo.create(db, track)
    log_action(db, user_id=actor_id, action="track.created", module="tracks", resource="track", resource_id=str(track.id))
    cache_delete_prefix("tracks:")
    return TrackOut.model_validate(track)


def update_track(db: Session, track_id: uuid.UUID, payload: TrackUpdate, actor_id: uuid.UUID) -> TrackOut:
    track = tracks_repo.get_by_id(db, track_id)
    if track is None:
        raise NotFoundError("Track introuvable.")
    fields = payload.model_dump(exclude_unset=True)
    if "title" in fields and fields["title"] != track.title:
        fields["slug"] = make_unique_slug(fields["title"], lambda s: tracks_repo.slug_exists(db, s))
    track = tracks_repo.update(db, track, fields)
    log_action(db, user_id=actor_id, action="track.updated", module="tracks", resource="track", resource_id=str(track.id), new_value=fields)
    cache_delete_prefix("tracks:")
    return TrackOut.model_validate(track)


def delete_track(db: Session, track_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    track = tracks_repo.get_by_id(db, track_id)
    if track is None:
        raise NotFoundError("Track introuvable.")
    tracks_repo.soft_delete(db, track)
    log_action(db, user_id=actor_id, action="track.deleted", module="tracks", resource="track", resource_id=str(track.id))
    cache_delete_prefix("tracks:")
