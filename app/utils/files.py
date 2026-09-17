"""Fonctions utilitaires liées aux fichiers (extensions, tailles lisibles)."""

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "docx", "xlsx", "pptx"}


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_allowed_image(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_IMAGE_EXTENSIONS


def is_allowed_document(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_DOCUMENT_EXTENSIONS


def human_readable_size(size_bytes: int) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} To"
