"""Helper de pagination standard (page/limit/total/pages) — voir Partie 5.6 du SRS."""
from typing import Any, Sequence

from pydantic import BaseModel


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    pages: int


class PaginatedResponse(BaseModel):
    data: list[Any]
    meta: PaginationMeta


def build_pagination_meta(page: int, limit: int, total: int) -> PaginationMeta:
    pages = (total + limit - 1) // limit if limit > 0 else 0
    return PaginationMeta(page=page, limit=limit, total=total, pages=pages)


def paginate(items: Sequence[Any], page: int, limit: int, total: int) -> dict:
    return {
        "data": list(items),
        "meta": build_pagination_meta(page, limit, total).model_dump(),
    }
