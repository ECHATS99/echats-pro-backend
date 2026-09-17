"""Exceptions spécifiques à l'intégration Firebase Admin SDK."""


class FirebaseTokenError(Exception):
    """Levée quand le token Firebase est absent, malformé, expiré ou révoqué."""
