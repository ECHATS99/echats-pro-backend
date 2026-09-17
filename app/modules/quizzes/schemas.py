"""Schémas Pydantic pour le domaine 'quizzes'."""
import uuid

from pydantic import BaseModel, Field


class AnswerCreate(BaseModel):
    answer: str = Field(min_length=1, max_length=500)
    correct: bool = False


class QuestionCreate(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    type: str = Field(default="single_choice", pattern="^(single_choice|multi_choice|true_false)$")
    answers: list[AnswerCreate] = Field(min_length=2)


class QuizCreate(BaseModel):
    lesson_id: uuid.UUID
    title: str = Field(min_length=3, max_length=200)
    passing_score: int = Field(default=70, ge=0, le=100)
    questions: list[QuestionCreate] = Field(default_factory=list)


class AnswerPublicOut(BaseModel):
    """Vue publique d'une réponse : ne révèle jamais si elle est correcte avant soumission."""
    id: uuid.UUID
    answer: str

    model_config = {"from_attributes": True}


class QuestionPublicOut(BaseModel):
    id: uuid.UUID
    question: str
    type: str
    answers: list[AnswerPublicOut]

    model_config = {"from_attributes": True}


class QuizPublicOut(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    title: str
    passing_score: int
    questions: list[QuestionPublicOut]

    model_config = {"from_attributes": True}


class QuizAttempt(BaseModel):
    """answers: {question_id: [answer_id, ...]}"""
    answers: dict[uuid.UUID, list[uuid.UUID]]


class QuizResult(BaseModel):
    score: int
    passed: bool
    correct_count: int
    total_questions: int
