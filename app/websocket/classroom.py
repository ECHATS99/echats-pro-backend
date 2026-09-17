"""Canal /ws/classroom : annonces instructeur en temps réel, par classroom."""
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.security.jwt import decode_access_token
from app.websocket.manager import connection_manager

router = APIRouter()


@router.websocket("/ws/classroom")
async def classroom_channel(websocket: WebSocket, token: str = Query(...), classroom_id: str = Query(...)):
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
    except Exception:
        await websocket.close(code=4401)
        return

    room = f"classroom:{classroom_id}"
    await connection_manager.connect(websocket, user_id, rooms=[room])
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, user_id, rooms=[room])
