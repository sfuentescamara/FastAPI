from app.core.dependencies import *

from app.api.v1.endpoints.frontend import router as frontend_router
from app.api.v1.endpoints.endpoint import router as endpoint_router

from fastapi import APIRouter

routers = APIRouter()
router_list = [frontend_router, endpoint_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)