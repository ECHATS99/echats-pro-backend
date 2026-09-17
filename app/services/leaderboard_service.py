"""Calcul et mise à jour du classement (Redis + WebSocket).

Façade fine : la logique complète (requêtes SQL, cache, pagination) vit dans
app.modules.leaderboard (respect de la séparation domaine / services partagés). Ce module
expose uniquement le point d'entrée "notifier le classement" utilisé par les domaines qui
font varier le score (ctf, exercises) sans qu'ils aient à connaître le détail du domaine
leaderboard.
"""
from app.services.cache_service import cache_delete_prefix
from app.services.websocket_service import broadcast_leaderboard_update


def invalidate_and_broadcast(event: str, **payload) -> None:
    """Invalide le cache du classement et notifie les clients connectés en temps réel."""
    cache_delete_prefix("leaderboard:global")
    broadcast_leaderboard_update({"event": event, **payload})
