from fastapi import WebSocket, WebSocketDisconnect

from app.core.dependencies import *
from app.core.engine import Engine
from app.model.base import Client, ClientManager, RoomManager

router = APIRouter()

class ConnectionManager:
    active_connections: List[WebSocket] = []

    @classmethod
    async def connect(cls, websocket: WebSocket):
        await websocket.accept()
        cls.active_connections.append(websocket)

        client = Client(
            ts_client=websocket.path_params['ts_client'],
            id_client=0,
            name="",
            ws=websocket
        )
        new_client = ClientManager.newClient(client)

    @classmethod
    def disconnect(cls, websocket: WebSocket):
        cls.active_connections.remove(websocket)

        client_id = ClientManager.checkClient(websocket.path_params['ts_client']) 
        if client_id != 0:
            RoomManager.leaveRoom(client_id)
        ClientManager.removeClient(websocket.path_params['ts_client'])


@router.websocket("/ws/{ts_client}")
async def websocket_endpoint(websocket: WebSocket, ts_client: int):
    await ConnectionManager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            Engine.engineSeletor(data)
            # Procesar datos
            # call to engine and precces data
    except WebSocketDisconnect:
        ConnectionManager.disconnect(websocket)