"""Logique métier du domaine 'news'. Consultation paginée du flux RSS agrégé côté backend
(Partie 11 du SRS : jamais d'appel RSS direct depuis le frontend)."""
from app.modules.news import repository as news_repo
from app.modules.news.schemas import NewsArticleOut
from app.services.rss_service import refresh_all_feeds
from app.utils.pagination import paginate


def list_news(db, page: int, limit: int, category: str | None):
    items, total = news_repo.list_news(db, page, limit, category)
    return paginate([NewsArticleOut.model_validate(a).model_dump() for a in items], page, limit, total)


def list_latest(db, limit: int) -> list[NewsArticleOut]:
    return [NewsArticleOut.model_validate(a) for a in news_repo.list_latest(db, limit)]


def force_refresh(db) -> dict:
    """Déclenche manuellement un rafraîchissement RSS (admin), en plus du cycle horaire automatique."""
    count = refresh_all_feeds(db)
    return {"new_articles": count}
