from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pipeline import (
    ValidationPipelineResponse,
    ETLJobRunListResponse,
    ETLJobRunResponse,
    AnalyticsBackfillRequest,
    AnalyticsBackfillResponse
    )
from app.services.validation_service import ValidationService
from app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])
# This route triggers the validation pipeline manually.

@router.post("/validate-raw-jobs", response_model=ValidationPipelineResponse)
def validate_raw_jobs(db: Session = Depends(get_db)):
    service = ValidationService(db)
    result = service.process_raw_jobs()
    return ValidationPipelineResponse(**result)

@router.post("/backfill-analytics", response_model=AnalyticsBackfillResponse)
def backfill_analytics(request: AnalyticsBackfillRequest, db: Session = Depends(get_db)):
    service = PipelineService(db)
    result = service.backfill_analytics(
        date_from=request.date_from,
        date_to=request.date_to
    )
    return AnalyticsBackfillResponse(**result)

@router.get("/runs", response_model=ETLJobRunListResponse)
def list_pipeline_runs(db: Session = Depends(get_db)):
    service = PipelineService(db)
    runs = service.list_pipeline_runs()

    return ETLJobRunListResponse(
        runs = [
            ETLJobRunResponse(
                id=run.id,
                job_name=run.job_name,
                status=run.status,
                records_processed=run.records_processed,
                records_failed=run.records_failed,
                started_at=run.started_at,
                ended_at=run.ended_at,
                error_message=run.error_message,
            )
            for run in runs
        ]
    )

@router.get("/runs/{run_id}", response_model = ETLJobRunResponse)
def get_pipeline_run(run_id: int, db: Session = Depends(get_db)):
    service = PipelineService(db)
    run = service.get_pipeline_run(run_id)

    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run with id={run_id} not found.",
        )

    return ETLJobRunResponse(
        id=run.id,
        job_name=run.job_name,
        status=run.status,
        records_processed=run.records_processed,
        records_failed=run.records_failed,
        started_at=run.started_at,
        ended_at=run.ended_at,
        error_message=run.error_message,
    )