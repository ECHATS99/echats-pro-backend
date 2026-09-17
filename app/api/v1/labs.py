"""Routes HTTP des labs éphémères."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import CurrentUser, get_current_user
from app.dependencies.database import get_db
from app.modules.labs import service as labs_service
from app.modules.labs.schemas import LabCreateRequest, LabSessionOut, LabWebSocketTicketOut

router = APIRouter(prefix="/labs", tags=["labs"])


@router.post("/create", response_model=LabSessionOut, status_code=201)
def create_lab(
    payload: LabCreateRequest,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return labs_service.create_lab(db, payload, current.id)


@router.post("/{lab_id}/ws-ticket", response_model=LabWebSocketTicketOut)
def create_ws_ticket(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
):
    return labs_service.create_ws_ticket(lab_id, current.id)


@router.post("/start", response_model=LabSessionOut)
def start_lab(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
):
    return labs_service.start_lab(lab_id, current.id)


@router.post("/stop")
def stop_lab(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
):
    labs_service.stop_lab(lab_id, current.id)
    return {"stopped": True}


@router.post("/reset", response_model=LabSessionOut)
def reset_lab(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
):
    return labs_service.reset_lab(lab_id, current.id)


@router.get("/status", response_model=LabSessionOut)
def get_status(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
):
    return labs_service.get_status(lab_id, current.id)


@router.delete("/destroy")
def destroy_lab(
    lab_id: str,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    labs_service.destroy_lab(db, lab_id, current.id)
    return {"destroyed": True}
