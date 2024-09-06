from pydantic import BaseModel

from app.core.dependencies import *
from app.core.utils import generate_id

class Client(BaseModel):
    id_client: int
    name: str

class ClientManager:
    n_client = 0

    @classmethod
    def getIdClient(cls) -> int:
        ClientManager.n_client += 1
        return ClientManager.n_client

class Room(BaseModel):
    id_room: str
    creator: Client
    ws_list: List[Any]
    users: List[Client]

class RoomManager():
    rooms = {}

    @classmethod
    def addRoom(cls, data: Room):
        # client_id
        cls.rooms[data.ws_list[0]['url'].split('/')[-1]] = data

    @classmethod
    def getNewIdRoom(cls) -> int:
        return generate_id()
    
    # @classmethod
    # def emptyRoom(cls, client_id) -> bool:
    #     if client_id in cls.rooms.keys():
    #         return True
    #     return False

    @classmethod
    def closeRoom(cls, client_id) -> bool:
        if client_id in cls.rooms.keys():# and cls.rooms[client_id].users == []:
            cls.rooms.pop(client_id)
            return True
        return False
