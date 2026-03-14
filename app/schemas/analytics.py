from datetime import date
from pydantic import BaseModel

# These schemas define analytics API responses.
class AnalyticsGenerationResponse(BaseModel):
    daily_metrics_created: int
    top_company_rows_created: int
    top_skill_rows_created: int
    salary_trend_rows_created: int
    message: str

class JobDailyCountResponse(BaseModel):
    metric_date: date
    job_count: int

class JobDailyCountListResponse(BaseModel):
    items: list[JobDailyCountResponse]

class TopCompanyResponse(BaseModel):
    company: str
    job_count: int

class TopCompanyListResponse(BaseModel):
    items: list[TopCompanyResponse]

class TopSkillResponse(BaseModel):
    skill: str
    demand_count: int

class TopSkillListResponse(BaseModel):
    items: list[TopSkillResponse]

class SalaryTrendResponse(BaseModel):
    metric_date: date
    average_salary: int
    currency: str|None
    job_count: int

class SalaryTrendListResponse(BaseModel):
    items:list[SalaryTrendResponse]