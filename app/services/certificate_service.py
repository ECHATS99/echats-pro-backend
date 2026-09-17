"""Génération de certificats PDF signés + vérification publique par code.

Le PDF est généré avec reportlab (aucune donnée binaire volumineuse conservée en base :
seule l'URL Cloudinary du PDF final est stockée, conformément à la Partie 8.5 du SRS).
"""
import hashlib
import hmac
import io
import uuid

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

from app.core.settings import settings
from app.integrations.cloudinary.client import upload_file


def generate_verification_code() -> str:
    return uuid.uuid4().hex[:16].upper()


def sign_certificate(verification_code: str, user_id: uuid.UUID, track_id: uuid.UUID) -> str:
    """Signature HMAC-SHA256 permettant de vérifier l'authenticité d'un certificat sans
    dépendre uniquement de sa présence en base (défense en profondeur)."""
    message = f"{verification_code}:{user_id}:{track_id}".encode()
    return hmac.new(settings.CERTIFICATE_SIGNING_SECRET.encode() or b"insecure-dev-key", message, hashlib.sha256).hexdigest()


def _render_pdf(username: str, track_title: str, verification_code: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    c.setFillColorRGB(0.05, 0.04, 0.12)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColorRGB(0.49, 0.23, 0.93)  # accent violet #7C3AED
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 100, "ECHATS PRO")

    c.setFillColorRGB(0.95, 0.96, 0.98)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 160, "Certificat de complétion")

    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 220, f"Décerné à {username}")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 260, track_title)

    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.58, 0.64, 0.72)
    c.drawCentredString(width / 2, 60, f"Code de vérification : {verification_code}")
    c.drawCentredString(width / 2, 45, "BLACKHAWK LAB — Formés en Afrique, opérationnels partout.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()


def generate_certificate_pdf(user_id: uuid.UUID, username: str, track_id: uuid.UUID, track_title: str) -> dict:
    """Génère le PDF, le signe, l'upload sur Cloudinary. Retourne les champs à persister."""
    verification_code = generate_verification_code()
    signature = sign_certificate(verification_code, user_id, track_id)

    pdf_bytes = _render_pdf(username, track_title, verification_code)
    upload_result = upload_file(pdf_bytes, folder="certificates", resource_type="raw", public_id=verification_code)

    return {
        "verification_code": verification_code,
        "signature": signature,
        "cloudinary_url": upload_result["url"],
    }


def verify_signature(verification_code: str, user_id: uuid.UUID, track_id: uuid.UUID, signature: str) -> bool:
    expected = sign_certificate(verification_code, user_id, track_id)
    return hmac.compare_digest(expected, signature)
