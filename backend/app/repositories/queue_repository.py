from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import QueueItemStatus
from app.db.models import JobQueue


class QueueRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, item: JobQueue) -> JobQueue:
        self.db.add(item)
        return item

    def get_by_job_id(self, job_id: UUID) -> JobQueue | None:
        stmt = (
            select(JobQueue)
            .options(joinedload(JobQueue.job))
            .where(JobQueue.job_id == job_id)
        )
        return self.db.scalar(stmt)

    def get_next_queued_job(self) -> JobQueue | None:
        now = datetime.now(timezone.utc)
        stmt = (
            select(JobQueue)
            .options(joinedload(JobQueue.job))
            .where(JobQueue.status == QueueItemStatus.QUEUED)
            .where(JobQueue.available_at <= now)
            .order_by(JobQueue.priority.asc(), JobQueue.created_at.asc())
            .limit(1)
        )
        return self.db.scalar(stmt)
