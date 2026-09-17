"""Routes HTTP /api/v1/forum."""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_db_user, get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.modules.forum import service as forum_service
from app.modules.forum.schemas import PostCreate, PostOut, ReportCreate, TopicCreate, TopicOut

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("")
def list_topics(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), category: str | None = None, db: Session = Depends(get_db)):
    return forum_service.list_topics(db, page, limit, category)


@router.post("/topic", response_model=TopicOut, status_code=201)
def create_topic(payload: TopicCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return forum_service.create_topic(db, payload, current.id)


@router.delete("/topic/{topic_id}", status_code=204)
def delete_topic(topic_id: uuid.UUID, current: User = Depends(get_current_db_user), db: Session = Depends(get_db)):
    is_moderator = current.primary_role_name in ("admin", "super_admin", "instructor", "mentor")
    forum_service.delete_topic(db, topic_id, current.id, is_moderator)


@router.get("/topic/{topic_id}/posts", response_model=list[PostOut])
def list_posts(topic_id: uuid.UUID, db: Session = Depends(get_db)):
    return forum_service.list_posts(db, topic_id)


@router.post("/topic/{topic_id}/reply", response_model=PostOut, status_code=201)
def reply(topic_id: uuid.UUID, payload: PostCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return forum_service.reply(db, topic_id, payload, current.id)


@router.post("/post/{post_id}/like")
def toggle_like(post_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return forum_service.toggle_like(db, post_id, current.id)


@router.post("/report", status_code=201)
def report(payload: ReportCreate, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    forum_service.report(db, payload, current.id)
