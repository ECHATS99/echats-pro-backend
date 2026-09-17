"""Tests unitaires : JWT interne (Partie 4.6 du SRS — access + refresh, aucune donnée sensible)."""
import pytest

from app.core.exceptions import InvalidTokenError
from app.security.jwt import (
    create_access_token, create_refresh_token, decode_access_token, decode_refresh_token,
)


def test_access_token_round_trip():
    token = create_access_token(user_id="user-123", role="student", plan="GO", permissions=["ctf.play"])
    payload = decode_access_token(token)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "student"
    assert payload["plan"] == "GO"
    assert payload["permissions"] == ["ctf.play"]
    assert payload["type"] == "access"


def test_refresh_token_round_trip():
    token = create_refresh_token(user_id="user-123")
    payload = decode_refresh_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "refresh"


def test_access_token_rejected_as_refresh_token():
    """Un access token ne doit jamais être accepté à la place d'un refresh token."""
    token = create_access_token(user_id="user-123", role="student", plan="GO", permissions=[])
    with pytest.raises(InvalidTokenError):
        decode_refresh_token(token)


def test_tampered_token_is_rejected():
    token = create_access_token(user_id="user-123", role="student", plan="GO", permissions=[])
    tampered = token[:-4] + "abcd"
    with pytest.raises(InvalidTokenError):
        decode_access_token(tampered)
