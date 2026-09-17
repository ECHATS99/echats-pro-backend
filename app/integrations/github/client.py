"""Client bas niveau pour GitHub API : création/destruction de sessions Codespaces
pour les labs complexes (Forensic, Pentest, Reverse Engineering)."""
import httpx

from app.core.settings import settings
from app.integrations.github.exceptions import GitHubCodespacesError

GITHUB_API_URL = "https://api.github.com"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def create_codespace(repository: str, machine: str = "basicLinux32gb", ref: str = "main") -> dict:
    try:
        response = httpx.post(
            f"{GITHUB_API_URL}/repos/{repository}/codespaces",
            headers=_headers(),
            json={"ref": ref, "machine": machine, "idle_timeout_minutes": 30},
            timeout=20.0,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        raise GitHubCodespacesError(f"Échec de création du Codespace : {exc}") from exc

    return {"id": data["name"], "web_url": data.get("web_url"), "state": data.get("state")}


def stop_codespace(codespace_name: str) -> None:
    try:
        response = httpx.post(
            f"{GITHUB_API_URL}/user/codespaces/{codespace_name}/stop",
            headers=_headers(), timeout=15.0,
        )
        response.raise_for_status()
    except Exception as exc:
        raise GitHubCodespacesError(f"Échec de l'arrêt du Codespace : {exc}") from exc


def delete_codespace(codespace_name: str) -> None:
    try:
        response = httpx.delete(f"{GITHUB_API_URL}/user/codespaces/{codespace_name}", headers=_headers(), timeout=15.0)
        response.raise_for_status()
    except Exception as exc:
        raise GitHubCodespacesError(f"Échec de la suppression du Codespace : {exc}") from exc
