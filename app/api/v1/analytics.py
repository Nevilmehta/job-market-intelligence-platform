from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import (
    AnalyticsGenerationResponse,
    JobDailyCountListResponse,
    JobDailyCountResponse,
    TopCompanyListResponse,
    TopCompanyResponse,
    TopSkillListResponse,
    TopSkillResponse,
    SalaryTrendResponse,
    SalaryTrendListResponse
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# one route to generate analytics and two routes to fetch analytics
@router.post("/generate", response_model=AnalyticsGenerationResponse)
def generate_analytics(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    result = service.generate_core_analytics()
    return AnalyticsGenerationResponse(**result)

@router.get("/job-daily-counts", response_model=JobDailyCountListResponse)
def get_job_daily_counts(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    rows = service.get_job_daily_counts()
    return JobDailyCountListResponse(
        items=[
            JobDailyCountResponse(
                metric_date=row.metric_date,
                job_count=row.job_count
            )
            for row in rows
        ]
    )

@router.get("/top-companies", response_model=TopCompanyListResponse)
def get_top_companies(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    rows = service.get_top_companies()

    return TopCompanyListResponse(
        items = [
            TopCompanyResponse(
                company=row.company,
                job_count=row.job_count
            )
            for row in rows
        ]
    )

@router.get("/top-skills", response_model=TopSkillListResponse)
def get_top_skills(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    rows = service.get_top_skills()

    return TopSkillListResponse(
        items = [
            TopSkillResponse(
                skill=row.skill,
                demand_count=row.demand_count
            )
            for row in rows
        ]
    )

@router.get("/salary-trends", response_model=SalaryTrendListResponse)
def get_salary_trends(db:Session = Depends(get_db)):
    service = AnalyticsService(db)
    rows = service.get_salary_trends()

    return SalaryTrendListResponse(
        items=[
            SalaryTrendResponse(
                metric_date=row.metric_date,
                average_salary=row.average_salary,
                currency=row.currency,
                job_count=row.job_count
            )
            for row in rows
        ]
    )