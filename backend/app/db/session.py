from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from app.core.config import settings
from app.db.base import Base
from app.db import models as db_models

engine = create_engine(settings.database_url, echo=settings.db_echo, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def initialize_database() -> None:
    # Ensure ORM models are imported so metadata includes all tables.
    _ = db_models

    schema = settings.db_schema
    quoted_schema = engine.dialect.identifier_preparer.quote(schema)

    with engine.begin() as connection:
        connection.execute(CreateSchema(schema, if_not_exists=True))
        connection.execute(text(f"SET LOCAL search_path TO {quoted_schema}, public"))
        Base.metadata.create_all(bind=connection)
