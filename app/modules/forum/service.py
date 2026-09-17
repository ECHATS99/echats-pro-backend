"""Logique métier du domaine 'forum'. Topics, réponses, likes, signalements, modération."""
import uuid

from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.models.forum import ForumPost, ForumReport, ForumTopic
from app.modules.forum import repository as forum_repo
from app.modules.forum.schemas import PostCreate, PostOut, ReportCreate, TopicCreate, TopicOut
from app.services.audit_service import log_action
from app.utils.pagination import paginate


def list_topics(db, page: int, limit: int, category: str | None):
    items, total = forum_repo.list_topics(db, page, limit, category)
    return paginate([TopicOut.model_validate(t).model_dump() for t in items], page, limit, total)


def create_topic(db, payload: TopicCreate, user_id: uuid.UUID) -> TopicOut:
    topic = forum_repo.create_topic(db, ForumTopic(user_id=user_id, **payload.model_dump()))
    log_action(db, user_id=user_id, action="forum.topic_created", module="forum", resource="topic", resource_id=str(topic.id))
    return TopicOut.model_validate(topic)


def delete_topic(db, topic_id: uuid.UUID, user_id: uuid.UUID, is_moderator: bool) -> None:
    topic = forum_repo.get_topic(db, topic_id)
    if topic is None:
        raise NotFoundError("Sujet introuvable.")
    if topic.user_id != user_id and not is_moderator:
        raise ForbiddenError("Vous ne pouvez supprimer que vos propres sujets.")
    forum_repo.delete_topic(db, topic)
    log_action(db, user_id=user_id, action="forum.topic_deleted", module="forum", resource="topic", resource_id=str(topic_id))


def reply(db, topic_id: uuid.UUID, payload: PostCreate, user_id: uuid.UUID) -> PostOut:
    topic = forum_repo.get_topic(db, topic_id)
    if topic is None:
        raise NotFoundError("Sujet introuvable.")
    if topic.locked:
        raise ValidationError("Ce sujet est verrouillé, les réponses sont désactivées.")
    post = forum_repo.create_post(db, ForumPost(topic_id=topic_id, user_id=user_id, content=payload.content))
    out = PostOut.model_validate(post)
    out.likes_count = 0
    return out


def list_posts(db, topic_id: uuid.UUID) -> list[PostOut]:
    posts = forum_repo.list_posts(db, topic_id)
    result = []
    for p in posts:
        out = PostOut.model_validate(p)
        out.likes_count = len(p.likes)
        result.append(out)
    return result


def toggle_like(db, post_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    if forum_repo.get_post(db, post_id) is None:
        raise NotFoundError("Message introuvable.")
    liked = forum_repo.toggle_like(db, post_id, user_id)
    return {"liked": liked}


def report(db, payload: ReportCreate, user_id: uuid.UUID) -> None:
    if not payload.post_id and not payload.topic_id:
        raise ValidationError("Un signalement doit cibler un message ou un sujet.")
    forum_repo.create_report(db, ForumReport(reporter_id=user_id, **payload.model_dump()))
    log_action(db, user_id=user_id, action="forum.reported", module="forum", resource="report")
