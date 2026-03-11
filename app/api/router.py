from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.pipelines import router as pipelines_router
from app.api.v1.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/v1")
api_router.include_router(ingestion_router, prefix="/v1")
api_router.include_router(pipelines_router, prefix="/v1")
api_router.include_router(analytics_router, prefix="/v1")