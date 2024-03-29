from fastapi.routing import APIRouter

from app.api.endpoints.health import healthcheck
from app.api.endpoints.images import images_router
from app.api.endpoints.throttling import throttling

api_router = APIRouter(prefix='/api')
api_router.include_router(healthcheck)
api_router.include_router(images_router)
api_router.include_router(throttling)
