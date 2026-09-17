"""Tests unitaires : génération de slugs uniques (app/utils/slug.py)."""
from app.utils.slug import make_unique_slug, slugify


def test_slugify_removes_accents_and_lowercases():
    assert slugify("Sécurité Réseau & Systèmes") == "securite-reseau-systemes"


def test_slugify_strips_leading_trailing_dashes():
    assert slugify("  Hello World!!  ") == "hello-world"


def test_make_unique_slug_appends_suffix_on_conflict():
    taken = {"pentest-web"}
    result = make_unique_slug("Pentest Web", lambda s: s in taken)
    assert result == "pentest-web-2"


def test_make_unique_slug_returns_base_when_free():
    result = make_unique_slug("OSINT Fondamentaux", lambda s: False)
    assert result == "osint-fondamentaux"
