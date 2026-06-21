# MediShop AI Agent

A deployable MVP for a medical-store AI agent using the existing monorepo architecture: a Next.js operator dashboard, a FastAPI backend, shared TypeScript contracts, and mock/local repositories. The MVP does not call Shopify APIs, paid LLM providers, or paid services.

## Architecture

```text
apps/
  web/          Next.js 14 App Router frontend for dashboard, chat, products, appointments, and support
  api/          FastAPI backend with versioned routes, validation, structured errors, CORS, and logging
packages/
  shared/       Shared API types, DTOs, constants, and interfaces
  config/       Shared configuration helpers
docs/           Architecture, deployment, Supabase setup, demo, and development guides
supabase/       Optional schema, vector-index migration, and seed SQL for future database-backed repos
.github/        CI workflow for frontend build, backend tests, and smoke checks
```

### Runtime flow

1. The web app reads `NEXT_PUBLIC_API_URL` and calls `/api/v1/*` endpoints.
2. FastAPI returns a consistent success envelope with `success`, `data`, optional `message`, and `request_id`.
3. Validation and domain errors return a consistent error envelope with `success: false`, `error`, `message`, `details`, and `request_id`.
4. Product, appointment, support, knowledge, and conversation data use free in-memory repositories for the MVP.
5. The chat service uses deterministic mock logic and safety disclaimers instead of a paid LLM provider.

## Features

- Dashboard metrics and recent activity.
- Product catalog browse, search, category filtering, stock states, and product details.
- Agent chat with loading state, safe fallback text, sources, and product recommendations.
- Appointment listing and creation.
- Support ticket listing and creation.
- Backend health endpoint and smoke-tested API contracts.
- Render backend configuration and Vercel frontend configuration.
- Supabase setup documentation for future database-backed repositories.

## Local setup

### 1. Environment

```bash
cp .env.example .env
```

Key local values:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
API_CORS_ORIGINS=http://localhost:3000
LLM_PROVIDER=mock
```

### 2. Install frontend dependencies

```bash
pnpm install
```

### 3. Install backend dependencies

```bash
python3.11 -m venv apps/api/.venv
source apps/api/.venv/bin/activate
pip install -e "apps/api[dev]"
```

### 4. Run the API

```bash
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

### 5. Run the web app

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm --filter @medishop/web dev
```

Open `http://localhost:3000`.

## API endpoints

| Area | Method | Path |
| --- | --- | --- |
| Health | `GET` | `/api/v1/health` |
| Products | `GET` | `/api/v1/products` |
| Products | `POST` | `/api/v1/products/search` |
| Products | `GET` | `/api/v1/products/{product_id}` |
| Appointments | `GET` | `/api/v1/appointments` |
| Appointments | `POST` | `/api/v1/appointments` |
| Appointments | `GET` | `/api/v1/appointments/{appointment_id}` |
| Appointments | `PATCH` | `/api/v1/appointments/{appointment_id}` |
| Support | `GET` | `/api/v1/support/tickets` |
| Support | `POST` | `/api/v1/support/tickets` |
| Support | `GET` | `/api/v1/support/tickets/{ticket_id}` |
| Support | `PATCH` | `/api/v1/support/tickets/{ticket_id}` |
| Agent | `POST` | `/api/v1/agent/chat` |

## Environment variables

| Variable | Default | Used by | Description |
| --- | --- | --- | --- |
| `APP_ENV` | `development` | API | Runtime environment label. |
| `LOG_LEVEL` | `INFO` | API | Structured logging level. |
| `API_HOST` | `0.0.0.0` | API | Local API bind host. |
| `API_PORT` | `8000` | API | Local API bind port. Render uses `$PORT`. |
| `API_CORS_ORIGINS` | `http://localhost:3000` | API | Comma-separated allowed frontend origins. |
| `LLM_PROVIDER` | `mock` | API | Keep as `mock` for this MVP. |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Web | Browser-visible FastAPI base URL. |

Optional future Supabase variables are documented in `docs/supabase-setup.md`.

## Quality checks

```bash
pnpm --filter @medishop/web test
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app tests
cd apps/api && pytest -q
```

The backend test suite includes smoke coverage for health, products, product search, appointment creation/update, support ticket creation/update, and agent chat.

## Deployment

### Backend on Render

1. Push this repository to GitHub.
2. In Render, create a Blueprint from `render.yaml`.
3. Set `API_CORS_ORIGINS` to the deployed frontend URL, for example `https://your-app.vercel.app`.
4. Keep `LLM_PROVIDER=mock`.
5. Render runs:

```bash
pip install --upgrade pip && pip install -e ".[dev]"
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Confirm `https://your-api.onrender.com/api/v1/health` returns `status: ok`.

### Frontend on Vercel

1. Import the GitHub repository in Vercel.
2. Use `vercel.json` or configure manually:
   - Framework: Next.js
   - Install command: `pnpm install --frozen-lockfile`
   - Build command: `pnpm --filter @medishop/web build`
   - Output directory: `apps/web/.next`
3. Set `NEXT_PUBLIC_API_URL=https://your-api.onrender.com`.
4. Deploy and open `/dashboard`, `/chat`, `/products`, `/appointments`, and `/support`.

## Demo instructions

Use `docs/demo-script.md` for a guided demo. Recommended quick path:

1. Dashboard: show metrics and recent activity.
2. Products: search `moisturizer`, open details.
3. Chat: ask `Which moisturizer is good for sensitive skin?`.
4. Appointments: create a pharmacist consultation.
5. Support: create a damaged package ticket.
6. Dashboard: verify new activity.

## Supabase

The MVP is fully functional without Supabase. Optional setup, migrations, seed process, and environment variables are documented in `docs/supabase-setup.md`.

## Current limitations

- Data is in-memory and resets when the API process restarts.
- Chat is deterministic mock logic, not a paid or external LLM.
- Shopify APIs are intentionally not implemented.
- Supabase schema and seed files are prepared, but runtime repositories still use local mock data.
