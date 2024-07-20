from app.dependencies import *

from app.api.v1.endpoints import frontend, endpoint


app = FastAPI()

app.include_router(frontend.router, prefix="", tags=["frontend"])
app.include_router(endpoint.router, prefix="", tags=["endpoint"])

@app.get("/hello")
def read_root():
    return {"Hello": "World"}
