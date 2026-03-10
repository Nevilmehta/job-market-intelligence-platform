from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.core.database import Base

class RejectedJob(Base):
    __tablename__ = "rejected_jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False, index=True)
    external_id = Column(String, nullable=True, index=True)
    payload = Column(JSONB, nullable=False)
    error_reason = Column(String, nullable=False)
    rejected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)