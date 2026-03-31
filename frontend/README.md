# Job Scheduler Frontend

Frontend for creating Livy batch job payloads and generating a ready-to-run cURL command.

## Stack

- Next.js 16 (App Router)
- React 19
- TypeScript 5
- Tailwind CSS 4
- ESLint 9 + `eslint-config-next`

## Prerequisites

- Node.js 20.9.0 or newer
- npm 10 or newer

Check versions:

```bash
node -v
npm -v
```

## Run Existing Frontend

From the `frontend` folder:

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Frontend Scripts

- `npm run dev`: Start local dev server
- `npm run build`: Create production build
- `npm run start`: Run production server
- `npm run lint`: Run ESLint
- `npm run lint:fix`: Auto-fix lint issues
- `npm run typecheck`: TypeScript check without emit

## Create This Frontend From Scratch

Use these commands to scaffold a clean frontend and configure it like this project.

### 1) Scaffold

```bash
npx create-next-app@latest frontend --yes
```

This uses Next defaults (TypeScript, ESLint, Tailwind, App Router, src dir, alias `@/*`).

### 2) Enter project

```bash
cd frontend
```

### 3) Install/align dependencies

```bash
npm install next@^16.2.1 react@^19.2.4 react-dom@^19.2.4
npm install -D typescript@^5 eslint@^9 eslint-config-next@16.2.1 @types/node@^20 @types/react@^19 @types/react-dom@^19 tailwindcss@^4 @tailwindcss/postcss@^4
```

### 4) Set package scripts and engines

Use this `package.json` shape:

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "engines": {
    "node": ">=20.9.0"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "typecheck": "tsc --noEmit"
  }
}
```

### 5) Use stable Next config baseline

`next.config.ts`

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {};

export default nextConfig;
```

### 6) Use ESLint flat config

`eslint.config.mjs`

```js
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);

export default eslintConfig;
```

### 7) Validate

```bash
npm run lint
npm run typecheck
npm run build
```

## Common Troubleshooting

If you hit Next/React/TypeScript issues after upgrades:

1. Remove old artifacts:

```bash
rm -rf node_modules .next package-lock.json
```

PowerShell equivalent:

```powershell
Remove-Item -Recurse -Force node_modules, .next
Remove-Item -Force package-lock.json
```

2. Reinstall clean:

```bash
npm install
```

3. Re-run checks:

```bash
npm run lint
npm run typecheck
npm run build
```

## Project Structure

```text
frontend/
├─ package.json
├─ package-lock.json
├─ tsconfig.json
├─ next.config.ts
├─ eslint.config.mjs
├─ postcss.config.mjs
├─ src/
│  ├─ app/
│  ├─ components/
│  ├─ hooks/
│  ├─ lib/
│  └─ types/
└─ public/
```
