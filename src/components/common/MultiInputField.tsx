"use client";

import { KeyboardEvent, useState } from "react";

interface MultiInputFieldProps {
  label: string;
  values: string[];
  onChange: (values: string[]) => void;
  placeholder?: string;
}

export function MultiInputField({
  label,
  values,
  onChange,
  placeholder,
}: MultiInputFieldProps) {
  const [draft, setDraft] = useState("");

  const addValue = () => {
    const nextValue = draft.trim();

    if (!nextValue) {
      return;
    }

    onChange([...values, nextValue]);
    setDraft("");
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key !== "Enter") {
      return;
    }

    event.preventDefault();
    addValue();
  };

  const removeValue = (index: number) => {
    onChange(values.filter((_, currentIndex) => currentIndex !== index));
  };

  return (
    <div className="grid gap-3">
      <span className="text-sm font-medium text-[var(--page-foreground)]">
        {label}
      </span>
      <div className="grid gap-3 rounded-[24px] border border-[var(--page-border)] bg-[var(--page-surface-strong)] p-4">
        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="field-shell flex-1 rounded-2xl px-4 py-3 transition">
            <input
              className="w-full bg-transparent text-sm text-[var(--page-foreground)] outline-none placeholder:text-[var(--page-muted)]"
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
            />
          </div>
          <button
            type="button"
            onClick={addValue}
            className="rounded-2xl bg-[var(--page-accent)] px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-[var(--page-accent-strong)]"
          >
            Add entry
          </button>
        </div>
        <div className="flex min-h-14 flex-wrap gap-2">
          {values.length ? (
            values.map((value, index) => (
              <span
                key={`${value}-${index}`}
                className="inline-flex items-center gap-2 rounded-full border border-[var(--page-border)] bg-[var(--page-accent-soft)] px-3 py-2 text-sm text-[var(--page-foreground)]"
              >
                <span className="max-w-[18rem] truncate">{value}</span>
                <button
                  type="button"
                  onClick={() => removeValue(index)}
                  className="rounded-full px-1 text-[var(--page-muted)] transition hover:text-[var(--page-foreground)]"
                  aria-label={`Remove ${value}`}
                >
                  x
                </button>
              </span>
            ))
          ) : (
            <p className="text-sm text-[var(--page-muted)]">
              No entries added yet.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
