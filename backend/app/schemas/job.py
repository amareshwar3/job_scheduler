from datetime import datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.core.enums import LogLevel, SnapshotStatus
from app.schemas.common import APIModel


def validate_required_string(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("This field is required.")
    return cleaned


class SparkConfigurationInput(APIModel):
    spark_pyspark_python: str = Field(alias="sparkPysparkPython")
    spark_pyspark_driver_python: str = Field(alias="sparkPysparkDriverPython")

    _validate_python = field_validator("spark_pyspark_python")(validate_required_string)
    _validate_driver = field_validator("spark_pyspark_driver_python")(validate_required_string)


class JobArgumentsInput(APIModel):
    output_files_path: str = Field(alias="outputFilesPath")
    checkpoints_hdfs_path: str = Field(alias="checkpointsHdfsPath")
    hive_output_schema: str = Field(alias="hiveOutputSchema")
    log_path: str = Field(alias="logPath")
    hive_prefix: str = Field(alias="hivePrefix")
    interval: str
    num_snapshots: str = Field(alias="numSnapshots")
    spark_config: str = Field(alias="sparkConfig")

    _validate_output_files_path = field_validator("output_files_path")(validate_required_string)
    _validate_checkpoints_hdfs_path = field_validator("checkpoints_hdfs_path")(validate_required_string)
    _validate_hive_output_schema = field_validator("hive_output_schema")(validate_required_string)
    _validate_log_path = field_validator("log_path")(validate_required_string)
    _validate_hive_prefix = field_validator("hive_prefix")(validate_required_string)
    _validate_interval = field_validator("interval")(validate_required_string)
    _validate_num_snapshots = field_validator("num_snapshots")(validate_required_string)
    _validate_spark_config = field_validator("spark_config")(validate_required_string)


class JobCreateRequest(APIModel):
    batch_name: str = Field(alias="batchName")
    main_file: str = Field(alias="mainFile")
    python_egg_wheel_files: list[str] = Field(default_factory=list, alias="pythonEggWheelFiles")
    dependency_files: list[str] = Field(default_factory=list, alias="dependencyFiles")
    spark_configuration: SparkConfigurationInput = Field(alias="sparkConfiguration")
    job_arguments: JobArgumentsInput = Field(alias="jobArguments")
    priority: int | None = Field(default=None, ge=1, le=1000)

    _validate_batch_name = field_validator("batch_name")(validate_required_string)
    _validate_main_file = field_validator("main_file")(validate_required_string)

    @field_validator("python_egg_wheel_files", "dependency_files")
    @classmethod
    def trim_list(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item.strip()]


class JobLogCreateRequest(APIModel):
    level: LogLevel = LogLevel.INFO
    source: str = "api"
    message: str
    metadata_json: dict = Field(default_factory=dict, alias="metadata")

    _validate_message = field_validator("message")(validate_required_string)
    _validate_source = field_validator("source")(validate_required_string)


class JobSnapshotCreateRequest(APIModel):
    snapshot_name: str = Field(alias="snapshotName")
    snapshot_type: str = Field(alias="snapshotType")
    storage_path: str | None = Field(default=None, alias="storagePath")
    snapshot_status: SnapshotStatus = Field(default=SnapshotStatus.CREATED, alias="snapshotStatus")
    payload: dict = Field(default_factory=dict)

    _validate_snapshot_name = field_validator("snapshot_name")(validate_required_string)
    _validate_snapshot_type = field_validator("snapshot_type")(validate_required_string)


class JobStatusHistoryResponse(APIModel):
    id: UUID
    from_status: str | None
    to_status: str
    source: str
    message: str | None
    metadata_json: dict
    created_at: datetime


class JobLogResponse(APIModel):
    id: UUID
    job_id: UUID
    level: LogLevel
    source: str
    message: str
    metadata_json: dict
    log_timestamp: datetime
    created_at: datetime


class JobSnapshotResponse(APIModel):
    id: UUID
    job_id: UUID
    snapshot_name: str
    snapshot_type: str
    snapshot_status: SnapshotStatus
    storage_path: str | None
    payload: dict
    created_at: datetime


class QueueItemResponse(APIModel):
    id: UUID
    status: str
    priority: int
    attempts: int
    max_attempts: int
    worker_id: str | None
    available_at: datetime
    claimed_at: datetime | None
    heartbeat_at: datetime | None
    lease_expires_at: datetime | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime


class JobDetailResponse(APIModel):
    id: UUID
    public_job_id: str
    batch_name: str
    main_file: str
    python_egg_wheel_files: list[str]
    dependency_files: list[str]
    spark_conf: dict
    command_arguments: dict
    livy_payload: dict
    generated_command: str
    request_payload: dict
    output_files_path: str
    checkpoints_hdfs_path: str
    hive_output_schema: str
    log_path: str
    hive_prefix: str
    interval: str
    num_snapshots: str
    spark_config: str
    current_status: str
    queue_status: str
    external_job_id: str | None
    storage_resource_path: str
    submitted_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    last_polled_at: datetime | None
    created_at: datetime
    updated_at: datetime
    queue_item: QueueItemResponse | None
    status_history: list[JobStatusHistoryResponse]
    logs: list[JobLogResponse]
    snapshots: list[JobSnapshotResponse]


class JobListResponse(APIModel):
    items: list[JobDetailResponse]
    count: int
