"""Client Firebase Admin SDK. SEUL point de contact avec Firebase Authentication.
Vérifie uniquement l'identité (uid/email) — ne décide jamais du rôle ou du plan,
qui viennent exclusivement de PostgreSQL (Partie 3 et 4.2 du SRS).
"""
from dataclasses import dataclass
from functools import lru_cache
import json

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from app.core.settings import settings
from app.integrations.firebase.exceptions import FirebaseTokenError


@dataclass
class FirebaseIdentity:
    """Identité minimale extraite du token Firebase — rien de plus n'est utilisé côté backend."""
    uid: str
    email: str | None
    email_verified: bool


@lru_cache
def _get_app() -> firebase_admin.App:
    if firebase_admin._apps:
        return firebase_admin.get_app()
    if not settings.FIREBASE_CREDENTIALS_JSON:
        raise FirebaseTokenError("FIREBASE_CREDENTIALS_JSON n'est pas configuré.")
    cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
    cred = credentials.Certificate(cred_dict)
    return firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token: str) -> FirebaseIdentity:
    """Vérifie un ID token Firebase envoyé par le frontend et retourne l'identité minimale.

    Lève FirebaseTokenError si le token est invalide, expiré ou révoqué.
    """
    _get_app()
    try:
        decoded = firebase_auth.verify_id_token(id_token, check_revoked=True)
    except Exception as exc:  # firebase_admin lève plusieurs types d'exceptions selon le cas
        raise FirebaseTokenError(f"Token Firebase invalide : {exc}") from exc

    return FirebaseIdentity(
        uid=decoded["uid"],
        email=decoded.get("email"),
        email_verified=decoded.get("email_verified", False),
    )
