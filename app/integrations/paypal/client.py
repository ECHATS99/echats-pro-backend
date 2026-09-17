"""Client bas niveau pour paypal (REST API v2, orders + captures)."""
import httpx

from app.core.settings import settings
from app.integrations.paypal.exceptions import PayPalError

PAYPAL_BASE_URL = "https://api-m.paypal.com"


def _get_access_token() -> str:
    try:
        response = httpx.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as exc:
        raise PayPalError(f"Échec d'authentification PayPal : {exc}") from exc


def create_order(amount: str, currency: str, reference_id: str) -> dict:
    token = _get_access_token()
    try:
        response = httpx.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "intent": "CAPTURE",
                "purchase_units": [{
                    "reference_id": reference_id,
                    "amount": {"currency_code": currency.upper(), "value": amount},
                }],
            },
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        raise PayPalError(f"Échec de création de commande PayPal : {exc}") from exc


def capture_order(order_id: str) -> dict:
    token = _get_access_token()
    try:
        response = httpx.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        raise PayPalError(f"Échec de capture PayPal : {exc}") from exc
