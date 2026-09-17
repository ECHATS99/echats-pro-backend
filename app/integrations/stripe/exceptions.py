"""Exceptions spécifiques au fournisseur stripe."""


class StripeError(Exception):
    """Levée en cas d'échec Stripe (création de paiement, vérification de webhook)."""
