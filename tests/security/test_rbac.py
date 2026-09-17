"""Tests de sécurité : moteur RBAC (Zero Trust — Partie 4.13 du SRS, ne jamais faire
confiance au frontend, tout est revérifié côté backend)."""
import pytest

from app.core.exceptions import ForbiddenError
from app.security.rbac import assert_permission, assert_role, assert_same_institution, has_permission, has_role


def test_has_permission_true_when_present():
    assert has_permission(["ctf.create", "admin.access"], "ctf.create") is True


def test_has_permission_false_when_absent():
    assert has_permission(["ctf.play"], "ctf.create") is False


def test_assert_permission_raises_forbidden_when_missing():
    with pytest.raises(ForbiddenError):
        assert_permission(["ctf.play"], "admin.access")


def test_assert_role_raises_forbidden_for_unauthorized_role():
    with pytest.raises(ForbiddenError):
        assert_role("student", ["admin", "super_admin"])


def test_assert_role_passes_for_authorized_role():
    assert_role("admin", ["admin", "super_admin"])  # ne doit lever aucune exception


def test_assert_same_institution_blocks_cross_tenant_access():
    """Isolation multi-tenant stricte (Partie 4.11 du SRS) : une institution ne doit jamais
    accéder aux ressources d'une autre."""
    import uuid
    institution_a = uuid.uuid4()
    institution_b = uuid.uuid4()
    with pytest.raises(ForbiddenError):
        assert_same_institution(institution_a, institution_b)


def test_assert_same_institution_allows_same_tenant():
    import uuid
    institution_a = uuid.uuid4()
    assert_same_institution(institution_a, institution_a)  # ne doit lever aucune exception
