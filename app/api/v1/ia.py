"""Routes HTTP /api/v1/ia (proxy sécurisé vers api.echats.ai)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.dependencies.permissions import require_permission
from app.modules.ia import service as ia_service
from app.modules.ia.schemas import ChatRequest, ChatResponse, IAPromptUpdate

router = APIRouter(prefix="/ia", tags=["ia"])


@router.post("/cyber", response_model=ChatResponse)
def cyber(payload: ChatRequest, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Assistant cybersécurité, enrichi par RAG (contexte de la leçon/exercice en cours)."""
    return ia_service.chat(db, "cyber", payload, current.id)


@router.post("/go", response_model=ChatResponse)
def go(payload: ChatRequest, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Assistant de navigation général."""
    return ia_service.chat(db, "go", payload, current.id)


@router.post("/nexo", response_model=ChatResponse)
def nexo(payload: ChatRequest, current: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Assistant commercial Nexoshop."""
    return ia_service.chat(db, "nexo", payload, current.id)


@router.put("/prompts/{context}")
def update_prompt(
    context: str, payload: IAPromptUpdate,
    current: CurrentUser = Depends(require_permission("ia.manage")),
    db: Session = Depends(get_db),
):
    """Modifie le prompt système d'un contexte (cyber/go/nexo) sans redéploiement (Partie 5 du SRS)."""
    return ia_service.update_prompt(db, context, payload, current.id)
