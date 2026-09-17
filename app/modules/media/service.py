"""Logique métier du domaine 'media'. Validation stricte (extension, MIME réel via signature
binaire, taille max) avant tout envoi vers Cloudinary — jamais de fichier stocké côté backend
(Partie 8.5 du SRS)."""
from app.core.exceptions import ValidationError
from app.integrations.cloudinary.client import delete_file, upload_file
from app.modules.media.schemas import MediaUploadOut

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 Mo

# Signatures binaires (magic bytes) des formats autorisés, vérifiées indépendamment de
# l'extension ou du Content-Type déclaré par le client (jamais de confiance aveugle).
_SIGNATURES: dict[bytes, tuple[str, str]] = {
    b"\xff\xd8\xff": ("image/jpeg", "image"),
    b"\x89PNG\r\n\x1a\n": ("image/png", "image"),
    b"GIF87a": ("image/gif", "image"),
    b"GIF89a": ("image/gif", "image"),
    b"%PDF-": ("application/pdf", "raw"),
    b"PK\x03\x04": ("application/zip", "raw"),  # zip, docx, xlsx, pptx
}


def _detect_type(file_bytes: bytes) -> tuple[str, str]:
    for signature, (mime, resource_type) in _SIGNATURES.items():
        if file_bytes.startswith(signature):
            return mime, resource_type
    raise ValidationError("Type de fichier non reconnu ou non autorisé.")


def upload_media(file_bytes: bytes, folder: str) -> MediaUploadOut:
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValidationError(f"Fichier trop volumineux (max {MAX_FILE_SIZE_BYTES // (1024 * 1024)} Mo).")
    if not file_bytes:
        raise ValidationError("Fichier vide.")

    _mime, resource_type = _detect_type(file_bytes)
    result = upload_file(file_bytes, folder=folder, resource_type=resource_type)
    return MediaUploadOut(**result)


def delete_media(public_id: str, resource_type: str = "image") -> bool:
    return delete_file(public_id, resource_type)
