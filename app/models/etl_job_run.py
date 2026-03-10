from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

class ETLJobRun(Base):
    __tablename__="etl_job_runs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    records_processed = Column(Integer, nullable=False, default=0)
    records_failed = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)