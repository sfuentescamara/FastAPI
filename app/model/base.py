from pydantic import BaseModel

from app.core.dependencies import *
from app.core.utils import generate_id


class Client(BaseModel):
    ts_client: str
    id_client: int
    name: str
    
class Client(BaseModel):
    ts_client: str
    id_client: int
    name: str
    ws: Any

class ClientManager:
    n_client = 0
    client_list: Dict[int, Client] = {}
    ts_id_client: Dict[str, int] = {}

    @classmethod
    def newClient(cls, new_client: Client):
        """ Adds new client to list and returns its obj """
        new_client.id_client = cls.getIdClient()
        if new_client.name == "":
            new_client.name = f"Guest-{str(new_client.id_client).zfill(5)}"
        ClientManager.ts_id_client[new_client.ts_client] = new_client.id_client
        ClientManager.client_list[new_client.id_client] = new_client
        return new_client

    @classmethod
    def getIdClient(cls) -> int:
        ClientManager.n_client += 1
        return ClientManager.n_client

    @classmethod
    def checkClient(cls, ts_client: str) -> int:
        """ Checks if client exist an return its id """
        if ts_client in ClientManager.ts_id_client:
            return ClientManager.ts_id_client[ts_client]
        return 0

    @classmethod
    def removeClient(cls, ts_client: str) -> int:
        if ts_client in ClientManager.ts_id_client:
            id_client = ClientManager.ts_id_client.pop(ts_client)
            ClientManager.client_list.pop(id_client)
            return 1
        return 0

class Room(BaseModel):
    id_room: str
    users: List[Client]
    opt: Any

class RoomManager():
    # rooms: Dict[id_room, Room]
    rooms_list: Dict[str, Room] = {}
    # client_room: Dict[id_client, id_room]
    client_room: Dict[str, str] = {}

    @classmethod
    def info(cls):
        rooms_info_list = []
        # Remove key ws od clients and return rooms
        for id_room, room in cls.rooms_list.items():
            room_info = room.copy()
            room_info.users = room.users.copy()

            for client in room_info.users:
                client.ws = None
            rooms_info_list.append(room_info)
        return rooms_info_list

    @classmethod
    def newRoom(cls):
        return Room(
            id_room = RoomManager.getNewIdRoom(),
            users = [],
            opt = {}
        )

    @classmethod
    def addRoom(cls, data: Room):
        # id_client
        cls.client_room[data.users[-1].id_client] = data.id_room
        cls.rooms_list[data.id_room] = data

    @classmethod
    def getNewIdRoom(cls) -> str:
        return generate_id()
    
    @classmethod
    def getRoom(cls, id_room: str) -> Room:
        try:
            return cls.rooms_list[id_room]
        except KeyError:
            raise Exception("Room not found")

    @classmethod
    def emptyRoom(cls, id_room: str) -> bool:
        room = cls.getRoom(id_room)
        if len(room.users) == 0:
            return True
        return False

    @classmethod
    def leaveRoom(cls, id_client) -> bool:
        """ Removes client of the room """
        if id_client in cls.client_room.keys():# and cls.rooms_list[id_client].users == []:
            id_room = cls.client_room[id_client]
            client = ClientManager.client_list[id_client]
            cls.rooms_list[id_room].users.remove(client)
            cls.client_room.pop(id_client)
            
            cls.closeRoom(id_room)
            return True
        return False

    @classmethod
    def closeRoom(cls, id_room) -> bool:
        if cls.emptyRoom(id_room):
            cls.rooms_list.pop(id_room)
            return True
        return False
