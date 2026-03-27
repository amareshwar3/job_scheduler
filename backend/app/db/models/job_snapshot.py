import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.core.enums import SnapshotStatus
from app.db.base import Base


class JobSnapshot(Base):
    __tablename__ = "job_snapshots"
    __table_args__ = {"schema": settings.db_schema}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(f"{settings.db_schema}.jobs.id", ondelete="CASCADE"),
        index=True,
    )
    snapshot_name: Mapped[str] = mapped_column(String(255))
    snapshot_type: Mapped[str] = mapped_column(String(120))
    snapshot_status: Mapped[SnapshotStatus] = mapped_column(
        Enum(SnapshotStatus, name="job_snapshot_status", schema=settings.db_schema),
        default=SnapshotStatus.CREATED,
    )
    storage_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="snapshots")
