from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }