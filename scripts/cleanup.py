"""Nettoyage manuel à la demande (fichiers temporaires, sessions expirées, labs inactifs).
Complète le cleanup_worker automatique (toutes les 15 min via le scheduler).

Usage : python -m scripts.cleanup
"""
from app.workers.cleanup_worker import run_once


def main() -> None:
    run_once()
    print("Nettoyage manuel terminé.")


if __name__ == "__main__":
    main()
