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


### Backend dependency compatibility

The backend pins the FastAPI/Starlette/httpx test stack to compatible, production-safe versions:

- FastAPI `0.115.14`
- Starlette `0.46.2`
- httpx `0.28.1`
- pytest `8.4.2`

Keep these versions in sync when upgrading. Starlette's `TestClient` uses httpx internally, so unbounded upgrades can break pytest collection before any tests run.

## Checks

```bash
pnpm --filter @medishop/web lint
pnpm --filter @medishop/web build
cd apps/api && ruff check app
```
