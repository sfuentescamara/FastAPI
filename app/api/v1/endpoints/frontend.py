from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.core.dependencies import *
from app.model.base import Room, RoomManager

router = APIRouter()

templates = Jinja2Templates(directory="app/api/v1/templates")

@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/room/", response_class=HTMLResponse)
def room_page(request: Request, room: Room):
    return templates.TemplateResponse("room.html", {"request": request, "id_room": room.id_room})
