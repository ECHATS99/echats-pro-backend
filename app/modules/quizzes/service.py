"""Logique métier du domaine 'quizzes' : création, passage, correction."""
import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.models.quiz import Answer, Question, Quiz
from app.modules.quizzes import repository as quizzes_repo
from app.modules.quizzes.schemas import QuizAttempt, QuizCreate, QuizPublicOut, QuizResult
from app.services.audit_service import log_action

QUIZ_XP_REWARD = 15


def create_quiz(db: Session, payload: QuizCreate, actor_id: uuid.UUID) -> QuizPublicOut:
    quiz = Quiz(lesson_id=payload.lesson_id, title=payload.title, passing_score=payload.passing_score)
    for q in payload.questions:
        question = Question(question=q.question, type=q.type)
        question.answers = [Answer(answer=a.answer, correct=a.correct) for a in q.answers]
        quiz.questions.append(question)

    quiz = quizzes_repo.create(db, quiz)
    log_action(db, user_id=actor_id, action="quiz.created", module="quizzes", resource="quiz", resource_id=str(quiz.id))
    return QuizPublicOut.model_validate(quiz)


def get_quiz_for_lesson(db: Session, lesson_id: uuid.UUID) -> QuizPublicOut:
    quiz = quizzes_repo.get_by_lesson(db, lesson_id)
    if quiz is None:
        raise NotFoundError("Aucun quiz pour cette leçon.")
    return QuizPublicOut.model_validate(quiz)


def delete_quiz(db: Session, quiz_id: uuid.UUID, actor_id: uuid.UUID) -> None:
    quiz = quizzes_repo.get_by_id(db, quiz_id)
    if quiz is None:
        raise NotFoundError("Quiz introuvable.")
    quizzes_repo.delete(db, quiz)
    log_action(db, user_id=actor_id, action="quiz.deleted", module="quizzes", resource="quiz", resource_id=str(quiz_id))


def submit_attempt(db: Session, quiz_id: uuid.UUID, user_id: uuid.UUID, attempt: QuizAttempt) -> QuizResult:
    """Corrige une tentative de quiz côté serveur (jamais côté client). Une question à choix
    multiple est correcte seulement si l'ensemble des réponses sélectionnées correspond
    exactement à l'ensemble des réponses correctes.
    """
    quiz = quizzes_repo.get_by_id(db, quiz_id)
    if quiz is None:
        raise NotFoundError("Quiz introuvable.")
    if not quiz.questions:
        raise ValidationError("Ce quiz ne contient aucune question.")

    correct_count = 0
    for question in quiz.questions:
        correct_answer_ids = {a.id for a in question.answers if a.correct}
        submitted_ids = set(attempt.answers.get(question.id, []))
        if submitted_ids == correct_answer_ids:
            correct_count += 1

    total = len(quiz.questions)
    score = round((correct_count / total) * 100)
    passed = score >= quiz.passing_score

    if passed:
        from app.services.xp_service import award_xp
        award_xp(db, user_id, QUIZ_XP_REWARD, f"quiz_passed:{quiz_id}")

    log_action(db, user_id=user_id, action="quiz.attempted", module="quizzes", resource="quiz", resource_id=str(quiz_id), new_value={"score": score, "passed": passed})
    return QuizResult(score=score, passed=passed, correct_count=correct_count, total_questions=total)
