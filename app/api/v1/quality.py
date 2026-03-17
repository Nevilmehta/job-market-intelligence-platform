from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.quality import (
    QualitySummaryResponse,
    RejectionJobItemResponse,
    RejectionJobListResponse,
    RejectionReasonListResponse,
    RejectionReasonResponse
)
from app.services.quality_service import QualityService

router = APIRouter(prefix="/quality", tags=["Quality"])

@router.get("/summary", response_model=QualitySummaryResponse)
def get_quality_summary(db: Session = Depends(get_db)):
    service = QualityService(db)
    result = service.get_quality_summary()
    return QualitySummaryResponse(**result)

@router.get("/rejection-reasons", response_model=RejectionReasonListResponse)
def get_rejection_reason_breakdown(db: Session = Depends(get_db)):
    service = QualityService(db)
    rows = service.get_rejection_reason_breakdown()
    return RejectionReasonListResponse(
        items= [
            RejectionReasonResponse(
                error_reason=row["error_reason"],
                count=row["count"]
            )
            for row in rows
        ]
    )

@router.get("/rejected_jobs", response_model=RejectionJobListResponse)
def get_recent_rejected_jobs(limit: int = Query(default=10, ge=1, le=100), db:Session = Depends(get_db)):
    service = QualityService(db)
    rows = service.get_recent_rejected_jobs(limit=limit)

    return RejectionJobListResponse(
        items = [
            RejectionJobItemResponse(
                id=row.id,
                source=row.source,
                external_id=row.external_id,
                error_reason=row.error_reason
            )
            for row in rows
        ]
    )