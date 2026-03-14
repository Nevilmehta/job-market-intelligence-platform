from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class JobDailyCount(Base):
    __tablename__ = "job_daily_counts"

    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(Date, nullable=False, index=True)
    job_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class TopCompany(Base):
    __tablename__ = "top_companies"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False, index=True)
    job_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class TopSkill(Base):
    __tablename__ = "top_skills"

    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String, nullable=False, index=True)
    demand_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class SalaryTrend(Base):
    __tablename__ = "salary_trends"

    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(Date, nullable=False, index=True)
    average_salary = Column(Integer, nullable=False)
    currency = Column(String, nullable=True, index=True)
    job_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)