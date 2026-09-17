"""Exceptions spécifiques au fournisseur cloudinary."""


class CloudinaryUploadError(Exception):
    """Levée quand l'upload, la suppression ou la transformation échoue."""
