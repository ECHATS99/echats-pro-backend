"""Routes HTTP /api/v1/news."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.news import service as news_service
from app.modules.news.schemas import NewsArticleOut

router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
def list_news(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), category: str | None = None, db: Session = Depends(get_db)):
    return news_service.list_news(db, page, limit, category)


@router.get("/latest", response_model=list[NewsArticleOut])
def latest(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    return news_service.list_latest(db, limit)


@router.get("/category", response_model=list[NewsArticleOut])
def by_category(category: str, limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    result = news_service.list_news(db, 1, limit, category)
    return result["data"]


@router.post("/refresh")
def refresh(current: CurrentUser = Depends(require_permission("admin.access")), db: Session = Depends(get_db)):
    return news_service.force_refresh(db)
