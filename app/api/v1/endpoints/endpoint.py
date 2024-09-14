from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from app.core.dependencies import *
from app.model.base import Client, ClientManager, Room, RoomManager

router = APIRouter()

@router.post("/newRoom", response_class=JSONResponse)
def newRoom(client: Client):
    # TODO: remove data: Room arg
    room = RoomManager.newRoom()

    new_client = ClientManager.checkClient(client.ts_client)
    if new_client == 0:
        new_client = ClientManager.newClient(client)
    client = ClientManager.client_list[new_client]
    room.users = [client]

    RoomManager.addRoom(room)
    client_safe = {'id_client': client.id_client, 'name': client.name}
    return {"id_room": room.id_room, "client": client_safe, "opt": room.opt}

@router.post("/joinRoom", response_class=JSONResponse)
def joinRoom(data: Room, client: Client):
    try:
        room = RoomManager.getRoom(data.id_room)
        # data.creator is a new user
        new_client = ClientManager.checkClient(client.ts_client)
        if new_client == 0:
            new_client = ClientManager.newClient(client)
        client = ClientManager.client_list[new_client]
        room.users.append(client)
        # Update Room and add new client
        RoomManager.addRoom(room)
        client_safe = {'id_client': client.id_client, 'name': client.name}
        return {"id_room": room.id_room, "client": client_safe, "opt": room.opt}
    except Exception as error:
        raise HTTPException(status_code=404, detail="Room not found")

@router.get("/room_info", response_class=JSONResponse)
def room_info(request: Request):
    return {"data": RoomManager.info()}

@router.get("/video/{video_name}")
async def stream_video(video_name: str):
    video_path = f"videos/{video_name}"
    video_path = "/mnt/chromeos/GoogleDrive/MyDrive/github/fastAPI/fastapi_app/Dasha - Austin (Official Music Video) [FyjnbSsZ2tc].mp4"
    try:
        file = open(video_path, "rb")
        return StreamingResponse(file, media_type="video/mp4")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video not found")

@router.get("/audio/{audio_name}")
async def stream_audio(audio_name: str):
    audio_path = f"audios/{audio_name}"
    try:
        file = open(audio_path, "rb")
        return StreamingResponse(file, media_type="audio/mpeg")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio not found")