"""Applique quotas par plan, injecte le contexte RAG (leçon/exercice en cours),
appelle integrations/echats_ai, journalise l'usage.

Façade fine : la logique complète vit dans app.modules.ia (quotas Redis par jour,
prompts modifiables depuis l'admin, RAG). Ce module réexporte le point d'entrée `chat`
pour les autres services partagés qui auraient besoin d'appeler l'IA sans dépendre
directement de la couche HTTP du domaine `ia`.
"""
from app.modules.ia.service import chat as chat_with_ia  # noqa: F401
