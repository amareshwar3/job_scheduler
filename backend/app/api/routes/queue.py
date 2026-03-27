from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.queue import (
    QueueClaimRequest,
    QueueClaimResponse,
    QueueHeartbeatRequest,
    QueueStatusUpdateRequest,
)
from app.services.job_service import JobService

router = APIRouter()


def service_factory(db: Session = Depends(get_db)) -> JobService:
    return JobService(db)


@router.post("/claim", response_model=QueueClaimResponse)
def claim_next_job(
    payload: QueueClaimRequest,
    service: JobService = Depends(service_factory),
) -> QueueClaimResponse:
    claim = service.claim_next_job(payload)
    if claim is None:
        return QueueClaimResponse(job=None, message="No queued job available.")
    return QueueClaimResponse(job=claim, message="Queued job claimed successfully.")


@router.post("/{job_id}/heartbeat", response_model=QueueClaimResponse)
def heartbeat(
    job_id: UUID,
    payload: QueueHeartbeatRequest,
    service: JobService = Depends(service_factory),
) -> QueueClaimResponse:
    claim = service.heartbeat(job_id=job_id, payload=payload)
    if claim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue item not found.")
    return QueueClaimResponse(job=claim, message="Heartbeat updated.")


@router.post("/{job_id}/complete", response_model=QueueClaimResponse)
def complete_job(
    job_id: UUID,
    payload: QueueStatusUpdateRequest,
    service: JobService = Depends(service_factory),
) -> QueueClaimResponse:
    claim = service.complete_job(job_id=job_id, payload=payload)
    if claim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue item not found.")
    return QueueClaimResponse(job=claim, message="Job marked as completed.")


@router.post("/{job_id}/fail", response_model=QueueClaimResponse)
def fail_job(
    job_id: UUID,
    payload: QueueStatusUpdateRequest,
    service: JobService = Depends(service_factory),
) -> QueueClaimResponse:
    claim = service.fail_job(job_id=job_id, payload=payload)
    if claim is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue item not found.")
    return QueueClaimResponse(job=claim, message="Job marked as failed.")
