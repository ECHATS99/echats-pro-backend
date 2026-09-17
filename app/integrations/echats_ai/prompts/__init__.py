"""Prompts système ECHATS IA — Modèle GO CYBER."""
from .go_cyber import GO_CYBER_PROMPT

PROMPTS = {
    "cyber": GO_CYBER_PROMPT,
    "go": GO_CYBER_PROMPT,
    "nexo": GO_CYBER_PROMPT,
}

def get_prompt(context: str | None = None) -> str:
    return GO_CYBER_PROMPT
