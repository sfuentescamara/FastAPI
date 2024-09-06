from fastapi import WebSocket, WebSocketDisconnect

from app.core.dependencies import *
from app.model.base import RoomManager

router = APIRouter()

class ConnectionManager:
    active_connections: List[WebSocket] = []

    @classmethod
    async def connect(cls, websocket: WebSocket):
        await websocket.accept()
        cls.active_connections.append(websocket)

    @classmethod
    def disconnect(cls, websocket: WebSocket):
        cls.active_connections.remove(websocket)
        if RoomManager.closeRoom(websocket.path_params['client_id']):
            # print("engine check ")
            pass


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ConnectionManager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # Procesar datos
            # call to engine and precces data
            
    except WebSocketDisconnect:
        ConnectionManager.disconnect(websocket)