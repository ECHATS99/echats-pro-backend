"""Régressions de sécurité Labs : ownership REST et tickets WebSocket."""
import json
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.modules.labs import repository as labs_repo
from app.modules.labs import service as labs_service


@pytest.mark.parametrize("method,path", [
    ("post", "/api/v1/labs/start?lab_id=lab-a"),
    ("post", "/api/v1/labs/stop?lab_id=lab-a"),
    ("post", "/api/v1/labs/reset?lab_id=lab-a"),
    ("get", "/api/v1/labs/status?lab_id=lab-a"),
])
def test_sensitive_lab_routes_require_authentication(method, path):
    from app.main import app
    response = getattr(TestClient(app), method)(path)
    assert response.status_code == 401


class TicketRedis:
    def __init__(self):
        self.store = {}
        self.ttl = {}

    def set(self, key, value, ex=None, nx=False):
        if nx and key in self.store:
            return False
        self.store[key] = value
        self.ttl[key] = ex
        return True

    def get(self, key):
        return self.store.get(key)

    def getdel(self, key):
        return self.store.pop(key, None)

    def delete(self, *keys):
        for key in keys:
            self.store.pop(key, None)
            self.ttl.pop(key, None)


def _lab_store(monkeypatch):
    owner_a = uuid.uuid4()
    owner_b = uuid.uuid4()
    sessions = {
        "lab-a": {"user_id": str(owner_a), "kind": "judge0", "status": "ready"},
    }

    monkeypatch.setattr(labs_repo, "get_session", lambda lab_id: sessions.get(lab_id))
    monkeypatch.setattr(labs_repo, "save_session", lambda lab_id, data: sessions.__setitem__(lab_id, dict(data)))
    monkeypatch.setattr(labs_repo, "touch_session", lambda lab_id: None)
    monkeypatch.setattr(labs_repo, "delete_session", lambda lab_id: sessions.pop(lab_id, None))
    return owner_a, owner_b, sessions


def test_user_a_can_start_own_lab_but_user_b_is_denied(monkeypatch):
    owner_a, owner_b, _ = _lab_store(monkeypatch)

    result = labs_service.start_lab("lab-a", owner_a)
    assert result.status == "active"

    with pytest.raises(ForbiddenError):
        labs_service.start_lab("lab-a", owner_b)


def test_cross_owner_stop_reset_and_status_are_denied(monkeypatch):
    owner_a, owner_b, _ = _lab_store(monkeypatch)

    with pytest.raises(ForbiddenError):
        labs_service.stop_lab("lab-a", owner_b)
    with pytest.raises(ForbiddenError):
        labs_service.reset_lab("lab-a", owner_b)
    with pytest.raises(ForbiddenError):
        labs_service.get_status("lab-a", owner_b)

    labs_service.stop_lab("lab-a", owner_a)
    assert labs_service.get_status("lab-a", owner_a).status == "stopped"


def test_unknown_lab_is_not_treated_as_public():
    with pytest.raises(Exception):
        labs_service.get_owned_lab("unknown", uuid.uuid4())


def test_ws_ticket_is_bound_to_owner_and_single_use(monkeypatch):
    owner_a, owner_b, _ = _lab_store(monkeypatch)
    fake_redis = TicketRedis()
    monkeypatch.setattr(labs_service, "get_redis_client", lambda: fake_redis)

    ticket_out = labs_service.create_ws_ticket("lab-a", owner_a)
    assert ticket_out.expires_in_seconds == 60
    lab_id, user_id = labs_service.consume_ws_ticket(ticket_out.ticket)
    assert lab_id == "lab-a"
    assert user_id == owner_a

    with pytest.raises(UnauthorizedError):
        labs_service.consume_ws_ticket(ticket_out.ticket)

    with pytest.raises(ForbiddenError):
        labs_service.create_ws_ticket("lab-a", owner_b)


def test_ws_ticket_cannot_be_rebound_to_another_lab(monkeypatch):
    owner_a, _, sessions = _lab_store(monkeypatch)
    sessions["lab-b"] = {"user_id": str(uuid.uuid4()), "kind": "judge0", "status": "ready"}
    fake_redis = TicketRedis()
    monkeypatch.setattr(labs_service, "get_redis_client", lambda: fake_redis)

    ticket_out = labs_service.create_ws_ticket("lab-a", owner_a)
    key = next(iter(fake_redis.store))
    fake_redis.store[key] = json.dumps({"lab_id": "lab-b", "user_id": str(owner_a)})

    with pytest.raises(ForbiddenError):
        labs_service.consume_ws_ticket(ticket_out.ticket)
