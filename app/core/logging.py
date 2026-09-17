"""Configuration de la journalisation structurée de l'application."""
import logging
import sys

from app.core.settings import settings


def configure_logging() -> None:
    """Configure le logging global de l'application (format, niveau, sortie stdout)."""
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    formatter = logging.Formatter(
        fmt='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]

    # Réduit le bruit des libs tierces
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
