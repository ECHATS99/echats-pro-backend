"""Régressions de sécurité pour TOTP et refresh sessions."""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import uuid

import pytest
import pyotp

from app.core.exceptions import UnauthorizedError
from app.modules.auth import service as auth_service
from app.security.jwt import create_refresh_token, decode_refresh_token, hash_refresh_token
from app.security.totp import verify_totp_code_once


def test_totp_code_is_single_use(fake_redis):
    secret = pyotp.random_base32()
    code = pyotp.TOTP(secret).now()
    assert verify_totp_code_once(secret, code, fake_redis, "user-a") is True
    assert verify_totp_code_once(secret, code, fake_redis, "user-a") is False


def test_totp_code_can_be_used_by_another_user_subject(fake_redis):
    secret = pyotp.random_base32()
    code = pyotp.TOTP(secret).now()
    assert verify_totp_code_once(secret, code, fake_redis, "user-a") is True
    assert verify_totp_code_once(secret, code, fake_redis, "user-b") is True


class FakeSessionDB:
    def __init__(self, user):
        self.user = user
        self.added = []
        self.commits = 0

    def get(self, model, user_id):
        return self.user if user_id == self.user.id else None

    def add(self, value):
        self.added.append(value)

    def commit(self):
        self.commits += 1


def _refresh_fixture():
    user_id = uuid.uuid4()
    session_id = uuid.uuid4()
    old_token = create_refresh_token(str(user_id), str(session_id))
    session = SimpleNamespace(
        user_id=user_id,
        session_id=session_id,
        token_hash=hash_refresh_token(old_token),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        revoked_at=None,
        replaced_by_session_id=None,
        last_used_at=None,
    )
    user = SimpleNamespace(
        id=user_id,
        is_active=True,
        primary_role_name="student",
        subscriptions=[],
        roles=[],
    )
    return old_token, session, user


def test_refresh_rotates_and_revokes_old_token(monkeypatch):
    old_token, session, user = _refresh_fixture()
    db = FakeSessionDB(user)
    monkeypatch.setattr(auth_service.sessions_repo, "get_by_session_id_for_update", lambda db, sid: session)

    access_token, new_refresh_token = auth_service.refresh_access_token(db, old_token)
    assert access_token
    assert new_refresh_token != old_token
    assert session.revoked_at is not None
    assert session.replaced_by_session_id is not None
    assert db.commits == 1
    assert decode_refresh_token(new_refresh_token)["sid"] == str(session.replaced_by_session_id)


def test_reused_refresh_token_is_denied_and_sessions_are_revoked(monkeypatch):
    old_token, session, user = _refresh_fixture()
    session.revoked_at = datetime.now(timezone.utc)
    db = FakeSessionDB(user)
    revoked_all = []
    monkeypatch.setattr(auth_service.sessions_repo, "get_by_session_id_for_update", lambda db, sid: session)
    monkeypatch.setattr(auth_service.sessions_repo, "revoke_all", lambda db, user_id: revoked_all.append(user_id))

    with pytest.raises(UnauthorizedError):
        auth_service.refresh_access_token(db, old_token)
    assert revoked_all == [user.id]


def test_expired_refresh_token_is_denied(monkeypatch):
    old_token, session, user = _refresh_fixture()
    session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    db = FakeSessionDB(user)
    monkeypatch.setattr(auth_service.sessions_repo, "get_by_session_id_for_update", lambda db, sid: session)

    with pytest.raises(UnauthorizedError):
        auth_service.refresh_access_token(db, old_token)
