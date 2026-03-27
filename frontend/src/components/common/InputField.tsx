interface InputFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
}

export function InputField({
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error,
}: InputFieldProps) {
  return (
    <label className="grid gap-2">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-[var(--page-foreground)]">
          {label}
        </span>
        {required ? (
          <span className="text-xs font-medium uppercase tracking-[0.14em] text-[var(--page-muted)]">
            Required
          </span>
        ) : null}
      </div>
      <div className="field-shell rounded-2xl px-4 py-3 transition">
        <input
          className="w-full bg-transparent text-sm text-[var(--page-foreground)] outline-none placeholder:text-[var(--page-muted)]"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
        />
      </div>
      {error ? (
        <p className="text-sm text-rose-500 dark:text-rose-300">{error}</p>
      ) : null}
    </label>
  );
}
