"use client";

import { useMemo, useState } from "react";
import {
  INITIAL_JOB_FORM_VALUES,
  JobFormErrors,
  JobFormValues,
} from "@/types/job-config";
import { generateCurlCommand } from "@/lib/curl-generator";
import { isFormValid, validateJobForm } from "@/lib/validation";

export function useJobForm() {
  const [values, setValues] = useState<JobFormValues>(INITIAL_JOB_FORM_VALUES);

  const errors = useMemo<JobFormErrors>(() => validateJobForm(values), [values]);
  const isValid = useMemo(() => isFormValid(errors), [errors]);
  const curlCommand = useMemo(() => generateCurlCommand(values), [values]);

  const updateField = (field: keyof JobFormValues, value: string | string[]) => {
    setValues((current) => ({
      ...current,
      [field]: value,
    }));
  };

  const updateSparkConfiguration = (
    field: keyof JobFormValues["sparkConfiguration"],
    value: string,
  ) => {
    setValues((current) => ({
      ...current,
      sparkConfiguration: {
        ...current.sparkConfiguration,
        [field]: value,
      },
    }));
  };

  const updateJobArgument = (
    field: keyof JobFormValues["jobArguments"],
    value: string,
  ) => {
    setValues((current) => ({
      ...current,
      jobArguments: {
        ...current.jobArguments,
        [field]: value,
      },
    }));
  };

  return {
    values,
    errors,
    isValid,
    curlCommand,
    updateField,
    updateSparkConfiguration,
    updateJobArgument,
  };
}
