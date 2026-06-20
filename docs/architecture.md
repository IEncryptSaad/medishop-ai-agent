# Architecture

MediShop AI Agent is organized as a monorepo with clear application and package boundaries.

## Applications

- `apps/web`: Next.js 14 App Router frontend for dashboards, chat, appointments, and support workflows.
- `apps/api`: FastAPI backend with modular folders for APIs, services, agents, models, schemas, repositories, core concerns, and utilities.

## Packages

- `packages/shared`: Shared API response types, DTOs, constants, and interfaces for TypeScript consumers.
- `packages/config`: Shared environment templates, application settings, and logging constants.

## Cross-Cutting Standards

- Configuration is loaded from validated environment variables.
- Backend logs are emitted as structured JSON.
- Expected operational errors flow through a common application error type and handler.
- API routes are versioned under `/api/v1`.
