"""Gestionnaire central des connexions WebSocket (rooms, broadcast).

Implémentation in-process : suffisante pour un seul worker. En cas de scale horizontal
(plusieurs workers Render), remplacer le transport interne par un pub/sub Redis
(REDIS as message bus) sans changer l'API publique de ce module (send_to_user /
broadcast_channel / broadcast_room), ce qui est l'objectif d'isolation recherché.
"""
from __future__ import annotations

import asyncio
import json
import uuid
from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        # user_id -> set de connexions actives (un utilisateur peut avoir plusieurs onglets)
        self._user_connections: dict[str, set[WebSocket]] = defaultdict(set)
        # room (ex: "classroom:<id>", "leaderboard", "activity") -> set de connexions
        self._rooms: dict[str, set[WebSocket]] = defaultdict(set)
        self._loop: asyncio.AbstractEventLoop | None = None

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def connect(self, websocket: WebSocket, user_id: uuid.UUID, rooms: list[str] | None = None) -> None:
        await websocket.accept()
        self._user_connections[str(user_id)].add(websocket)
        for room in rooms or []:
            self._rooms[room].add(websocket)
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

    def disconnect(self, websocket: WebSocket, user_id: uuid.UUID, rooms: list[str] | None = None) -> None:
        self._user_connections[str(user_id)].discard(websocket)
        for room in rooms or []:
            self._rooms[room].discard(websocket)

    async def _send(self, websocket: WebSocket, payload: dict) -> None:
        try:
            await websocket.send_text(json.dumps(payload, default=str))
        except Exception:
            pass

    def _schedule(self, coro) -> None:
        """Planifie une coroutine d'envoi depuis un contexte potentiellement synchrone
        (les services métier appellent ces méthodes sans être eux-mêmes async).
        """
        if self._loop is None or self._loop.is_closed():
            return
        try:
            asyncio.run_coroutine_threadsafe(coro, self._loop)
        except RuntimeError:
            pass

    def send_to_user(self, user_id: uuid.UUID, payload: dict) -> None:
        for ws in list(self._user_connections.get(str(user_id), set())):
            self._schedule(self._send(ws, payload))

    def broadcast_channel(self, channel: str, payload: dict) -> None:
        self.broadcast_room(channel, payload)

    def broadcast_room(self, room: str, payload: dict) -> None:
        for ws in list(self._rooms.get(room, set())):
            self._schedule(self._send(ws, payload))


connection_manager = ConnectionManager()
