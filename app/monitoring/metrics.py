"""Compteurs et mesures in-process exposés sur /metrics (format compatible Prometheus texte).
Pour une observabilité multi-workers en production, faire pointer ces compteurs vers Redis
(INCR) plutôt qu'un dict en mémoire — l'API publique ci-dessous resterait identique."""
import time
from collections import defaultdict

_counters: dict[str, int] = defaultdict(int)
_start_time = time.time()


def increment(name: str, value: int = 1) -> None:
    _counters[name] += value


def get_counter(name: str) -> int:
    return _counters.get(name, 0)


def uptime_seconds() -> float:
    return time.time() - _start_time


def render_prometheus() -> str:
    """Rend les compteurs au format texte Prometheus (name value)."""
    lines = [f"echats_uptime_seconds {uptime_seconds():.2f}"]
    for name, value in _counters.items():
        safe_name = f"echats_{name.replace('.', '_')}"
        lines.append(f"{safe_name} {value}")
    return "\n".join(lines) + "\n"
