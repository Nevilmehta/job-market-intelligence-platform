from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
# from app.core.database import Base, engine
# from app.models import (
#     ETLJobRun,
#     JobDailyCount,
#     RawJob,
#     RejectedJob,
#     SalaryTrend,
#     StagingJob,
#     TopCompany,
#     TopSkill
#     )

app = FastAPI(
    title = settings.APP_NAME,
    description = "A Backend platform for ingesting, preocessing and analyzing job market data",
    version = settings.APP_VERSION
)

app.include_router(api_router)

@app.get("/", tags= ["Root"])
def root():
    return{
        "message": "welcome to the {settings.APP_NAME} API"
    }