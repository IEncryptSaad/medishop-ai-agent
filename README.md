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

4. Run the API:

   ```bash
   cd apps/api
   uvicorn app.main:app --reload
   ```

   The backend runs at `http://localhost:8000` by default and exposes `/api/v1/health`, `/api/v1/products`, `/api/v1/products/search`, `/api/v1/appointments`, `/api/v1/support/tickets`, and `/api/v1/agent/chat`. The API resolves configuration from the repository-root `.env` file, so the same local settings are used whether you start it from the repository root or from `apps/api`. `LLM_PROVIDER` defaults to `mock`, and local product, appointment, support, conversation, and knowledge data do not require a Supabase connection.

5. Run the web app in another terminal:

   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm --filter @medishop/web dev
   ```

   `NEXT_PUBLIC_API_URL` is optional in local development because the frontend defaults to `http://localhost:8000`. If the backend cannot be reached, the demo UI falls back to local mock catalog, appointment, support, and chat data so the MVP remains demo-ready without paid services. Validation and API errors from the backend are displayed as user-friendly messages in the UI.

## Environment Variables

| Variable              | Default                 | Used by  | Description                                        |
| --------------------- | ----------------------- | -------- | -------------------------------------------------- |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Frontend | Base URL for the FastAPI backend.                  |
| `API_CORS_ORIGINS`    | `http://localhost:3000` | Backend  | Comma-separated frontend origins allowed by CORS.  |
| `API_HOST`            | `0.0.0.0`               | Backend  | API bind host.                                     |
| `API_PORT`            | `8000`                  | Backend  | API bind port.                                     |
| `LLM_PROVIDER`        | `mock`                  | Backend  | Keeps local chat responses free and deterministic. |

## Local Full-Stack Test Steps

1. Start the backend with `cd apps/api && uvicorn app.main:app --reload`.
2. Verify health with `curl http://localhost:8000/api/v1/health`.
3. Start the frontend with `NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm --filter @medishop/web dev`.
4. Open `http://localhost:3000/products` and search for `moisturizer`.
5. Open `http://localhost:3000/chat` and ask a product question such as `Which moisturizer is good for sensitive skin?`.
6. Open `http://localhost:3000/appointments` and create a booking.
7. Open `http://localhost:3000/support` and create a ticket.
8. Open `http://localhost:3000/dashboard` and confirm products, appointments, and tickets are loaded from the API.

## Quality Checks

```bash
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app tests
cd apps/api && pytest
```

## Frontend MVP

The Next.js app includes demo-ready routes for `/`, `/chat`, `/products`, `/appointments`, `/support`, and `/dashboard`. The UI provides a responsive healthcare SaaS shell, reusable cards and badges, product search and detail views, safe chat with source and recommendation cards, booking and ticket forms, loading/empty/error-friendly states, and dashboard metrics.

## Current Scope

Backend Batch 1 includes mock/local business logic for product discovery, appointment booking, support ticket creation, and safe agent responses. Shopify integrations, Supabase-backed repositories, real LLM providers, and production RAG pipelines remain future iterations.
