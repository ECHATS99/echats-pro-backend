"""Routes HTTP /api/v1/search."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.modules.search import service as search_service
from app.modules.search.schemas import SearchResultItem, SearchResults

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResults)
def search(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return search_service.global_search(db, q)


@router.get("/courses", response_model=list[SearchResultItem])
def search_courses(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return search_service.search_scoped(db, q, "courses")


@router.get("/ctf", response_model=list[SearchResultItem])
def search_ctf(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return search_service.search_scoped(db, q, "ctf")


@router.get("/products", response_model=list[SearchResultItem])
def search_products(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return search_service.search_scoped(db, q, "products")


@router.get("/users", response_model=list[SearchResultItem])
def search_users(q: str = Query(min_length=1), db: Session = Depends(get_db)):
    return search_service.search_scoped(db, q, "users")
