"""Schémas Pydantic pour le domaine 'search'."""
import uuid

from pydantic import BaseModel


class SearchResultItem(BaseModel):
    type: str  # track|ctf|product|user|writeup
    id: uuid.UUID
    title: str
    subtitle: str | None = None


class SearchResults(BaseModel):
    query: str
    tracks: list[SearchResultItem] = []
    ctf: list[SearchResultItem] = []
    products: list[SearchResultItem] = []
    users: list[SearchResultItem] = []
