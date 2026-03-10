from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

# defines response and request shape
class JobIngestionRequest(BaseModel):
    source: str = Field(..., example="linkedin")
    external_id: str = Field(..., example="job-12345")
    payload: dict[str, Any]

class JobIngestionResponse(BaseModel):
    id: int
    source: str
    external_id: str
    ingested_at: datetime
    message: str
