from fastapi import APIRouter

from app.api.agent import router as agent_router
from app.api.appointments import router as appointments_router
from app.api.health import router as health_router
from app.api.products import router as products_router
from app.api.support import router as support_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(products_router)
api_router.include_router(appointments_router)
api_router.include_router(support_router)
api_router.include_router(agent_router)
