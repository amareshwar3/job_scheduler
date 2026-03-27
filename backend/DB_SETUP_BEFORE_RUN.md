# SQL Commands to Run Before Backend

Run these commands in DBeaver SQL Editor (or any Postgres client) before starting the backend:

```sql
-- Create the schema if it does not exist
CREATE SCHEMA IF NOT EXISTS job_scheduler;

-- Optional: set privileges for your DB user only on this schema
-- Replace my_user with your real username
GRANT USAGE, CREATE ON SCHEMA job_scheduler TO my_user;

-- (Optional) List all tables in the schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'job_scheduler';

-- Optional safety check: verify tables in other schemas are untouched
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema IN ('public', 'job_scheduler')
ORDER BY table_schema, table_name;
```

**Instructions:**
- Use your existing database (do not create a new one if not needed).
- Only the `job_scheduler` schema will be used for all tables.
- No other schemas will be created by the backend.
- All backend tables will be created automatically in this schema on first run.

**.env Example:**
```
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:<port>/<dbname>
DB_SCHEMA=job_scheduler
```

If you must use psycopg2 driver explicitly, use this URL format:
```
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:<port>/<dbname>
DB_SCHEMA=job_scheduler
```

Replace `<user>`, `<password>`, `<host>`, `<port>`, and `<dbname>` with your actual credentials.

**You do not need to manually create tables. The backend will do this on startup.**

Important safety note:
- Do not run DROP SCHEMA, DROP TABLE, or TRUNCATE statements in shared databases unless you are absolutely sure.
