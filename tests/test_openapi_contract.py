"""Régression : OpenAPI doit rester sérialisable et Swagger UI doit être servi."""

import json
import os

# L'import de l'application construit le moteur SQLAlchemy dès le chargement.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://openapi:openapi@127.0.0.1:5432/openapi",
)

from fastapi.testclient import TestClient

from app.main import app


def test_openapi_json_and_docs_are_valid():
    with TestClient(app) as client:
        openapi_response = client.get("/openapi.json")
        docs_response = client.get("/docs")

    assert openapi_response.status_code == 200
    assert docs_response.status_code == 200
    payload = openapi_response.json()
    assert payload["openapi"].startswith("3.")
    assert payload["paths"]
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    json.loads(serialized)
    forbidden_fragments = (
        '\"summary\":\"Health\"\",\"description\"',
        '\"description\":\"Réponse réussie Réponse,\"content\"',
        '\"Réussi Réponse,',
        '\"Erreur de validation,',
    )
    assert not any(fragment in serialized for fragment in forbidden_fragments)
    assert "swagger-ui" in docs_response.text.lower()
