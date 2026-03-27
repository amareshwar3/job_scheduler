# Job Scheduler Backend

This backend is a FastAPI service for job creation, queueing, polling support, tracking, logging, and snapshot metadata storage.

It stores:

- the original request from the UI
- the generated Livy payload
- the generated cURL command
- queue state for worker/server polling
- status history
- logs
- snapshots

## Suggested flow

1. Frontend sends the job form payload to `POST /api/v1/jobs`
2. Backend creates a `job_id` and stores the full payload in Postgres
3. Backend creates one queue row in `job_queue`
4. A future worker/server calls `POST /api/v1/queue/claim`
5. Worker/server sends heartbeats and completion/failure updates
6. UI polls `GET /api/v1/jobs/{job_id}` or `GET /api/v1/jobs/{job_id}/tracking`

## Why this schema works

- `jobs` is the anchor table
- every job has a UUID primary key plus a human-readable `public_job_id`
- `job_queue` keeps queue state in the database
- `job_status_history` gives an audit trail
- `job_logs` stores API or worker logs
- `job_snapshots` stores snapshot metadata and snapshot storage paths

## API summary

- `GET /api/v1/health`
- `POST /api/v1/jobs`
- `GET /api/v1/jobs`
- `GET /api/v1/jobs/{job_id}`
- `GET /api/v1/jobs/{job_id}/tracking`
- `POST /api/v1/jobs/{job_id}/logs`
- `GET /api/v1/jobs/{job_id}/logs`
- `POST /api/v1/jobs/{job_id}/snapshots`
- `GET /api/v1/jobs/{job_id}/snapshots`
- `POST /api/v1/queue/claim`
- `POST /api/v1/queue/{job_id}/heartbeat`
- `POST /api/v1/queue/{job_id}/complete`
- `POST /api/v1/queue/{job_id}/fail`

## Run locally

```powershell
cd C:\Users\anamp\OneDrive\Desktop\job_scheduler\backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Update `.env` before starting the app.

## Frontend payload expected by `POST /api/v1/jobs`

```json
{
  "batchName": "daily_customer_snapshot",
  "mainFile": "hdfs:///jobs/main.py",
  "pythonEggWheelFiles": ["hdfs:///libs/job.whl"],
  "dependencyFiles": ["hdfs:///configs/app.yaml"],
  "sparkConfiguration": {
    "sparkPysparkPython": "/usr/bin/python3",
    "sparkPysparkDriverPython": "/usr/bin/python3"
  },
  "jobArguments": {
    "outputFilesPath": "hdfs:///output/customer",
    "checkpointsHdfsPath": "hdfs:///checkpoints/customer",
    "hiveOutputSchema": "analytics",
    "logPath": "hdfs:///logs/customer",
    "hivePrefix": "customer_daily",
    "interval": "7",
    "numSnapshots": "10",
    "sparkConfig": "driver-memory=4g"
  },
  "priority": 100
}
```

## Important env values

- `DATABASE_URL`
- `DB_SCHEMA`
- `CORS_ORIGINS`

For database creation and connection steps, read `DATABASE_SETUP.md`.
