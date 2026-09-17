"""Fonctions utilitaires liées aux images (au-delà de Cloudinary, pour la validation locale
avant envoi)."""

MAX_AVATAR_DIMENSION_PX = 2048


def build_cloudinary_variant_url(base_url: str, width: int, height: int | None = None) -> str:
    """Insère une transformation Cloudinary (redimensionnement) dans une URL déjà générée,
    sans nouvel appel réseau — utile pour servir des vignettes depuis une URL existante."""
    transform = f"w_{width}"
    if height:
        transform += f",h_{height},c_fill"
    return base_url.replace("/upload/", f"/upload/{transform}/")
