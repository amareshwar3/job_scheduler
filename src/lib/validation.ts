import { JobFormErrors, JobFormValues } from "@/types/job-config";

const REQUIRED_MESSAGE = "This field is required.";

const getRequiredError = (value: string) =>
  value.trim() ? undefined : REQUIRED_MESSAGE;

export function validateJobForm(values: JobFormValues): JobFormErrors {
  return {
    batchName: getRequiredError(values.batchName),
    mainFile: getRequiredError(values.mainFile),
    sparkPysparkPython: getRequiredError(
      values.sparkConfiguration.sparkPysparkPython,
    ),
    sparkPysparkDriverPython: getRequiredError(
      values.sparkConfiguration.sparkPysparkDriverPython,
    ),
    outputFilesPath: getRequiredError(values.jobArguments.outputFilesPath),
    checkpointsHdfsPath: getRequiredError(
      values.jobArguments.checkpointsHdfsPath,
    ),
    hiveOutputSchema: getRequiredError(values.jobArguments.hiveOutputSchema),
    logPath: getRequiredError(values.jobArguments.logPath),
    hivePrefix: getRequiredError(values.jobArguments.hivePrefix),
    interval: getRequiredError(values.jobArguments.interval),
    numSnapshots: getRequiredError(values.jobArguments.numSnapshots),
    sparkConfig: getRequiredError(values.jobArguments.sparkConfig),
  };
}

export function isFormValid(errors: JobFormErrors) {
  return Object.values(errors).every((value) => !value);
}
