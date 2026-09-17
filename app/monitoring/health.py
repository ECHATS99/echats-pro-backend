"""Vérifications de santé agrégées (DB, Redis) pour /health et /status (Partie 5.32 du SRS)."""
from app.core.database import engine
from app.core.redis import get_redis_client


def check_database() -> bool:
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return True
    except Exception:
        return False


def check_redis() -> bool:
    try:
        return get_redis_client().ping()
    except Exception:
        return False


def full_health_report() -> dict:
    db_ok = check_database()
    redis_ok = check_redis()
    return {
        "status": "ok" if (db_ok and redis_ok) else "degraded",
        "database": "ok" if db_ok else "down",
        "redis": "ok" if redis_ok else "down",
    }
