"""Client bas niveau pour cloudinary. Upload/suppression/transformation d'images et fichiers.
Clé secrète jamais exposée au frontend — ce module est le SEUL point de contact avec Cloudinary.
"""
from functools import lru_cache

import cloudinary
import cloudinary.uploader

from app.core.settings import settings
from app.integrations.cloudinary.exceptions import CloudinaryUploadError

ALLOWED_RESOURCE_TYPES = {"image", "video", "raw"}


@lru_cache
def _configure() -> None:
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


def upload_file(file_bytes: bytes, folder: str, resource_type: str = "image", public_id: str | None = None) -> dict:
    """Upload un fichier vers Cloudinary avec compression/optimisation automatique
    (quality:auto, format:auto — Partie 8.6 du SRS). Retourne {url, public_id, bytes, format}.
    """
    if resource_type not in ALLOWED_RESOURCE_TYPES:
        raise CloudinaryUploadError(f"Type de ressource non supporté : {resource_type}")

    _configure()
    try:
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=folder,
            resource_type=resource_type,
            public_id=public_id,
            quality="auto",
            fetch_format="auto",
            overwrite=True,
        )
    except Exception as exc:
        raise CloudinaryUploadError(f"Échec de l'upload Cloudinary : {exc}") from exc

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
        "bytes": result.get("bytes"),
        "format": result.get("format"),
    }


def delete_file(public_id: str, resource_type: str = "image") -> bool:
    _configure()
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return result.get("result") == "ok"
    except Exception as exc:
        raise CloudinaryUploadError(f"Échec de la suppression Cloudinary : {exc}") from exc
