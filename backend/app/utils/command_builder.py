from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.job import JobCreateRequest

CURL_BASE = [
    "curl -k --negotiate -u : \\",
    '-H "Content-Type: application/json" \\',
    '-H "X-Requested-By: livy" \\',
    "-X POST https://gbl20167161.systems.uk.hsbc:28998/batches \\",
]


def _escape_for_single_quoted_shell(value: str) -> str:
    return value.replace("'", """'"'"'""")


def build_livy_payload(payload: JobCreateRequest) -> dict:
    return {
        "name": payload.batch_name,
        "file": payload.main_file,
        "pyFiles": payload.python_egg_wheel_files,
        "files": payload.dependency_files,
        "conf": {
            "spark.pyspark.python": payload.spark_configuration.spark_pyspark_python,
            "spark.pyspark.driver.python": payload.spark_configuration.spark_pyspark_driver_python,
        },
        "args": [
            "--output-files-path",
            payload.job_arguments.output_files_path,
            "--checkpoints-hdfs-path",
            payload.job_arguments.checkpoints_hdfs_path,
            "--hive-output-schema",
            payload.job_arguments.hive_output_schema,
            "--log-path",
            payload.job_arguments.log_path,
            "--hive-prefix",
            payload.job_arguments.hive_prefix,
            "--interval",
            payload.job_arguments.interval,
            "--num-snapshots",
            payload.job_arguments.num_snapshots,
            "--spark-config",
            payload.job_arguments.spark_config,
        ],
    }


def build_generated_command(livy_payload: dict) -> str:
    import json

    pretty_json = json.dumps(livy_payload, indent=2)
    escaped_json = _escape_for_single_quoted_shell(pretty_json)
    return f"{chr(10).join(CURL_BASE)}-d '{escaped_json}'"


def build_job_record_data(payload: JobCreateRequest) -> dict:
    livy_payload = build_livy_payload(payload)
    generated_command = build_generated_command(livy_payload)

    return {
        "batch_name": payload.batch_name,
        "main_file": payload.main_file,
        "python_egg_wheel_files": payload.python_egg_wheel_files,
        "dependency_files": payload.dependency_files,
        "spark_conf": livy_payload["conf"],
        "command_arguments": {
            "output_files_path": payload.job_arguments.output_files_path,
            "checkpoints_hdfs_path": payload.job_arguments.checkpoints_hdfs_path,
            "hive_output_schema": payload.job_arguments.hive_output_schema,
            "log_path": payload.job_arguments.log_path,
            "hive_prefix": payload.job_arguments.hive_prefix,
            "interval": payload.job_arguments.interval,
            "num_snapshots": payload.job_arguments.num_snapshots,
            "spark_config": payload.job_arguments.spark_config,
        },
        "livy_payload": livy_payload,
        "generated_command": generated_command,
        "request_payload": payload.model_dump(by_alias=True),
        "output_files_path": payload.job_arguments.output_files_path,
        "checkpoints_hdfs_path": payload.job_arguments.checkpoints_hdfs_path,
        "hive_output_schema": payload.job_arguments.hive_output_schema,
        "log_path": payload.job_arguments.log_path,
        "hive_prefix": payload.job_arguments.hive_prefix,
        "interval": payload.job_arguments.interval,
        "num_snapshots": payload.job_arguments.num_snapshots,
        "spark_config": payload.job_arguments.spark_config,
    }


def build_public_job_id() -> str:
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"JOB-{date_part}-{uuid4().hex[:8].upper()}"
