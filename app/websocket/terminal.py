"""Canal WebSocket terminal pour les labs.

Le navigateur obtient d'abord un ticket court et à usage unique via
POST /api/v1/labs/{lab_id}/ws-ticket. Aucun JWT n'est accepté dans l'URL.
"""
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.core.exceptions import AppError
from app.modules.labs.service import consume_ws_ticket
from app.websocket.manager import connection_manager

router = APIRouter()


@router.websocket("/ws/labs")
async def terminal_channel(websocket: WebSocket, ticket: str = Query(...)):
    try:
        lab_id, user_id = consume_ws_ticket(ticket)
    except AppError as exc:
        # Ne pas révéler si le ticket, l'utilisateur ou le lab est la cause précise.
        await websocket.close(code=4401 if exc.status_code == 401 else 4403)
        return
    except Exception:
        await websocket.close(code=4401)
        return

    room = f"lab:{lab_id}"
    await connection_manager.connect(websocket, user_id, rooms=[room])
    try:
        while True:
            data = await websocket.receive_text()
            # Le lab_id provient du ticket consommé, jamais du client.
            connection_manager.broadcast_room(room, {"channel": "labs", "from": str(user_id), "data": data})
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, user_id, rooms=[room])
