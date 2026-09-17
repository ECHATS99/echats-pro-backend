"""Restaure la base PostgreSQL à partir d'un dump généré par scripts/backup.py.

ATTENTION : action destructive et irréversible sur la base cible. À utiliser uniquement
en cas de sinistre (Partie 7.9 du SRS : Plan de reprise), jamais en production sans
confirmation manuelle explicite.

Usage : python -m scripts.restore --file backup_20260730_120000.sql
"""
import argparse
import subprocess
import sys

from app.core.settings import settings


def restore_postgres(filepath: str) -> None:
    confirm = input(f"Ceci va ÉCRASER la base '{settings.DATABASE_URL}' avec le contenu de "
                     f"'{filepath}'. Taper OUI en majuscules pour confirmer : ")
    if confirm != "OUI":
        print("Restauration annulée.")
        sys.exit(0)

    with open(filepath, "rb") as f:
        result = subprocess.run(["psql", settings.DATABASE_URL], stdin=f, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode(), file=sys.stderr)
        sys.exit(result.returncode)
    print("Restauration terminée.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Chemin du fichier de dump SQL à restaurer")
    args = parser.parse_args()
    restore_postgres(args.file)
