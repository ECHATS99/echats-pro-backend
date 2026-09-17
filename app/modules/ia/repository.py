"""Accès aux données du domaine 'ia' via SQLAlchemy et Redis (quotas journaliers)."""
import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.redis import get_redis_client
from app.models.ia_prompt import IAPrompt

DEFAULT_PROMPTS = {
    "cyber": "Tu es l'assistant expert en cybersécurité d'ECHATS PRO. Tu aides l'apprenant sur ses cours, "
             "modules et CTF, en t'appuyant sur le contexte de la leçon ou de l'exercice en cours.",
    "go": "Tu es l'assistant de navigation général d'ECHATS PRO (onboarding, support, questions générales "
          "sur la plateforme BLACKHAWK LAB).",
    "nexo": "Tu es Nexo, l'assistant commercial de Nexoshop sur ECHATS PRO (produits, commandes, boutiques partenaires).",
}


def get_prompt(db: Session, context: str) -> IAPrompt | None:
    stmt = select(IAPrompt).where(IAPrompt.context == context, IAPrompt.active.is_(True))
    return db.execute(stmt).scalar_one_or_none()


def get_or_default_prompt(db: Session, context: str) -> str:
    prompt = get_prompt(db, context)
    if prompt:
        return prompt.system_prompt
    return DEFAULT_PROMPTS.get(context, DEFAULT_PROMPTS["go"])


def upsert_prompt(db: Session, context: str, system_prompt: str, model: str | None, active: bool) -> IAPrompt:
    prompt = db.execute(select(IAPrompt).where(IAPrompt.context == context)).scalar_one_or_none()
    if prompt is None:
        prompt = IAPrompt(context=context, system_prompt=system_prompt, model=model, active=active)
    else:
        prompt.system_prompt = system_prompt
        prompt.model = model
        prompt.active = active
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


def _quota_key(user_id: uuid.UUID) -> str:
    return f"ia_quota:{user_id}:{date.today().isoformat()}"


def get_daily_usage(user_id: uuid.UUID) -> int:
    raw = get_redis_client().get(_quota_key(user_id))
    return int(raw) if raw else 0


def increment_daily_usage(user_id: uuid.UUID) -> int:
    client = get_redis_client()
    key = _quota_key(user_id)
    value = client.incr(key)
    if value == 1:
        client.expire(key, 86400)
    return value
