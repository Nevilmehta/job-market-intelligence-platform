from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pipeline import (
    ValidationPipelineResponse,
    TaskQueuedResponse,
    ETLJobRunListResponse,
    ETLJobRunResponse,
    AnalyticsBackfillRequest,
    AnalyticsBackfillResponse
    )
from app.services.validation_service import ValidationService
from app.services.pipeline_service import PipelineService
from app.tasks.analytics_tasks import generate_core_analytics_task
from app.tasks.backfill_tasks import backfill_analytics_task
from app.tasks.validation_tasks import validate_raw_jobs_task

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])
# This route triggers the validation pipeline manually.

@router.post("/validate-raw-jobs", response_model=ValidationPipelineResponse)
def validate_raw_jobs(db: Session = Depends(get_db)):
    service = ValidationService(db)
    result = service.process_raw_jobs()
    return ValidationPipelineResponse(**result)

@router.post("/validate-raw-jobs/async", response_model=TaskQueuedResponse)
def validate_raw_jobs_async():
    task = validate_raw_jobs_task.delay()
    return TaskQueuedResponse(
        task_id=task.id,
        task_name="validate_raw_jobs",
        message="Validation pipeline task queued successfully"
    )

@router.post("/generate-analytics/async", response_model=TaskQueuedResponse)
def generate_analytics_async():
    task = generate_core_analytics_task.delay()
    return TaskQueuedResponse(
        task_id=task.id,
        task_name="generate_core_analytics",
        message="Analytics generation task queued successfully"
    )

@router.post("/backfill-analytics", response_model=AnalyticsBackfillResponse)
def backfill_analytics(request: AnalyticsBackfillRequest, db: Session = Depends(get_db)):
    service = PipelineService(db)
    result = service.backfill_analytics(
        date_from=request.date_from,
        date_to=request.date_to
    )
    return AnalyticsBackfillResponse(**result)

@router.post("/backfill-analytics/async", response_model=TaskQueuedResponse)
def backfill_analytics_async(request: AnalyticsBackfillRequest):
    task = backfill_analytics_task.delay(
        request.date_from.isoformat(),
        request.date_to.isoformat()
    )
    return TaskQueuedResponse(
        task_id=task.id,
        task_name="backfill_analytics",
        message="Analytics backfill task queued successfully"
    )

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