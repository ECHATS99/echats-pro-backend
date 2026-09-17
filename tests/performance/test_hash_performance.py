"""Test de performance léger (smoke test) : le hashing de flag doit rester rapide même en
rafale, car il est appelé à chaque soumission CTF (potentiellement des milliers en simultané
lors d'un évènement — Partie 7.17 du SRS : objectif <200ms par requête API hors opérations
lourdes). Ceci n'est PAS un test de charge complet (voir Partie 7.15 : à compléter avec un
outil dédié type Locust/k6 dans le pipeline CI)."""
import time

from app.security.hash import generate_salt, hash_flag, verify_flag

ITERATIONS = 1000
MAX_SECONDS_FOR_BATCH = 2.0  # SHA256 est volontairement rapide (contrairement à Argon2id
# utilisé pour les secrets internes) : ce budget est large pour absorber la variance CI.


def test_flag_hashing_stays_fast_under_load():
    salt = generate_salt()
    start = time.perf_counter()
    for i in range(ITERATIONS):
        digest = hash_flag(f"ECHATS{{flag_{i}}}", salt)
        verify_flag(f"ECHATS{{flag_{i}}}", salt, digest)
    elapsed = time.perf_counter() - start
    assert elapsed < MAX_SECONDS_FOR_BATCH, (
        f"{ITERATIONS} hash+verify de flags ont pris {elapsed:.2f}s, "
        f"budget maximum {MAX_SECONDS_FOR_BATCH}s."
    )
