# Database Setup Guide

This guide explains how to create a new Postgres database or schema for this project, connect it from the backend, and understand what the backend will create.

## Recommended isolation

Safest option:

1. Create a brand new database for this project if your access allows it
2. Create a dedicated schema such as `job_scheduler`
3. Point this backend only to that database and schema

If a separate database is not allowed, create a new schema inside the existing database and use that schema only for this project.

## DBeaver steps

### Option A: create a new database

1. Open DBeaver and connect to your Postgres server
2. In Database Navigator, expand the server connection
3. Right-click `Databases`
4. Click `Create New Database`
5. Enter a name such as `job_scheduler_db`
6. Save

### Option B: create a new schema

1. Open the target database
2. Expand it in DBeaver
3. Right-click `Schemas`
4. Click `Create New Schema`
5. Enter `job_scheduler`
6. Save

## SQL option

Run this in DBeaver SQL Editor if you have permission:

```sql
CREATE DATABASE job_scheduler_db;
```

Then connect to that database and run:

```sql
CREATE SCHEMA IF NOT EXISTS job_scheduler;
```

The repository also contains `backend_sql/bootstrap_schema.sql`.

## Connect the backend

Copy `.env.example` to `.env`, then update:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/job_scheduler_db
DB_SCHEMA=job_scheduler
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:secret@localhost:5432/job_scheduler_db
DB_SCHEMA=job_scheduler
```

## What to update in code later

Normally, no Python code changes are required after DB creation. You only need to update:

- `DATABASE_URL`
- `DB_SCHEMA`
- `CORS_ORIGINS`

Only change code if you want different schema names, different table names, or a separate migration system later.

## What the app does on startup

1. Connects using `DATABASE_URL`
2. Creates the configured schema if it does not already exist
3. Creates all required tables in that schema

## Tables created by this backend

- `job_scheduler.jobs`
- `job_scheduler.job_queue`
- `job_scheduler.job_status_history`
- `job_scheduler.job_logs`
- `job_scheduler.job_snapshots`

If you choose another schema, the same tables will be created there instead.

## How jobs are stored

Each submitted job gets:

- an internal UUID `id`
- a readable ID like `JOB-20260327-AB12CD34`
- one main row in `jobs`
- one queue row in `job_queue`
- many optional rows in history, logs, and snapshots

The permanent storage anchor is the `jobs` row. Every related table links back to that `job_id`.

The backend also stores a resource path like:

```text
/api/v1/jobs/<job_uuid>
```

That gives the UI and future worker/server code a stable lookup path.

## Official references

- DBeaver PostgreSQL docs: https://dbeaver.com/docs/dbeaver/PostgreSQL/
- PostgreSQL `CREATE DATABASE`: https://www.postgresql.org/docs/current/sql-createdatabase.html
- PostgreSQL `CREATE SCHEMA`: https://www.postgresql.org/docs/current/sql-createschema.html
- SQLAlchemy engine docs: https://docs.sqlalchemy.org/en/20/core/engines.html
- FastAPI SQL databases tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/
