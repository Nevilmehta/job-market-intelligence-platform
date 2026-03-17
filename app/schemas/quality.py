from pydantic import BaseModel

class QualitySummaryResponse(BaseModel):
    total_raw_jobs: int
    processed_raw_jobs: int
    unprocessed_raw_jobs: int
    total_rejected_jobs: int
    processing_rate_percent: float

class RejectionReasonResponse(BaseModel):
    error_reason: str
    count: int

class RejectionReasonListResponse(BaseModel):
    items: list[RejectionReasonResponse]

class RejectionJobItemResponse(BaseModel):
    id: int
    source: str
    eternal_id: str|None
    error_reason: str

class RejectionJobListResponse(BaseModel):
    items: list[RejectionJobItemResponse]