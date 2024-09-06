from fastapi.staticfiles import StaticFiles

from app.api.v1.routes import routers as v1
from app.core.dependencies import *
from app.core.config import configs
from app.core.connection import router as connection_routers

class myFastAPI():
    def __init__(self) -> None:
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )


        # set routes
        @self.app.get("/hello")
        def root():
            return "service is working"

        self.app.mount("/static", StaticFiles(directory="app/api/v1/static"))
        self.app.include_router(v1, prefix=configs.API_V1_STR)
        self.app.include_router(connection_routers)

        # self.app.include_router(v2_routers, prefix=configs.API_V2_STR)

app = myFastAPI()
app = app.app