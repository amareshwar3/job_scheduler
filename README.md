# Job Scheduler Frontend

Production-ready frontend application for configuring Livy batch job inputs and generating the final cURL command on the client side.

## Overview

This project is built with:

- Next.js 16 App Router
- TypeScript
- React 19
- Tailwind CSS 4

Current scope:

- Frontend only
- No backend calls
- Real-time cURL generation
- Required field validation
- Dark and light theme toggle with `localStorage` persistence
- Modular component and utility structure for future database integration

## What The App Does

The UI collects:

1. Job Details
2. Spark Configuration
3. Job Arguments

It then generates this final output in real time:

- Fixed cURL headers and Livy endpoint
- `-d '<JSON>'` payload
- Pretty formatted JSON
- Shell-safe escaping for single quotes

The generated JSON follows this exact structure:

```json
{
  "name": "...",
  "file": "...",
  "pyFiles": ["..."],
  "files": ["..."],
  "conf": {
    "spark.pyspark.python": "...",
    "spark.pyspark.driver.python": "..."
  },
  "args": [
    "--output-files-path",
    "...",
    "--checkpoints-hdfs-path",
    "...",
    "--hive-output-schema",
    "...",
    "--log-path",
    "...",
    "--hive-prefix",
    "...",
    "--interval",
    "...",
    "--num-snapshots",
    "...",
    "--spark-config",
    "..."
  ]
}
```

## Features Implemented

- Responsive two-column layout
- Clearly separated sections for all form groups
- Exact field labels as requested
- Multi-input chip/tag UX for:
  - Python Egg/Wheel Files (HDFS)
  - Dependency Files
- Add and remove behavior for multi-value fields
- Reusable input components
- Reusable section wrapper
- Live cURL preview with copy button
- Required field validation
- Graceful handling of empty arrays
- Theme toggle with persisted preference
- Separated state, validation, and cURL generation logic

## Exact Commands Used To Create The App

These are the commands to recreate this frontend from scratch.

### 1. Scaffold the project

```bash
npx create-next-app@latest frontend --ts --tailwind --eslint --app --use-npm --src-dir --import-alias "@/*" --yes --disable-git
```

### 2. Move into the project

```bash
cd frontend
```

### 3. Start the development server

```bash
npm run dev
```

### 4. Verify linting

```bash
npm run lint
```

### 5. Verify production build

```bash
npm run build
```

## Packages Installed

No additional runtime packages were required beyond the official Next.js scaffold.

Installed by `create-next-app`:

- `next`
- `react`
- `react-dom`
- `typescript`
- `tailwindcss`
- `@tailwindcss/postcss`
- `eslint`
- `eslint-config-next`
- `@types/node`
- `@types/react`
- `@types/react-dom`

## Project Structure

```text
frontend/
├─ package.json
├─ package-lock.json
├─ tsconfig.json
├─ next.config.ts
├─ next-env.d.ts
├─ eslint.config.mjs
├─ postcss.config.mjs
├─ README.md
├─ public/
│  ├─ file.svg
│  ├─ globe.svg
│  ├─ next.svg
│  ├─ vercel.svg
│  └─ window.svg
└─ src/
   ├─ app/
   │  ├─ globals.css
   │  ├─ layout.tsx
   │  └─ page.tsx
   ├─ components/
   │  ├─ common/
   │  │  ├─ CurlPreview.tsx
   │  │  ├─ InputField.tsx
   │  │  ├─ MultiInputField.tsx
   │  │  └─ SectionWrapper.tsx
   │  ├─ job-scheduler/
   │  │  └─ JobSchedulerBuilder.tsx
   │  └─ theme/
   │     ├─ ThemeProvider.tsx
   │     └─ ThemeToggle.tsx
   ├─ hooks/
   │  └─ use-job-form.ts
   ├─ lib/
   │  ├─ curl-generator.ts
   │  └─ validation.ts
   └─ types/
      └─ job-config.ts
```

## Architecture

### UI Layer

- `src/components/common`
  - Shared reusable UI pieces
- `src/components/job-scheduler`
  - Main page-level feature composition
- `src/components/theme`
  - Theme state integration and toggle UI

### State Layer

- `src/hooks/use-job-form.ts`
  - Holds typed form state
  - Exposes update functions
  - Produces validation result
  - Produces generated cURL command

### Logic Layer

- `src/lib/validation.ts`
  - Required field validation rules
- `src/lib/curl-generator.ts`
  - Builds the JSON payload
  - Preserves required `args` order
  - Escapes JSON for shell-safe cURL output

### Type Layer

- `src/types/job-config.ts`
  - Centralized TypeScript interfaces
  - Initial form state
  - Error shape definitions

## Form Mapping

| Form Field | JSON Output |
| --- | --- |
| Batch Name | `name` |
| Main File (HDFS) | `file` |
| Python Egg/Wheel Files (HDFS) | `pyFiles` |
| Dependency Files | `files` |
| Spark Config fields | `conf` |
| Job Arguments | `args` |

## Theme Implementation

Theme support is implemented fully on the frontend:

- Light mode and dark mode toggle
- Preference stored in `localStorage`
- Theme class applied to the root HTML element
- System preference used as fallback when no saved theme exists

## Validation Rules

Required fields:

- Batch Name
- Main File (HDFS)
- `spark.pyspark.python`
- `spark.pyspark.driver.python`
- `--output-files-path`
- `--checkpoints-hdfs-path`
- `--hive-output-schema`
- `--log-path`
- `--hive-prefix`
- `--interval`
- `--num-snapshots`
- `--spark-config`

Arrays:

- `pyFiles` can be empty
- `files` can be empty

## How To Run

```bash
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Production Checks Completed

Verified successfully:

- `npm run lint`
- `npm run build`

## Future Extensibility

The app is intentionally structured so a backend can be added later without rewriting the UI:

- form model is typed
- payload generation is isolated
- validation is isolated
- UI components are reusable
- persistence can later be added through API actions or route handlers

## Notes

- Backend is intentionally not included
- No API integration is performed
- The Livy endpoint and headers are fixed as requested
- The generated output is preview-only for now
