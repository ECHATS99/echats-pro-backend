"""Client bas niveau pour Judge0 : exécution de code sandboxée pour les exercices/CTF légers."""
import base64
import time

import httpx

from app.core.settings import settings
from app.integrations.judge0.exceptions import Judge0Error

# Sous-ensemble des language_id Judge0 les plus utilisés sur la plateforme.
LANGUAGE_IDS = {
    "python": 71, "c": 50, "cpp": 54, "java": 62, "bash": 46, "javascript": 63,
}


def submit_code(source_code: str, language: str, stdin: str = "") -> dict:
    """Soumet du code à Judge0 en mode synchrone (wait=true) et retourne le résultat.
    Chaque soumission est une sandbox isolée, détruite après exécution (Partie 7 du SRS).
    """
    language_id = LANGUAGE_IDS.get(language.lower())
    if language_id is None:
        raise Judge0Error(f"Langage non supporté par Judge0 : {language}")

    if not settings.JUDGE0_API_URL:
        raise Judge0Error("JUDGE0_API_URL n'est pas configuré.")

    try:
        response = httpx.post(
            f"{settings.JUDGE0_API_URL}/submissions?wait=true&base64_encoded=true",
            json={
                "source_code": base64.b64encode(source_code.encode()).decode(),
                "language_id": language_id,
                "stdin": base64.b64encode(stdin.encode()).decode() if stdin else "",
            },
            timeout=20.0,
        )
        response.raise_for_status()
        result = response.json()
    except Exception as exc:
        raise Judge0Error(f"Échec de la soumission Judge0 : {exc}") from exc

    def _decode(field: str) -> str | None:
        value = result.get(field)
        if not value:
            return value
        return base64.b64decode(value).decode(errors="replace")

    return {
        "stdout": _decode("stdout"),
        "stderr": _decode("stderr"),
        "compile_output": _decode("compile_output"),
        "status": result.get("status", {}).get("description"),
        "time": result.get("time"),
        "memory": result.get("memory"),
    }
