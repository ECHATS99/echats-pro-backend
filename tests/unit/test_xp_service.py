"""Tests unitaires : calcul de la courbe de progression XP -> niveau (app/services/xp_service.py)."""
from app.services.xp_service import LEVEL_XP_STEP, level_for_xp


def test_level_1_at_zero_xp():
    assert level_for_xp(0) == 1


def test_level_increases_with_xp():
    assert level_for_xp(0) < level_for_xp(LEVEL_XP_STEP) < level_for_xp(LEVEL_XP_STEP * 5)


def test_level_never_decreases_for_higher_xp():
    """Propriété de monotonie : plus d'XP ne doit jamais donner un niveau inférieur."""
    previous_level = 1
    for xp in range(0, 20000, 250):
        level = level_for_xp(xp)
        assert level >= previous_level
        previous_level = level


def test_level_for_negative_xp_defaults_to_one():
    assert level_for_xp(-100) == 1
