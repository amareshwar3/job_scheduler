"use client";

import { ReactNode, useEffect, useSyncExternalStore } from "react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";

export type Theme = "light" | "dark";

const STORAGE_KEY = "job-scheduler-theme";
const THEME_EVENT = "job-scheduler-theme-change";

const getSystemTheme = (): Theme =>
  window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";

const readTheme = (): Theme => {
  if (typeof window === "undefined") {
    return "light";
  }

  const storedTheme = window.localStorage.getItem(STORAGE_KEY);

  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return getSystemTheme();
};

const applyTheme = (theme: Theme) => {
  document.documentElement.classList.toggle("dark", theme === "dark");
  window.localStorage.setItem(STORAGE_KEY, theme);
  window.dispatchEvent(new Event(THEME_EVENT));
};

const subscribe = (callback: () => void) => {
  if (typeof window === "undefined") {
    return () => undefined;
  }

  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const handleChange = () => callback();

  window.addEventListener(THEME_EVENT, handleChange);
  mediaQuery.addEventListener("change", handleChange);

  return () => {
    window.removeEventListener(THEME_EVENT, handleChange);
    mediaQuery.removeEventListener("change", handleChange);
  };
};

export function ThemeProvider({ children }: { children: ReactNode }) {
  const theme = useSyncExternalStore<Theme>(
    subscribe,
    readTheme,
    () => "light",
  );

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const handleToggle = () => {
    applyTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <>
      <ThemeToggle theme={theme} onToggle={handleToggle} />
      {children}
    </>
  );
}
