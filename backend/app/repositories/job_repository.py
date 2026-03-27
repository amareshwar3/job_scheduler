from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import JobLifecycleStatus, QueueItemStatus
from app.db.models import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, job: Job) -> Job:
        self.db.add(job)
        return job

    def list(
        self,
        *,
        status_filter: JobLifecycleStatus | None,
        queue_status_filter: QueueItemStatus | None,
        limit: int,
        offset: int,
    ) -> list[Job]:
        stmt = (
            select(Job)
            .options(
                joinedload(Job.queue_item),
                joinedload(Job.status_history),
                joinedload(Job.logs),
                joinedload(Job.snapshots),
            )
            .order_by(Job.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if status_filter:
            stmt = stmt.where(Job.current_status == status_filter)
        if queue_status_filter:
            stmt = stmt.where(Job.queue_status == queue_status_filter)
        return list(self.db.scalars(stmt).unique().all())

    def get(self, job_id: UUID) -> Job | None:
        stmt = (
            select(Job)
            .options(
                joinedload(Job.queue_item),
                joinedload(Job.status_history),
                joinedload(Job.logs),
                joinedload(Job.snapshots),
            )
            .where(Job.id == job_id)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()
