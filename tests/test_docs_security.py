"""Vérifie que les assets de documentation sont autorisés sans relâcher la CSP globale."""

import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://openapi:openapi@127.0.0.1:5432/openapi",
)

from fastapi.testclient import TestClient

from app.main import app
from app.security.headers import SECURITY_HEADERS


def test_docs_and_redoc_have_targeted_csp_allowlist():
    with TestClient(app) as client:
        docs_headers = client.get("/docs").headers
        redoc_headers = client.get("/redoc").headers
        api_headers = client.get("/api/v1/health").headers

    for headers in (docs_headers, redoc_headers):
        csp = headers["content-security-policy"]
        assert "https://cdn.jsdelivr.net" in csp
        assert "'unsafe-inline'" in csp
        assert "frame-ancestors 'none'" in csp

    assert api_headers["content-security-policy"] == SECURITY_HEADERS["Content-Security-Policy"]
    assert "https://cdn.jsdelivr.net" not in api_headers["content-security-policy"]
