"""Point d'entrée FastAPI. Crée l'app, enregistre les routers, les middlewares, le lifespan,
CORS, exception handlers.
"""
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.settings import settings
from app.lifespan import lifespan
from app.middlewares.cors import add_cors_middleware
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.middlewares.timing import TimingMiddleware
from app.websocket import activity, classroom, leaderboard, notifications, terminal

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Middlewares — l'ordre est important : appliqués en LIFO pour la requête entrante.
add_cors_middleware(app)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
, prefix=settings.API_V1_PREFIX)

# Canaux WebSocket temps réel (Partie 14 du SRS) — hors préfixe /api/v1, montés à la racine.
app.include_router(notifications.router)
app.include_router(leaderboard.router)
app.include_router(activity.router)
app.include_router(classroom.router)
app.include_router(terminal.router)
