"""Canal /ws/leaderboard : classement live, mis à jour à chaque soumission."""
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.security.jwt import decode_access_token
from app.websocket.manager import connection_manager

router = APIRouter()


@router.websocket("/ws/leaderboard")
async def leaderboard_channel(websocket: WebSocket, token: str = Query(...)):
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
    except Exception:
        await websocket.close(code=4401)
        return

    await connection_manager.connect(websocket, user_id, rooms=["leaderboard"])
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, user_id, rooms=["leaderboard"])
