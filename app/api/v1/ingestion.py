from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import DuplicateRawJobException
from app.schemas.ingestion import JobIngestionRequest, JobIngestionResponse
from app.services.ingestion_service import IngestionService

# This is the router handler
router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/jobs", response_model=JobIngestionResponse, status_code=status.HTTP_201_CREATED)
def ingest_job(request: JobIngestionRequest, db:Session=Depends(get_db)):
    service = IngestionService(db)

    try:
        raw_job = service.ingest_job(request)
    except DuplicateRawJobException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )from exc

    return JobIngestionResponse(
        id=raw_job.id,
        source=raw_job.source,
        external_id=raw_job.external_id,
        ingested_at=raw_job.ingested_at,
        message="Job ingested successfully"
    )