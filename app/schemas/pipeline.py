from pydantic import BaseModel
from typing import Any
from datetime import date, datetime

# This schema will be used for pipeline responses.
class ValidationPipelineResponse(BaseModel):
    total_records: int
    valid_records: int 
    rejected_records: int
    message: str

class ETLJobRunResponse(BaseModel):
    id: int
    job_name: str
    status: str
    records_processed: int
    records_failed: int
    started_at: datetime
    ended_at: datetime | None
    error_message: str | None

class ETLJobRunListResponse(BaseModel):
    runs: list[ETLJobRunResponse]

class AnalyticsBackfillRequest(BaseModel):
    date_from: date
    date_to: date

class AnalyticsBackfillResponse(BaseModel):
    date_from: date
    date_to: date
    daily_metrics_created: int
    salary_trend_rows_created: int
    message: str

# Celery-redis response model for task queuing
class TaskQueuedResponse(BaseModel):
    task_id: str
    task_name: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    state: str
    result: Any | None
    error: str | None