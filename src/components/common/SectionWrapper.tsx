import { ReactNode } from "react";

interface SectionWrapperProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function SectionWrapper({
  title,
  description,
  children,
}: SectionWrapperProps) {
  return (
    <section className="glass-panel rounded-[28px] p-6 sm:p-8">
      <div className="mb-6 flex flex-col gap-2 border-b border-[var(--page-border)] pb-5">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--page-accent)]">
          {title}
        </p>
        <h2 className="text-2xl font-semibold tracking-tight text-[var(--page-foreground)]">
          {description}
        </h2>
      </div>
      <div className="grid gap-5">{children}</div>
    </section>
  );
}
