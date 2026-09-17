"""Logique métier du domaine 'search'. Recherche globale (cours, challenges, users, writeups...)."""
from app.modules.search import repository as search_repo
from app.modules.search.schemas import SearchResultItem, SearchResults

MIN_QUERY_LENGTH = 2


def global_search(db, q: str) -> SearchResults:
    if len(q.strip()) < MIN_QUERY_LENGTH:
        return SearchResults(query=q)

    return SearchResults(
        query=q,
        tracks=[SearchResultItem(type="track", id=t.id, title=t.title, subtitle=t.domain) for t in search_repo.search_tracks(db, q)],
        ctf=[SearchResultItem(type="ctf", id=c.id, title=c.title, subtitle=c.difficulty) for c in search_repo.search_ctf(db, q)],
        products=[SearchResultItem(type="product", id=p.id, title=p.name, subtitle=f"{p.price_fcfa} FCFA") for p in search_repo.search_products(db, q)],
        users=[SearchResultItem(type="user", id=u.id, title=u.username, subtitle=u.country) for u in search_repo.search_users(db, q)],
    )


def search_scoped(db, q: str, scope: str) -> list[SearchResultItem]:
    if scope == "courses":
        return [SearchResultItem(type="track", id=t.id, title=t.title, subtitle=t.domain) for t in search_repo.search_tracks(db, q)]
    if scope == "ctf":
        return [SearchResultItem(type="ctf", id=c.id, title=c.title, subtitle=c.difficulty) for c in search_repo.search_ctf(db, q)]
    if scope == "products":
        return [SearchResultItem(type="product", id=p.id, title=p.name) for p in search_repo.search_products(db, q)]
    if scope == "users":
        return [SearchResultItem(type="user", id=u.id, title=u.username) for u in search_repo.search_users(db, q)]
    return []
