"""Bus d'évènements in-process minimal (Partie 2.14 du SRS : communication inter-modules
par évènements plutôt que par appel direct). Chaque évènement du dossier events/ définit son
propre payload et ses propres abonnés ; ce bus ne fait que le routage générique.

Limite assumée : in-process uniquement (pas de file distribuée). Suffisant pour un backend
mono-service ; à remplacer par Redis Pub/Sub ou une queue dédiée si plusieurs services
consomment ces évènements indépendamment du process API.
"""
from collections import defaultdict
from typing import Callable

_subscribers: dict[str, list[Callable]] = defaultdict(list)


def subscribe(event_name: str, handler: Callable) -> None:
    _subscribers[event_name].append(handler)


def publish(event_name: str, **payload) -> None:
    """Diffuse un évènement à tous les abonnés. Chaque handler est exécuté de façon isolée :
    l'échec d'un abonné ne doit jamais empêcher les autres de s'exécuter ni remonter d'erreur
    à l'appelant (les évènements sont un mécanisme best-effort, pas transactionnel)."""
    import logging
    logger = logging.getLogger("echats.events")
    for handler in _subscribers.get(event_name, []):
        try:
            handler(**payload)
        except Exception:
            logger.exception("Échec du handler pour l'évènement '%s'.", event_name)
