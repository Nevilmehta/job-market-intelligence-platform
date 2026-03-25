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

“How did you make background jobs reliable?”

You can say:
“I used Celery with Redis for asynchronous pipeline execution, exposed task-status APIs using AsyncResult, and configured automatic retries with backoff for transient failures.”

there are 2 processors now,
1 is for worker and 1 is for beat
celery -A app.tasks.celery_app.celery_app worker --loglevel=info
celery -A app.tasks.celery_app.celery_app beat --loglevel=info

In Beat logs, you’ll see messages like:
Scheduler: Sending due task validate-raw-jobs-every-10-minutes
Then in worker logs, you should see task execution.
So the flow becomes:
Beat decides → Redis queues → Worker executes

Configured Celery Beat to schedule recurring ETL and analytics workflows, enabling automated validation and nightly metric generation outside the request-response cycle.

------------------------------------------------------------------
To keep everything align with one command,(in docker)(keep in docker compose)
requirements.text
.dockerignore
.env => localhost-db, localhost-redis
Dockerfile
docker-compose.yaml

docker compose up --build
docker compose down -v (for complete clean)
docker ps
docker compose ps
docker compose ps -a
docker compose up --build worker beat (if it wont start )
docker compose logs -f api/worker/beat

Why this works
It:
uses Python 3.12
installs dependencies
copies your project
starts FastAPI

Worker and Beat will reuse this same image, but with different commands.

Containerized a multi-service backend platform with Docker Compose, orchestrating FastAPI, PostgreSQL, Redis, Celery workers, and Celery Beat for local development and scheduled ETL execution.

Alembic and migrations
alembic init migrations
alembic upgrade head
alembic revision --autogenerate -m "initial schema"

docker compose exec api alembic upgrade head
docker compose exec api printenv DATABASE_URL

to integrate with docker (alembic)

Inside Docker 
api container-> db container
localhost-> db

Outside Docker
your laptop-> local postgres
db-> localhost

Local
.env.local → localhost
Docker
.env.docker → db / redis