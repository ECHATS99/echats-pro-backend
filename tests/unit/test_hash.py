"""Tests unitaires : hashing des flags CTF (Partie 7 du SRS — jamais en clair, temps constant)."""
from app.security.hash import generate_salt, hash_flag, verify_flag


def test_hash_flag_is_deterministic_for_same_salt():
    salt = "fixed-salt"
    assert hash_flag("ECHATS{test_flag}", salt) == hash_flag("ECHATS{test_flag}", salt)


def test_hash_flag_differs_across_salts():
    flag = "ECHATS{test_flag}"
    assert hash_flag(flag, "salt-a") != hash_flag(flag, "salt-b")


def test_verify_flag_accepts_correct_flag():
    salt = generate_salt()
    stored_hash = hash_flag("ECHATS{correct}", salt)
    assert verify_flag("ECHATS{correct}", salt, stored_hash) is True


def test_verify_flag_rejects_incorrect_flag():
    salt = generate_salt()
    stored_hash = hash_flag("ECHATS{correct}", salt)
    assert verify_flag("ECHATS{wrong}", salt, stored_hash) is False


def test_generate_salt_is_unique():
    salts = {generate_salt() for _ in range(100)}
    assert len(salts) == 100
