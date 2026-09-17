"""Tests de sécurité : validation des entrées (Partie 8.4 du SRS — protection XSS basique
en complément de Pydantic)."""
from app.utils.validators import contains_dangerous_html, is_safe_text, is_valid_slug


def test_detects_script_tag():
    assert contains_dangerous_html("<script>alert(1)</script>") is True


def test_detects_iframe_tag():
    assert contains_dangerous_html("<iframe src='evil.com'></iframe>") is True


def test_allows_normal_text():
    assert contains_dangerous_html("Ceci est un writeup normal avec du <b>gras</b>.") is False


def test_is_safe_text_rejects_oversized_input():
    assert is_safe_text("a" * 20000, max_length=10000) is False


def test_is_valid_slug_accepts_correct_format():
    assert is_valid_slug("pentest-web-owasp") is True


def test_is_valid_slug_rejects_uppercase_or_spaces():
    assert is_valid_slug("Pentest Web") is False
    assert is_valid_slug("PENTEST-WEB") is False
