"""Routes HTTP /api/v1/lessons."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.lessons import service as lessons_service
from app.modules.lessons.schemas import LessonCreate, LessonDetailOut, LessonListOut, LessonUpdate, ProgressUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/by-module/{module_id}", response_model=list[LessonListOut])
def list_lessons(module_id: uuid.UUID, db: Session = Depends(get_db)):
    return lessons_service.list_lessons_for_module(db, module_id)


@router.get("/all")
def list_all_lessons(db: Session = Depends(get_db)):
    """Renvoie TOUT le curriculum (tracks + modules + lessons) en 1 requête.
    Optimisé pour le frontend : 1 appel au lieu de 22+.
    """
    from sqlalchemy import select
    from app.models.track import Track
    from app.models.course_module import CourseModule
    from app.models.lesson import Lesson

    tracks = db.execute(
        select(Track).where(Track.deleted_at.is_(None)).order_by(Track.created_at)
    ).scalars().all()
    modules = db.execute(select(CourseModule).order_by(CourseModule.order)).scalars().all()
    lessons = db.execute(select(Lesson).order_by(Lesson.order)).scalars().all()

    modules_by_track = {}
    for m in modules:
        modules_by_track.setdefault(str(m.track_id), []).append(m)

    lessons_by_module = {}
    for l in lessons:
        lessons_by_module.setdefault(str(l.module_id), []).append(l)

    result_tracks = []
    flat_lessons = []

    for t in tracks:
        t_modules = []
        for m in modules_by_track.get(str(t.id), []):
            m_lessons = []
            for l in lessons_by_module.get(str(m.id), []):
                lesson_dict = {
                    "id": str(l.id),
                    "module_id": str(l.module_id),
                    "title": l.title,
                    "content": l.content,
                    "video": getattr(l, "video", None),
                    "duration_minutes": l.duration_minutes or 0,
                    "order": l.order or 0,
                    "published": l.published,
                    "category": m.title,
                    "module_title": m.title,
                    "track_slug": t.slug,
                    "track_title": t.title,
                    "difficulty": t.difficulty,
                    "domain": t.domain,
                    "description": t.description or getattr(m, "description", None),
                }
                m_lessons.append(lesson_dict)
                flat_lessons.append(lesson_dict)

            t_modules.append({
                "id": str(m.id),
                "track_id": str(m.track_id),
                "title": m.title,
                "description": getattr(m, "description", None),
                "order": getattr(m, "order", 0),
                "published": getattr(m, "published", True),
                "lessons": m_lessons,
            })

        result_tracks.append({
            "id": str(t.id),
            "title": t.title,
            "slug": t.slug,
            "description": t.description,
            "difficulty": t.difficulty,
            "domain": t.domain,
            "cover_image": t.cover_image,
            "published": t.published,
            "modules": t_modules,
        })

    return {
        "tracks": result_tracks,
        "lessons": flat_lessons,
        "total_tracks": len(result_tracks),
        "total_lessons": len(flat_lessons),
    }


@router.get("/{lesson_id}", response_model=LessonDetailOut)
def get_lesson(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    return lessons_service.get_lesson(db, lesson_id)


@router.post("", response_model=LessonDetailOut, status_code=201)
def create_lesson(
    payload: LessonCreate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return lessons_service.create_lesson(db, payload, current.id)


@router.patch("/{lesson_id}", response_model=LessonDetailOut)
def update_lesson(
    lesson_id: uuid.UUID, payload: LessonUpdate,
    current: CurrentUser = Depends(require_permission("tracks.update")),
    db: Session = Depends(get_db),
):
    return lessons_service.update_lesson(db, lesson_id, payload, current.id)


@router.delete("/{lesson_id}", status_code=204)
def delete_lesson(
    lesson_id: uuid.UUID,
    current: CurrentUser = Depends(require_permission("tracks.delete")),
    db: Session = Depends(get_db),
):
    lessons_service.delete_lesson(db, lesson_id, current.id)


@router.post("/{lesson_id}/progress")
def update_progress(
    lesson_id: uuid.UUID, payload: ProgressUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Met à jour la progression de l'utilisateur authentifié sur cette leçon."""
    return lessons_service.update_progress(db, current.id, lesson_id, payload)
