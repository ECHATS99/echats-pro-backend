"""Tests unitaires : signature HMAC des certificats (app/services/certificate_service.py)."""
import uuid

from app.services.certificate_service import sign_certificate, verify_signature


def test_signature_round_trip():
    user_id = uuid.uuid4()
    track_id = uuid.uuid4()
    code = "ABC123"
    signature = sign_certificate(code, user_id, track_id)
    assert verify_signature(code, user_id, track_id, signature) is True


def test_signature_invalid_for_tampered_code():
    user_id = uuid.uuid4()
    track_id = uuid.uuid4()
    signature = sign_certificate("ABC123", user_id, track_id)
    assert verify_signature("XYZ999", user_id, track_id, signature) is False


def test_signature_invalid_for_different_user():
    track_id = uuid.uuid4()
    signature = sign_certificate("ABC123", uuid.uuid4(), track_id)
    assert verify_signature("ABC123", uuid.uuid4(), track_id, signature) is False
