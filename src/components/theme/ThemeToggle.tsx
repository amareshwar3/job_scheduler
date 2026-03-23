"use client";

import { Theme } from "@/components/theme/ThemeProvider";

interface ThemeToggleProps {
  theme: Theme;
  onToggle: () => void;
}

export function ThemeToggle({ theme, onToggle }: ThemeToggleProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className="fixed top-5 right-5 z-50 rounded-full border border-[var(--page-border)] bg-[var(--page-surface-strong)] px-4 py-2 text-sm font-semibold text-[var(--page-foreground)] shadow-lg backdrop-blur transition hover:border-[var(--page-accent)] hover:text-[var(--page-accent)]"
      aria-label="Toggle theme"
      suppressHydrationWarning
    >
      {theme === "dark" ? "Light mode" : "Dark mode"}
    </button>
  );
}
