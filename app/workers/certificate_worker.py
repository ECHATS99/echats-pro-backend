"""Génération asynchrone des certificats PDF (évite de bloquer la requête HTTP sur
le rendu PDF + upload Cloudinary, potentiellement lents)."""
import logging
import uuid

from sqlalchemy.orm import Session

logger = logging.getLogger("echats.workers.certificate")


def run_once(db: Session, user_id: uuid.UUID, track_id: uuid.UUID) -> dict | None:
    from app.modules.certificates.service import generate_certificate

    try:
        certificate = generate_certificate(db, user_id, track_id)
        return certificate.model_dump()
    except Exception:
        logger.exception("Échec de génération asynchrone du certificat pour user=%s track=%s", user_id, track_id)
        return None
