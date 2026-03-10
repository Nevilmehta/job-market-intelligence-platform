from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.core.database import Base

# This table stores the original incoming data exactly as received.

class RawJob(Base):
    __tablename__="raw_jobs"

    # duplicate harder at database level
    __table_args__=(
        UniqueConstraint("source", "external_id", name="uq_raw_jobs_source_external_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False, index=True)
    external_id = Column(String, nullable=False, index=True)
    payload = Column(JSONB, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_processed = Column(Boolean, nullable=False, default=False, server_default="false")
    processed_at = Column(DateTime(timezone=True), nullable=True)
