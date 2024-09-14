import json
import asyncio

from app.core.dependencies import *
from app.model.base import Client, ClientManager, RoomManager

async def video_generator():
    pass

class Engine:
    
    @classmethod
    def engineSeletor(cls, data: str):
        data_parse = json.loads(data)
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(ChatEngine.chatMessage(data_parse))


class ChatEngine:
    
    @classmethod
    async def chatMessage(cls, data: dict):
        room = RoomManager.getRoom(data['id_room'])
        for user in room.users:
            if user.id_client != data['user']['id_client']:
                await cls.broadcastMessage(user, f"{data['user']['name']}: {data['message']}")

    @classmethod
    async def broadcastMessage(cls, client: Any, data: str):
        if client.ws is not None:
            await client.ws.send_text(data)
