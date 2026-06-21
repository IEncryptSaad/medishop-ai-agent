# Deployment

## Overview

The MVP skeleton is deployment-ready for separate web and API services.

## Web

`vercel.json` is intentionally limited to safe build/static configuration. Do not commit `NEXT_PUBLIC_API_URL` or placeholder production API URLs there. For Vercel deployments, configure `NEXT_PUBLIC_API_URL` in Vercel Project Settings and set it to the deployed Render backend URL. The local development default can remain `http://localhost:8000`.

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

Configure all variables listed in `.env.example` for each environment. Production deployments should use platform secret managers rather than committed `.env` files. In particular, set `NEXT_PUBLIC_API_URL` in Vercel Project Settings to the deployed Render backend URL; keep the local default as `http://localhost:8000`.
