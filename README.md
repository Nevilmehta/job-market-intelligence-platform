Proper Backend Project: Internal Data Platform
--------------------------------------------------

JOB MARKET INTELLIGENCE PLATFORM (Currently working and updating daily)

A production-style internal platform that ingests data from external/internal sources, validates and stores raw data, runs ETL pipelines to produce analytics tables, exposes APIs for querying metrics/reports, and includes job orchestration, observability, testing, and containerized deployment.

After writing all this APIs,
Client → API → pipeline runs immediately → response after completion

After including Celery into this Application,
Client → API → Celery task queued → immediate response
                        ↓
            Worker executes later

Docker for redis,
FastAPI (local)
   ↓
Redis (Docker container)
   ↓
Celery worker (local)

future architecute(we will build it later):
[ FastAPI container ]
[ Celery worker container ]
[ Redis container ]
[ Postgres container ]
[ Celery beat container ]
managed by docker-compose up

start celery worker,
celery -A app.tasks.celery_app.celery_app worker --loglevel=info

prefork ❌	multiprocessing (breaks on Windows)
solo ✅	single process (stable on Windows)

Celery's prefork pool has compatibility issues on Windows, so I configured the worker to use the solo execution pool during development.
celery -A app.tasks.celery_app.celery_app worker --loglevel=info --pool=solo

Integrated Celery and Redis to execute ETL and analytics workflows asynchronously, allowing validation, analytics generation, and backfill jobs to run outside the request-response cycle.