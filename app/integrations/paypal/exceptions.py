"""Exceptions spécifiques au fournisseur paypal."""


class PayPalError(Exception):
    """Levée en cas d'échec PayPal (création de commande, capture, remboursement)."""
