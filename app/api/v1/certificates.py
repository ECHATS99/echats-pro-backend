"""Routes HTTP /api/v1/certificates."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.modules.certificates import service as certificates_service
from app.modules.certificates.schemas import CertificateOut, CertificateVerifyOut

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("", response_model=list[CertificateOut])
def list_my_certificates(current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return certificates_service.list_my_certificates(db, current.id)


@router.post("/generate", response_model=CertificateOut, status_code=201)
def generate(track_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return certificates_service.generate_certificate(db, current.id, track_id)


@router.get("/verify/{code}", response_model=CertificateVerifyOut)
def verify(code: str, db: Session = Depends(get_db)):
    """Vérification publique d'un certificat (aucune authentification requise)."""
    return certificates_service.verify_certificate(db, code)
