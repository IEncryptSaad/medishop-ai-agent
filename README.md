# MediShop AI Agent

Production-grade AI Agent MVP foundation for Shopify medical stores. The monorepo is prepared for a Next.js operator dashboard, a FastAPI service layer, shared TypeScript contracts, and reusable configuration assets.

## Architecture

```text
apps/
  web/          Next.js 14 App Router frontend
  api/          FastAPI backend service
packages/
  shared/       Shared API types, DTOs, constants, and interfaces
  config/       Environment templates, app settings, and logging config
docs/           Architecture, deployment, and development guides
.github/        CI workflows
```

The initial backend exposes a versioned API router with a health endpoint and foundational cross-cutting concerns: configuration management, environment variable validation, structured logging, CORS, and application error handling.

## Tech Stack

- **Frontend:** Next.js 14, React, TypeScript, TailwindCSS, ESLint, Prettier
- **Backend:** Python 3.11, FastAPI, Pydantic Settings, Uvicorn, Ruff
- **Package management:** pnpm workspaces
- **CI/CD:** GitHub Actions

## Setup Instructions

1. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

2. Install frontend dependencies:

   ```bash
   pnpm install
   ```

3. Install backend dependencies:

   ```bash
   cd apps/api
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

4. Run the web app:

   ```bash
   pnpm --filter @medishop/web dev
   ```

5. Run the API:

   ```bash
   cd apps/api
   uvicorn app.main:app --reload
   ```

## Quality Checks

```bash
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app
```

## Current Scope

This repository intentionally contains only the production-grade skeleton and foundational files. Business logic, Shopify integrations, AI agent workflows, RAG pipelines, appointment booking, and support automation will be implemented in later iterations.
