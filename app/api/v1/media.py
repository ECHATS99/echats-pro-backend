"""Routes HTTP /api/v1/media."""
from fastapi import APIRouter, Depends, UploadFile

from app.dependencies.auth import CurrentUser, get_current_user
from app.modules.media import service as media_service
from app.modules.media.schemas import MediaUploadOut

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload", response_model=MediaUploadOut, status_code=201)
async def upload(file: UploadFile, folder: str = "misc", current: CurrentUser = Depends(get_current_user)):
    """Point d'entrée unique pour tout upload (avatars, images de cours, produits, etc.).
    Le frontend ne connaît jamais les clés Cloudinary."""
    file_bytes = await file.read()
    return media_service.upload_media(file_bytes, folder)


@router.delete("/delete")
def delete(public_id: str, resource_type: str = "image", current: CurrentUser = Depends(get_current_user)):
    deleted = media_service.delete_media(public_id, resource_type)
    return {"deleted": deleted}
