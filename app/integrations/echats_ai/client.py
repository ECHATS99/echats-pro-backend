"""Client bas niveau pour api.echats.ai. SEUL point de contact avec l'infrastructure IA.
Toutes les requêtes IA passent ici, jamais directement depuis un autre module
(Partie 5 / 8.11 du SRS : ECHATS PRO ne possède aucun modèle IA, il agit en proxy sécurisé).
"""
import httpx

from app.core.settings import settings
from app.integrations.echats_ai.exceptions import EchatsAIError


def chat_completion(system_prompt: str, message: str, context: dict | None = None) -> str:
    """Appelle api.echats.ai/api/v1/chat et retourne la réponse texte de l'assistant."""
    if not settings.ECHATS_AI_BACKEND_URL:
        raise EchatsAIError("ECHATS_AI_BACKEND_URL n'est pas configuré.")

    try:
        headers = {"Content-Type": "application/json"}
        if settings.ECHATS_AI_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ECHATS_AI_API_KEY}"
        response = httpx.post(
            f"{settings.ECHATS_AI_BACKEND_URL}/api/v1/chat",
            headers=headers,
            json={"system_prompt": system_prompt, "message": message, "context": context or {}},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["reply"]
    except Exception as exc:
        raise EchatsAIError(f"Échec de l'appel à api.echats.ai : {exc}") from exc


def sync_knowledge(payload: dict) -> None:
    """Synchronise un nouvel élément de contenu (cours, module, leçon, CTF, writeup)
    vers l'index de connaissances d'api.echats.ai (Partie 7 du SRS Partie 1)."""
    if not settings.ECHATS_AI_BACKEND_URL:
        return
    try:
        httpx.post(
            f"{settings.ECHATS_AI_BACKEND_URL}/api/v1/assistant/sync",
            headers={"Authorization": f"Bearer {settings.ECHATS_AI_API_KEY}"},
            json=payload, timeout=10.0,
        )
    except Exception:
        import logging
        logging.getLogger("echats.ia").warning("Échec de synchronisation vers api.echats.ai (non bloquant).")
