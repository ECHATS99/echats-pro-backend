"""Vérification du token Firebase via Firebase Admin SDK, extraction de l'uid.
Ne décide jamais du rôle (ça vient de PostgreSQL). Délègue au client dédié dans
app/integrations/firebase/ (seul point de contact réel avec le SDK Firebase).
"""
from app.integrations.firebase.client import FirebaseIdentity, verify_firebase_token
from app.integrations.firebase.exceptions import FirebaseTokenError

__all__ = ["FirebaseIdentity", "verify_firebase_token", "FirebaseTokenError"]
