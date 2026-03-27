from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from app.core.config import settings
from app.db.base import Base
from app.db.models import Job, JobLog, JobQueue, JobSnapshot, JobStatusHistory  # noqa: F401

engine = create_engine(settings.database_url, echo=settings.db_echo, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def initialize_database() -> None:
    with engine.begin() as connection:
        connection.execute(CreateSchema(settings.db_schema, if_not_exists=True))
        connection.execute(text(f"SET search_path TO {settings.db_schema}"))
        Base.metadata.create_all(bind=connection)
