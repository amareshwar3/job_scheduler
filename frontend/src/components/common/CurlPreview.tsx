"use client";

import { useState } from "react";

interface CurlPreviewProps {
  command: string;
  isValid: boolean;
}

export function CurlPreview({ command, isValid }: CurlPreviewProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(command);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <section className="glass-panel rounded-[28px] p-6 sm:p-8">
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--page-accent)]">
            cURL Preview
          </p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight">
            Live command output
          </h2>
        </div>
        <button
          type="button"
          onClick={handleCopy}
          className="rounded-2xl border border-[var(--page-border)] bg-[var(--page-surface-strong)] px-4 py-3 text-sm font-semibold text-[var(--page-foreground)] transition hover:border-[var(--page-accent)] hover:text-[var(--page-accent)]"
        >
          {copied ? "Copied" : "Copy command"}
        </button>
      </div>
      <div className="mb-4 rounded-2xl border border-[var(--page-border)] bg-slate-950/95 p-4">
        <pre className="overflow-x-auto whitespace-pre-wrap break-words font-mono text-sm leading-7 text-slate-100">
          {command}
        </pre>
      </div>
      <p
        className={`text-sm ${
          isValid
            ? "text-emerald-600 dark:text-emerald-300"
            : "text-amber-700 dark:text-amber-300"
        }`}
      >
        {isValid
          ? "All required fields are populated."
          : "Preview updates in real time, but required fields still need values."}
      </p>
    </section>
  );
}
