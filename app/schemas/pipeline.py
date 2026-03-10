from pydantic import BaseModel
from datetime import datetime

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