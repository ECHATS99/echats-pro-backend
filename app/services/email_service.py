"""Envoi d'emails transactionnels (SendGrid ou Resend)."""
import logging

import httpx

from app.core.settings import settings

logger = logging.getLogger("echats.email")


def _send_via_sendgrid(to: str, subject: str, html: str) -> bool:
    response = httpx.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"},
        json={
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": settings.EMAIL_FROM},
            "subject": subject,
            "content": [{"type": "text/html", "value": html}],
        },
        timeout=10.0,
    )
    return response.status_code in (200, 202)


def _send_via_resend(to: str, subject: str, html: str) -> bool:
    response = httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
        json={"from": settings.EMAIL_FROM, "to": [to], "subject": subject, "html": html},
        timeout=10.0,
    )
    return response.status_code in (200, 201)


def send_email(to: str, subject: str, html: str) -> bool:
    """Envoie un email transactionnel. Best effort : ne lève jamais d'exception bloquante
    pour ne pas casser le flux métier principal (ex: inscription réussie même si l'email échoue).
    """
    try:
        if settings.SENDGRID_API_KEY:
            return _send_via_sendgrid(to, subject, html)
        if settings.RESEND_API_KEY:
            return _send_via_resend(to, subject, html)
        logger.warning("Aucun provider email configuré, envoi ignoré (to=%s, subject=%s).", to, subject)
        return False
    except Exception:
        logger.exception("Échec de l'envoi d'email à %s.", to)
        return False


def send_welcome_email(to: str, username: str) -> None:
    send_email(to, "Bienvenue sur ECHATS PRO", f"<p>Bonjour {username},</p><p>Bienvenue sur ECHATS PRO, la plateforme de cybersécurité francophone de BLACKHAWK LAB.</p>")


def send_certificate_email(to: str, username: str, track_title: str, verify_url: str) -> None:
    send_email(
        to, f"Votre certificat « {track_title} »",
        f"<p>Félicitations {username},</p><p>Votre certificat pour « {track_title} » est prêt. "
        f"Vérifiez-le ici : <a href='{verify_url}'>{verify_url}</a></p>",
    )
