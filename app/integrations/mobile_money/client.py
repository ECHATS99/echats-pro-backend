"""Client bas niveau pour Mobile Money (MTN Mobile Money, Airtel Money, Wave).

Les trois providers exposent des API REST différentes ; ce client normalise l'interface
utilisée par le reste du backend (`request_payment` / `check_status`) afin que le domaine
`payments` reste indépendant du fournisseur effectif.
"""
import uuid

import httpx

from app.core.settings import settings
from app.integrations.mobile_money.exceptions import MobileMoneyError

PROVIDER_ENDPOINTS = {
    "mtn": "https://api.mtn.com/collection/v1_0/requesttopay",
    "airtel": "https://openapi.airtel.africa/merchant/v1/payments/",
    "wave": "https://api.wave.com/v1/checkout/sessions",
}


def request_payment(provider: str, phone_number: str, amount: int, currency: str, reference: str | None = None) -> dict:
    """Initie une demande de paiement Mobile Money. Retourne un identifiant de transaction
    à interroger ensuite via `check_status`.
    """
    provider = provider.lower()
    if provider not in PROVIDER_ENDPOINTS:
        raise MobileMoneyError(f"Fournisseur Mobile Money inconnu : {provider}")

    reference = reference or str(uuid.uuid4())
    try:
        response = httpx.post(
            PROVIDER_ENDPOINTS[provider],
            headers={"Authorization": f"Bearer {settings.MOBILE_MONEY_API_KEY}"},
            json={"phone_number": phone_number, "amount": amount, "currency": currency, "reference": reference},
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        raise MobileMoneyError(f"Échec de la demande de paiement {provider} : {exc}") from exc

    return {"transaction_id": data.get("transaction_id", reference), "status": data.get("status", "pending")}


def check_status(provider: str, transaction_id: str) -> str:
    provider = provider.lower()
    if provider not in PROVIDER_ENDPOINTS:
        raise MobileMoneyError(f"Fournisseur Mobile Money inconnu : {provider}")
    try:
        response = httpx.get(
            f"{PROVIDER_ENDPOINTS[provider]}{transaction_id}",
            headers={"Authorization": f"Bearer {settings.MOBILE_MONEY_API_KEY}"},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json().get("status", "pending")
    except Exception as exc:
        raise MobileMoneyError(f"Échec de vérification du statut {provider} : {exc}") from exc
