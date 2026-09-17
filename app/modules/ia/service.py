"""Logique métier du domaine 'ia'. ECHATS PRO ne possède aucun modèle IA : ce module est
un proxy sécurisé vers api.echats.ai (Partie 8.11 du SRS), avec RAG (contexte leçon/exercice
injecté), quotas par plan, et prompts système modifiables depuis l'admin sans redéploiement.
"""
import uuid

from app.core.exceptions import NotFoundError, QuotaExceededError
from app.integrations.echats_ai.client import chat_completion
from app.integrations.echats_ai.exceptions import EchatsAIError
from app.modules.ia import repository as ia_repo
from app.modules.ia.schemas import ChatRequest, ChatResponse, IAPromptUpdate
from app.modules.lessons import repository as lessons_repo
from app.modules.subscriptions import repository as subscriptions_repo


def _build_rag_context(db, payload: ChatRequest) -> dict:
    context: dict = {}
    if payload.lesson_id:
        try:
            lesson = lessons_repo.get_by_id(db, uuid.UUID(payload.lesson_id))
            if lesson:
                context["lesson_title"] = lesson.title
                context["lesson_content_excerpt"] = (lesson.content or "")[:2000]
        except ValueError:
            pass
    if payload.exercise_id:
        context["exercise_id"] = payload.exercise_id
    return context


def _check_and_consume_quota(db, user_id: uuid.UUID) -> int:
    subscription = subscriptions_repo.get_active_for_user(db, user_id)
    max_requests = subscription.plan.max_ai_requests_per_day if subscription else 10  # quota GO par défaut

    used = ia_repo.get_daily_usage(user_id)
    if used >= max_requests:
        raise QuotaExceededError("Quota de requêtes IA journalier atteint pour votre plan.")

    used = ia_repo.increment_daily_usage(user_id)
    return max(0, max_requests - used)


def chat(db, context: str, payload: ChatRequest, user_id: uuid.UUID) -> ChatResponse:
    """Chemin générique utilisé par /ia/cyber, /ia/go, /ia/nexo."""
    remaining = _check_and_consume_quota(db, user_id)
    system_prompt = ia_repo.get_or_default_prompt(db, context)
    rag_context = _build_rag_context(db, payload) if context == "cyber" else {}

    try:
        reply = chat_completion(system_prompt, payload.message, rag_context)
    except EchatsAIError as exc:
        reply = f"Le service IA est momentanément indisponible ({exc}). Réessayez dans quelques instants."

    return ChatResponse(reply=reply, context=context, remaining_quota=remaining)


def update_prompt(db, context: str, payload: IAPromptUpdate, actor_id: uuid.UUID):
    from app.services.audit_service import log_action
    prompt = ia_repo.upsert_prompt(db, context, payload.system_prompt, payload.model, payload.active)
    log_action(db, user_id=actor_id, action="ia.prompt_updated", module="ia", resource="ia_prompt", resource_id=str(prompt.id))
    return {"context": prompt.context, "system_prompt": prompt.system_prompt, "active": prompt.active}
