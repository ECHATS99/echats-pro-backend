"""Déclenche une sauvegarde manuelle à la demande (en complément du cron nocturne —
Partie 7.8 du SRS). Le dump PostgreSQL complet reste délégué à `pg_dump` en dehors du
process applicatif (voir app/workers/backup_worker.py pour le détail et sa justification).

Usage : python -m scripts.backup
"""
import subprocess
import sys
from datetime import datetime, timezone

from app.core.settings import settings
from app.workers.backup_worker import run_once as backup_redis_snapshot


def dump_postgres() -> str | None:
    """Lance pg_dump si l'utilitaire est disponible sur la machine exécutant le script."""
    filename = f"backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.sql"
    try:
        with open(filename, "wb") as f:
            result = subprocess.run(["pg_dump", settings.DATABASE_URL], stdout=f, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(result.stderr.decode(), file=sys.stderr)
            return None
        return filename
    except FileNotFoundError:
        print("pg_dump introuvable sur cette machine — sauvegarde PostgreSQL ignorée.", file=sys.stderr)
        return None


def main() -> None:
    pg_file = dump_postgres()
    if pg_file:
        print(f"Dump PostgreSQL créé : {pg_file}")

    redis_key = backup_redis_snapshot()
    if redis_key:
        print(f"Snapshot Redis créé : {redis_key}")

    if not pg_file and not redis_key:
        print("Aucune sauvegarde n'a pu être créée.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
