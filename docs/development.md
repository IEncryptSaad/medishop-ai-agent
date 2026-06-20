# Development

## Prerequisites

- Node.js 20+
- pnpm 9+
- Python 3.11+

## Local Environment

Copy the repository-root `.env.example` to a repository-root `.env` and update values for your local environment. The API resolves this root `.env` from its config module path, so local settings are consistent whether commands are run from the repository root or from `apps/api`.

## Frontend

```bash
pnpm install
pnpm --filter @medishop/web dev
```

## Backend

```bash
cd apps/api
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Checks

```bash
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app
```
