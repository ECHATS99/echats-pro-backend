"""Injecte les headers de sécurité HTTP sur chaque réponse."""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.security.headers import SECURITY_HEADERS


DOCS_CSP = (
    "default-src 'self'; "
    "img-src 'self' https://res.cloudinary.com https://fastapi.tiangolo.com data:; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com 'unsafe-inline'; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "connect-src 'self'; frame-ancestors 'none'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        headers = SECURITY_HEADERS
        if request.url.path in {"/docs", "/redoc"}:
            # Swagger UI/ReDoc utilisent des assets CDN et un bootstrap inline.
            # Cette exception reste limitée aux deux pages de documentation.
            headers = {**SECURITY_HEADERS, "Content-Security-Policy": DOCS_CSP}
        for key, value in headers.items():
            response.headers[key] = value
        return response
