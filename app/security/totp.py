"""Génération et validation TOTP, avec anti-réutilisation côté serveur."""
import secrets
import time

import pyotp

from app.core.settings import settings


def generate_totp_secret() -> str:
    """Génère un nouveau secret TOTP pour un utilisateur (à stocker chiffré en base)."""
    return pyotp.random_base32()


def get_provisioning_uri(secret: str, account_email: str) -> str:
    """URI otpauth:// à encoder en QR code pour une app Authenticator."""
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=account_email, issuer_name=settings.TOTP_ISSUER_NAME
    )


def verify_totp_code(secret: str, code: str) -> bool:
    """Vérifie un code TOTP à 6 chiffres avec une tolérance d'une période."""
    return bool(code and code.isdigit() and len(code) == 6 and pyotp.totp.TOTP(secret).verify(code, valid_window=1))


def verify_totp_code_once(secret: str, code: str, redis_client, subject: str) -> bool:
    """Vérifie un code et interdit sa réutilisation pendant sa période de validité.

    Le compteur TOTP correspondant est marqué en Redis avec SET NX. Cela conserve la
    tolérance de dérive d'horloge d'une période, mais un code accepté une fois ne peut
    plus être rejoué pour le même utilisateur.
    """
    if not code or not code.isdigit() or len(code) != 6:
        return False

    totp = pyotp.TOTP(secret)
    current_counter = int(time.time() // totp.interval)
    matched_counter = None
    for offset in (-1, 0, 1):
        counter = current_counter + offset
        expected = totp.at(counter * totp.interval)
        if secrets.compare_digest(expected, code):
            matched_counter = counter
            break

    if matched_counter is None:
        return False

    key = f"totp:used:{subject}:{matched_counter}"
    return bool(redis_client.set(key, "1", nx=True, ex=settings.TOTP_USED_TTL_SECONDS))
