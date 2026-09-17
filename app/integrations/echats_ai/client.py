"""Client IA ECHATS — proxy sécurisé. Modèle public : ECHATS IA GO CYBER.
Développé par BLACKHAWK LAB. Fournisseur interne non exposé.
"""
import logging
import re

import httpx

from app.core.settings import settings
from app.integrations.echats_ai.exceptions import EchatsAIError
from app.integrations.echats_ai.prompts import get_prompt

logger = logging.getLogger("echats.ia")

# Blocage : demandes illégales
_BLOCKED_PATTERNS = [
    r"\b(creer|créer|fabriquer|generer|générer|coder|developper|développer)\s+(un|le|des|du)\s+(virus|malware|ransomware|trojan|rootkit|keylogger|spyware|botnet)",
    r"\b(ddos|deni\s+de\s+service|déni\s+de\s+service)\s+(contre|sur|vers)\s+",
    r"\b(attaquer|exploiter|hacker|pirater)\s+(?:le\s+|la\s+|les\s+|un\s+|une\s+)?(site|serveur|compte|systeme|système|reseau|réseau|api)\s+(de|d|du)\s+",
    r"\b(doxxer|dox|swatting)\b",
    r"\b(pedophil|pédophil|terroris|trafic\s+d.etres\s+humains)",
    r"\b(contourner|bypasser|casser)\s+(l.authentification|le\s+pare-?feu|le\s+waf|la\s+2fa)",
]

# Injection de prompt
_INJECTION_PATTERNS = [
    r"ignore\s+(toutes?\s+)?(les\s+)?instructions?\s+(precedentes?|précédentes?|ci-dessus)",
    r"ignore\s+previous\s+instructions",
    r"tu\s+es\s+maintenant\s+(?!echats)",
    r"fais\s+semblant\s+d.etre",
    r"mode\s+developpeur|mode\s+développeur",
    r"system\s*:\s*",
    r"<\|\s*im_start\s*\|>",
    r"<\|\s*system\s*\|>",
    r"\[\s*system\s*\]",
]

# Attaques contre la plateforme
_PLATFORM_ATTACK_PATTERNS = [
    r"(attaquer|injecter|cracker)\s+(echats|la\s+plateforme|le\s+site|la\s+base)",
    r"\b(sql\s*injection|sqli|xss|xxe|csrf|rce)\s+(sur|contre|dans)\s+echats",
]


def _sanitize_input(message: str) -> str:
    if not message:
        raise EchatsAIError("Message vide.")
    message = message.strip()
    if len(message) > settings.IA_MAX_MESSAGE_LENGTH:
        message = message[: settings.IA_MAX_MESSAGE_LENGTH]
    return message


def _check_safety(message: str) -> None:
    low = message.lower()

    for pattern in _INJECTION_PATTERNS:
        if re.search(pattern, low, re.IGNORECASE):
            logger.warning("Injection prompt detectee")
            raise EchatsAIError("Message refuse : tentative de manipulation detectee.")

    for pattern in _PLATFORM_ATTACK_PATTERNS:
        if re.search(pattern, low, re.IGNORECASE):
            logger.warning("Attaque plateforme detectee")
            raise EchatsAIError(
                "Cette action est contraire aux conditions d'utilisation d'ECHATS PRO. Je ne peux pas vous assister sur ce point."
            )

    for pattern in _BLOCKED_PATTERNS:
        if re.search(pattern, low, re.IGNORECASE):
            logger.warning("Demande illegale bloquee : %s", pattern)
            raise EchatsAIError(
                "Je ne peux pas vous aider sur ce point. ECHATS PRO promeut uniquement la cybersecurite ethique et legale."
            )


def _post_filter(reply: str) -> str:
    """Masque toute reference a un fournisseur externe ou a une personne physique."""
    forbidden = [
        "groq", "llama", "meta-llama", "gpt-oss", "openai", "gemini",
        "anthropic", "claude", "mistral", "mikabou", "elioth",
    ]
    for word in forbidden:
        reply = re.sub(rf"\b{re.escape(word)}\b", "ECHATS IA", reply, flags=re.IGNORECASE)
    return reply


def chat_completion(
    system_prompt: str | None,
    message: str,
    context: dict | None = None,
    assistant_type: str = "cyber",
) -> str:
    """Appelle le fournisseur IA interne et retourne la reponse ECHATS IA."""
    if not settings.GROQ_API_KEY:
        raise EchatsAIError("Service IA indisponible.")

    message = _sanitize_input(message)
    _check_safety(message)

    base_prompt = system_prompt or get_prompt(assistant_type)

    context_str = ""
    if context:
        if context.get("lesson_title"):
            context_str += f"\n\n[Contexte lecon: {context['lesson_title']}]"
        if context.get("lesson_content_excerpt"):
            context_str += f"\n{context['lesson_content_excerpt'][:1500]}"

    full_system = base_prompt + context_str

    try:
        response = httpx.post(
            f"{settings.GROQ_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": full_system},
                    {"role": "user", "content": message},
                ],
                "temperature": settings.IA_TEMPERATURE,
                "max_tokens": settings.IA_MAX_TOKENS,
            },
            timeout=settings.IA_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return _post_filter(reply)

    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status == 401:
            raise EchatsAIError("Service IA mal configure.") from exc
        if status == 429:
            raise EchatsAIError("Quota momentanement atteint. Reessayez dans un instant.") from exc
        raise EchatsAIError(f"Erreur service IA ({status}).") from exc
    except httpx.TimeoutException as exc:
        raise EchatsAIError("L'assistant met trop de temps a repondre.") from exc
    except Exception as exc:
        logger.exception("Erreur IA inattendue")
        raise EchatsAIError("Erreur interne du service IA.") from exc


def sync_knowledge(payload: dict) -> None:
    """No-op — conserve pour compat avec le scheduler."""
    return None
