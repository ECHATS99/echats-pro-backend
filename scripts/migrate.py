"""Applique les migrations Alembic en attente (wrapper simple pour les déploiements
et le CI/CD — Partie 7.14 du SRS : aucun déploiement si les migrations échouent).

Usage : python -m scripts.migrate
"""
import subprocess
import sys


def main() -> None:
    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    print("Migrations appliquées avec succès.")


if __name__ == "__main__":
    main()
