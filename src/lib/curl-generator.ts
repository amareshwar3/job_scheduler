import { JobFormValues, JobPayload } from "@/types/job-config";

const CURL_BASE = [
  "curl -k --negotiate -u : \\",
  '-H "Content-Type: application/json" \\',
  '-H "X-Requested-By: livy" \\',
  "-X POST https://gbl20167161.systems.uk.hsbc:28998/batches \\",
];

const trimArrayValues = (items: string[]) =>
  items.map((item) => item.trim()).filter(Boolean);

const escapeForSingleQuotedShell = (value: string) =>
  value.replace(/'/g, `'"'"'`);

export function buildJobPayload(values: JobFormValues): JobPayload {
  return {
    name: values.batchName.trim(),
    file: values.mainFile.trim(),
    pyFiles: trimArrayValues(values.pythonEggWheelFiles),
    files: trimArrayValues(values.dependencyFiles),
    conf: {
      "spark.pyspark.python": values.sparkConfiguration.sparkPysparkPython.trim(),
      "spark.pyspark.driver.python":
        values.sparkConfiguration.sparkPysparkDriverPython.trim(),
    },
    args: [
      "--output-files-path",
      values.jobArguments.outputFilesPath.trim(),
      "--checkpoints-hdfs-path",
      values.jobArguments.checkpointsHdfsPath.trim(),
      "--hive-output-schema",
      values.jobArguments.hiveOutputSchema.trim(),
      "--log-path",
      values.jobArguments.logPath.trim(),
      "--hive-prefix",
      values.jobArguments.hivePrefix.trim(),
      "--interval",
      values.jobArguments.interval.trim(),
      "--num-snapshots",
      values.jobArguments.numSnapshots.trim(),
      "--spark-config",
      values.jobArguments.sparkConfig.trim(),
    ],
  };
}

export function generateCurlCommand(values: JobFormValues) {
  const payload = buildJobPayload(values);
  const prettyJson = JSON.stringify(payload, null, 2);
  const escapedJson = escapeForSingleQuotedShell(prettyJson);

  return `${CURL_BASE.join("\n")}-d '${escapedJson}'`;
}
