from datetime import datetime

from pydantic import Field, field_validator

from app.schemas.common import APIModel
from app.schemas.job import JobDetailResponse, validate_required_string


class QueueClaimRequest(APIModel):
    worker_id: str = Field(alias="workerId")
    lease_seconds: int = Field(default=300, alias="leaseSeconds", ge=30, le=86400)

    _validate_worker_id = field_validator("worker_id")(validate_required_string)


class QueueHeartbeatRequest(APIModel):
    worker_id: str = Field(alias="workerId")
    lease_seconds: int = Field(default=300, alias="leaseSeconds", ge=30, le=86400)
    heartbeat_at: datetime | None = Field(default=None, alias="heartbeatAt")

    _validate_worker_id = field_validator("worker_id")(validate_required_string)


class QueueStatusUpdateRequest(APIModel):
    worker_id: str = Field(alias="workerId")
    message: str | None = None
    external_job_id: str | None = Field(default=None, alias="externalJobId")
    metadata_json: dict = Field(default_factory=dict, alias="metadata")

    _validate_worker_id = field_validator("worker_id")(validate_required_string)


class QueueClaimResponse(APIModel):
    job: JobDetailResponse | None
    message: str
