export type JobArgumentKey =
  | "--output-files-path"
  | "--checkpoints-hdfs-path"
  | "--hive-output-schema"
  | "--log-path"
  | "--hive-prefix"
  | "--interval"
  | "--num-snapshots"
  | "--spark-config";

export interface JobArguments {
  outputFilesPath: string;
  checkpointsHdfsPath: string;
  hiveOutputSchema: string;
  logPath: string;
  hivePrefix: string;
  interval: string;
  numSnapshots: string;
  sparkConfig: string;
}

export interface SparkConfiguration {
  sparkPysparkPython: string;
  sparkPysparkDriverPython: string;
}

export interface JobFormValues {
  batchName: string;
  mainFile: string;
  pythonEggWheelFiles: string[];
  dependencyFiles: string[];
  sparkConfiguration: SparkConfiguration;
  jobArguments: JobArguments;
}

export interface JobPayload {
  name: string;
  file: string;
  pyFiles: string[];
  files: string[];
  conf: {
    "spark.pyspark.python": string;
    "spark.pyspark.driver.python": string;
  };
  args: string[];
}

export type JobFormErrors = Partial<
  Record<
    | "batchName"
    | "mainFile"
    | "sparkPysparkPython"
    | "sparkPysparkDriverPython"
    | "outputFilesPath"
    | "checkpointsHdfsPath"
    | "hiveOutputSchema"
    | "logPath"
    | "hivePrefix"
    | "interval"
    | "numSnapshots"
    | "sparkConfig",
    string
  >
>;

export const INITIAL_JOB_FORM_VALUES: JobFormValues = {
  batchName: "",
  mainFile: "",
  pythonEggWheelFiles: [],
  dependencyFiles: [],
  sparkConfiguration: {
    sparkPysparkPython: "",
    sparkPysparkDriverPython: "",
  },
  jobArguments: {
    outputFilesPath: "",
    checkpointsHdfsPath: "",
    hiveOutputSchema: "",
    logPath: "",
    hivePrefix: "",
    interval: "",
    numSnapshots: "",
    sparkConfig: "",
  },
};
