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

The backend exposes versioned API routes for health, mock product catalog search, in-memory appointment booking, support tickets, and a safe mock agent chat flow. Foundational cross-cutting concerns include configuration management, environment variable validation, structured logging, CORS, and application error handling.

## Tech Stack

- **Frontend:** Next.js 14, React, TypeScript, TailwindCSS, ESLint, Prettier
- **Backend:** Python 3.11, FastAPI, Pydantic Settings, Uvicorn, Ruff
- **Package management:** pnpm workspaces
- **CI/CD:** GitHub Actions

## Setup Instructions

1. Copy environment variables at the repository root:

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

   The API resolves configuration from the repository-root `.env` file, so the same local settings are used whether you start it from the repository root or from `apps/api`. `LLM_PROVIDER` defaults to `mock`, and local product, appointment, support, conversation, and knowledge data do not require a Supabase connection.

## Quality Checks

```bash
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app tests
cd apps/api && pytest
```

## Current Scope

Backend Batch 1 includes mock/local business logic for product discovery, appointment booking, support ticket creation, and safe agent responses. Shopify integrations, Supabase-backed repositories, real LLM providers, and production RAG pipelines remain future iterations.
