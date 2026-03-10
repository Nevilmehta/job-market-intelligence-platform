from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.core.database import Base

# this is ur cleaned structured table
class StagingJob(Base):
    __tablename__="staging_jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False, index=True)
    external_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True, index=True)
    salary_text = Column(String, nullable=True)
    technologies = Column(JSONB, nullable=True)
    posted_date = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)