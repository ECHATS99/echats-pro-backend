"""Schémas Pydantic pour le domaine 'ia'."""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    lesson_id: str | None = Field(default=None, description="Injecté en RAG pour le contexte cyber.")
    exercise_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    context: str  # cyber|go|nexo
    remaining_quota: int


class IAPromptUpdate(BaseModel):
    system_prompt: str = Field(min_length=1)
    model: str | None = None
    active: bool = True
