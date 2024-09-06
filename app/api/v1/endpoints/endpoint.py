from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from app.core.dependencies import *
from app.model.base import ClientManager, Room, RoomManager

router = APIRouter()

@router.post("/newRoom", response_class=JSONResponse)
def newRoom(data: Room):
    data.id_room = RoomManager.getNewIdRoom()
    if data.creator.name == "":
        data.creator.name = f"Guest-{data.id_room[-5:]}"
        data.creator.id_client = ClientManager.getIdClient()
        data.users = [data.creator]
    RoomManager.addRoom(data)
    return {"data": data}

@router.get("/room_info", response_class=JSONResponse)
def room_info(request: Request):
    return {"data": RoomManager.rooms}

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