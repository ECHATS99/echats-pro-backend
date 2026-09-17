"""Schémas Pydantic pour le domaine 'labs'."""
import uuid

from pydantic import BaseModel, Field


class LabCreateRequest(BaseModel):
    exercise_id: uuid.UUID
    kind: str = Field(pattern="^(judge0|codespaces)$", description="judge0 pour les exercices légers, codespaces pour les labs complexes.")
    repository: str | None = Field(default=None, description="Requis si kind='codespaces' (org/repo).")


class LabSessionOut(BaseModel):
    lab_id: str
    kind: str
    status: str
    web_url: str | None = None
    expires_in_seconds: int


class LabWebSocketTicketOut(BaseModel):
    ticket: str
    expires_in_seconds: int
