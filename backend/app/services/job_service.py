from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums import JobLifecycleStatus, QueueItemStatus
from app.db.models import Job, JobLog, JobQueue, JobSnapshot, JobStatusHistory
from app.repositories.job_repository import JobRepository
from app.repositories.queue_repository import QueueRepository
from app.schemas.job import (
    JobCreateRequest,
    JobDetailResponse,
    JobListResponse,
    JobLogCreateRequest,
    JobLogResponse,
    JobSnapshotCreateRequest,
    JobSnapshotResponse,
)
from app.schemas.queue import (
    QueueClaimRequest,
    QueueHeartbeatRequest,
    QueueStatusUpdateRequest,
)
from app.utils.command_builder import build_job_record_data, build_public_job_id


class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.jobs = JobRepository(db)
        self.queue = QueueRepository(db)

    def create_job(self, payload: JobCreateRequest) -> JobDetailResponse:
        record = build_job_record_data(payload)
        job = Job(
            public_job_id=build_public_job_id(),
            batch_name=record["batch_name"],
            main_file=record["main_file"],
            python_egg_wheel_files=record["python_egg_wheel_files"],
            dependency_files=record["dependency_files"],
            spark_conf=record["spark_conf"],
            command_arguments=record["command_arguments"],
            livy_payload=record["livy_payload"],
            generated_command=record["generated_command"],
            request_payload=record["request_payload"],
            output_files_path=record["output_files_path"],
            checkpoints_hdfs_path=record["checkpoints_hdfs_path"],
            hive_output_schema=record["hive_output_schema"],
            log_path=record["log_path"],
            hive_prefix=record["hive_prefix"],
            interval=record["interval"],
            num_snapshots=record["num_snapshots"],
            spark_config=record["spark_config"],
            current_status=JobLifecycleStatus.QUEUED,
            queue_status=QueueItemStatus.QUEUED,
            storage_resource_path="pending",
        )
        self.jobs.add(job)
        self.db.flush()

        job.storage_resource_path = f"{settings.api_v1_prefix}/jobs/{job.id}"
        queue_item = JobQueue(
            job_id=job.id,
            status=QueueItemStatus.QUEUED,
            priority=payload.priority or settings.queue_default_priority,
            max_attempts=settings.queue_default_max_attempts,
        )
        self.queue.add(queue_item)

        history = JobStatusHistory(
            job_id=job.id,
            from_status=None,
            to_status=JobLifecycleStatus.QUEUED,
            source="api:create_job",
            message="Job created and queued.",
            metadata_json={"public_job_id": job.public_job_id},
        )
        log = JobLog(
            job_id=job.id,
            source="api:create_job",
            message="Job payload stored successfully.",
            metadata_json={"resource_path": job.storage_resource_path},
        )

        self.db.add_all([history, log])
        self.db.commit()
        self.db.refresh(job)
        return JobDetailResponse.model_validate(job)

    def list_jobs(
        self,
        *,
        status_filter: str | None,
        queue_status_filter: str | None,
        limit: int,
        offset: int,
    ) -> JobListResponse:
        jobs = self.jobs.list(
            status_filter=status_filter,
            queue_status_filter=queue_status_filter,
            limit=limit,
            offset=offset,
        )
        return JobListResponse(
            items=[JobDetailResponse.model_validate(job) for job in jobs],
            count=len(jobs),
        )

    def get_job(self, job_id: UUID) -> JobDetailResponse | None:
        job = self.jobs.get(job_id)
        if job is None:
            return None
        return JobDetailResponse.model_validate(job)

    def add_log(self, job_id: UUID, payload: JobLogCreateRequest) -> JobLogResponse:
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        log = JobLog(
            job_id=job_id,
            level=payload.level,
            source=payload.source,
            message=payload.message,
            metadata_json=payload.metadata_json,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return JobLogResponse.model_validate(log)

    def list_logs(self, job_id: UUID) -> list[JobLogResponse]:
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
        return [JobLogResponse.model_validate(log) for log in job.logs]

    def add_snapshot(self, job_id: UUID, payload: JobSnapshotCreateRequest) -> JobSnapshotResponse:
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        snapshot = JobSnapshot(
            job_id=job_id,
            snapshot_name=payload.snapshot_name,
            snapshot_type=payload.snapshot_type,
            snapshot_status=payload.snapshot_status,
            storage_path=payload.storage_path,
            payload=payload.payload,
        )
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return JobSnapshotResponse.model_validate(snapshot)

    def list_snapshots(self, job_id: UUID) -> list[JobSnapshotResponse]:
        job = self.jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
        return [JobSnapshotResponse.model_validate(snapshot) for snapshot in job.snapshots]

    def claim_next_job(self, payload: QueueClaimRequest) -> JobDetailResponse | None:
        queue_item = self.queue.get_next_queued_job()
        if queue_item is None:
            return None

        now = datetime.now(timezone.utc)
        queue_item.status = QueueItemStatus.CLAIMED
        queue_item.worker_id = payload.worker_id
        queue_item.claimed_at = now
        queue_item.heartbeat_at = now
        queue_item.lease_expires_at = now + timedelta(seconds=payload.lease_seconds)
        queue_item.attempts += 1

        job = queue_item.job
        previous_status = job.current_status
        job.current_status = JobLifecycleStatus.CLAIMED
        job.queue_status = QueueItemStatus.CLAIMED
        job.started_at = now
        job.last_polled_at = now

        self.db.add(
            JobStatusHistory(
                job_id=job.id,
                from_status=str(previous_status),
                to_status=JobLifecycleStatus.CLAIMED,
                source="queue:claim",
                message="Job claimed by worker.",
                metadata_json={"worker_id": payload.worker_id},
            )
        )
        self.db.commit()
        self.db.refresh(job)
        return JobDetailResponse.model_validate(job)

    def heartbeat(self, job_id: UUID, payload: QueueHeartbeatRequest) -> JobDetailResponse | None:
        queue_item = self.queue.get_by_job_id(job_id)
        if queue_item is None:
            return None
        if queue_item.worker_id != payload.worker_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Worker mismatch.")

        heartbeat_at = payload.heartbeat_at or datetime.now(timezone.utc)
        queue_item.heartbeat_at = heartbeat_at
        queue_item.lease_expires_at = heartbeat_at + timedelta(seconds=payload.lease_seconds)
        queue_item.status = QueueItemStatus.RUNNING

        job = queue_item.job
        previous_status = job.current_status
        job.current_status = JobLifecycleStatus.RUNNING
        job.queue_status = QueueItemStatus.RUNNING
        job.last_polled_at = heartbeat_at

        if previous_status != JobLifecycleStatus.RUNNING:
            self.db.add(
                JobStatusHistory(
                    job_id=job.id,
                    from_status=str(previous_status),
                    to_status=JobLifecycleStatus.RUNNING,
                    source="queue:heartbeat",
                    message="Worker heartbeat received.",
                    metadata_json={"worker_id": payload.worker_id},
                )
            )

        self.db.commit()
        self.db.refresh(job)
        return JobDetailResponse.model_validate(job)

    def complete_job(self, job_id: UUID, payload: QueueStatusUpdateRequest) -> JobDetailResponse | None:
        return self._close_job(
            job_id=job_id,
            payload=payload,
            lifecycle_status=JobLifecycleStatus.COMPLETED,
            queue_status=QueueItemStatus.COMPLETED,
            source="queue:complete",
        )

    def fail_job(self, job_id: UUID, payload: QueueStatusUpdateRequest) -> JobDetailResponse | None:
        return self._close_job(
            job_id=job_id,
            payload=payload,
            lifecycle_status=JobLifecycleStatus.FAILED,
            queue_status=QueueItemStatus.FAILED,
            source="queue:fail",
        )

    def _close_job(
        self,
        *,
        job_id: UUID,
        payload: QueueStatusUpdateRequest,
        lifecycle_status: JobLifecycleStatus,
        queue_status: QueueItemStatus,
        source: str,
    ) -> JobDetailResponse | None:
        queue_item = self.queue.get_by_job_id(job_id)
        if queue_item is None:
            return None
        if queue_item.worker_id and queue_item.worker_id != payload.worker_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Worker mismatch.")

        now = datetime.now(timezone.utc)
        queue_item.status = queue_status
        queue_item.heartbeat_at = now
        queue_item.lease_expires_at = now
        if lifecycle_status == JobLifecycleStatus.FAILED:
            queue_item.last_error = payload.message

        job = queue_item.job
        previous_status = job.current_status
        job.current_status = lifecycle_status
        job.queue_status = queue_status
        job.completed_at = now
        job.last_polled_at = now
        if payload.external_job_id:
            job.external_job_id = payload.external_job_id

        self.db.add(
            JobStatusHistory(
                job_id=job.id,
                from_status=str(previous_status),
                to_status=lifecycle_status,
                source=source,
                message=payload.message,
                metadata_json=payload.metadata_json,
            )
        )
        if payload.message:
            self.db.add(
                JobLog(
                    job_id=job.id,
                    source=source,
                    message=payload.message,
                    metadata_json=payload.metadata_json,
                )
            )

        self.db.commit()
        self.db.refresh(job)
        return JobDetailResponse.model_validate(job)
