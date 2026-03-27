"use client";

import { useDeferredValue } from "react";
import { CurlPreview } from "@/components/common/CurlPreview";
import { InputField } from "@/components/common/InputField";
import { MultiInputField } from "@/components/common/MultiInputField";
import { SectionWrapper } from "@/components/common/SectionWrapper";
import { useJobForm } from "@/hooks/use-job-form";

export function JobSchedulerBuilder() {
  const {
    values,
    errors,
    isValid,
    curlCommand,
    updateField,
    updateSparkConfiguration,
    updateJobArgument,
  } = useJobForm();

  const deferredCommand = useDeferredValue(curlCommand);

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-8 px-4 py-20 sm:px-6 lg:px-8">
      <section className="grid gap-6 lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)] lg:items-start">
        <div className="glass-panel rounded-[32px] p-8 sm:p-10">
          <div className="flex flex-col gap-4">
            <p className="text-xs font-semibold uppercase tracking-[0.32em] text-[var(--page-accent)]">
              Job Scheduler Frontend
            </p>
            <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-[var(--page-foreground)] sm:text-5xl">
              Configure a batch job and generate the exact Livy cURL command in
              real time.
            </h1>
            <p className="max-w-2xl text-base leading-7 text-[var(--page-muted)]">
              This frontend-only flow is ready for future persistence. Form
              state, validation, and command generation are all separated into
              reusable modules.
            </p>
          </div>
        </div>
        <CurlPreview command={deferredCommand} isValid={isValid} />
      </section>

      <div className="grid gap-8 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
        <div className="grid gap-8">
          <SectionWrapper
            title="1. JOB DETAILS"
            description="Capture the batch identity and file references."
          >
            <InputField
              label="Batch Name"
              value={values.batchName}
              onChange={(value) => updateField("batchName", value)}
              placeholder="Enter the Livy batch name"
              required
              error={errors.batchName}
            />
            <InputField
              label="Main File (HDFS)"
              value={values.mainFile}
              onChange={(value) => updateField("mainFile", value)}
              placeholder="hdfs:///path/to/main.py"
              required
              error={errors.mainFile}
            />
            <MultiInputField
              label="Python Egg/Wheel Files (HDFS)"
              values={values.pythonEggWheelFiles}
              onChange={(nextValues) =>
                updateField("pythonEggWheelFiles", nextValues)
              }
              placeholder="Add a .egg or .whl HDFS path"
            />
            <MultiInputField
              label="Dependency Files"
              values={values.dependencyFiles}
              onChange={(nextValues) => updateField("dependencyFiles", nextValues)}
              placeholder="Add a dependency file path"
            />
          </SectionWrapper>

          <SectionWrapper
            title="2. SPARK CONFIGURATION"
            description="Define the Python executables passed in the conf object."
          >
            <InputField
              label="spark.pyspark.python"
              value={values.sparkConfiguration.sparkPysparkPython}
              onChange={(value) =>
                updateSparkConfiguration("sparkPysparkPython", value)
              }
              placeholder="/usr/bin/python3"
              required
              error={errors.sparkPysparkPython}
            />
            <InputField
              label="spark.pyspark.driver.python"
              value={values.sparkConfiguration.sparkPysparkDriverPython}
              onChange={(value) =>
                updateSparkConfiguration("sparkPysparkDriverPython", value)
              }
              placeholder="/usr/bin/python3"
              required
              error={errors.sparkPysparkDriverPython}
            />
          </SectionWrapper>
        </div>

        <SectionWrapper
          title="3. JOB ARGUMENTS"
          description="Collect the required key-value arguments in the exact output order."
        >
          <InputField
            label="--output-files-path"
            value={values.jobArguments.outputFilesPath}
            onChange={(value) => updateJobArgument("outputFilesPath", value)}
            placeholder="hdfs:///path/to/output"
            required
            error={errors.outputFilesPath}
          />
          <InputField
            label="--checkpoints-hdfs-path"
            value={values.jobArguments.checkpointsHdfsPath}
            onChange={(value) => updateJobArgument("checkpointsHdfsPath", value)}
            placeholder="hdfs:///path/to/checkpoints"
            required
            error={errors.checkpointsHdfsPath}
          />
          <InputField
            label="--hive-output-schema"
            value={values.jobArguments.hiveOutputSchema}
            onChange={(value) => updateJobArgument("hiveOutputSchema", value)}
            placeholder="schema_name"
            required
            error={errors.hiveOutputSchema}
          />
          <InputField
            label="--log-path"
            value={values.jobArguments.logPath}
            onChange={(value) => updateJobArgument("logPath", value)}
            placeholder="hdfs:///path/to/logs"
            required
            error={errors.logPath}
          />
          <InputField
            label="--hive-prefix"
            value={values.jobArguments.hivePrefix}
            onChange={(value) => updateJobArgument("hivePrefix", value)}
            placeholder="table_prefix"
            required
            error={errors.hivePrefix}
          />
          <InputField
            label="--interval"
            value={values.jobArguments.interval}
            onChange={(value) => updateJobArgument("interval", value)}
            placeholder="7"
            required
            error={errors.interval}
          />
          <InputField
            label="--num-snapshots"
            value={values.jobArguments.numSnapshots}
            onChange={(value) => updateJobArgument("numSnapshots", value)}
            placeholder="10"
            required
            error={errors.numSnapshots}
          />
          <InputField
            label="--spark-config"
            value={values.jobArguments.sparkConfig}
            onChange={(value) => updateJobArgument("sparkConfig", value)}
            placeholder="driver-memory=4g"
            required
            error={errors.sparkConfig}
          />
        </SectionWrapper>
      </div>
    </main>
  );
}
