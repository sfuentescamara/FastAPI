from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from app.dependencies import *

router = APIRouter()

templates = Jinja2Templates(directory="app/api/v1/endpoints/templates")
router.mount("/static", StaticFiles(directory="app/api/v1/endpoints/static"))

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/2", response_class=HTMLResponse)
def read_root2(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
