"""Génération de slugs uniques (tracks, produits...)."""
import re
import unicodedata


def slugify(text: str) -> str:
    """Convertit un texte en slug URL-safe (minuscule, tirets, sans accents)."""
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def make_unique_slug(base: str, exists_fn) -> str:
    """Génère un slug unique en ajoutant un suffixe numérique si nécessaire.
    `exists_fn(slug) -> bool` doit vérifier l'existence en base.
    """
    slug = slugify(base)
    candidate = slug
    counter = 2
    while exists_fn(candidate):
        candidate = f"{slug}-{counter}"
        counter += 1
    return candidate
