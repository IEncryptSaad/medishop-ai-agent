# Deployment

## Overview

The MVP skeleton is deployment-ready for separate web and API services.

## Web

Build the Next.js app with:

```bash
pnpm --filter @medishop/web build
```

Deploy the generated Next.js application to a Node-compatible platform.

## API

Run the FastAPI app with an ASGI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Environment

Configure all variables listed in `.env.example` for each environment. Production deployments should use platform secret managers rather than committed `.env` files.
