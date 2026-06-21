# Supabase Setup

The MVP runs without Supabase by default. The FastAPI service uses in-memory mock repositories for products, appointments, conversations, knowledge, and support tickets so local demos and free deployments do not require paid services.

Use this guide when you are ready to provision the optional database schema already included in `supabase/migrations`.

## 1. Create a Supabase project

1. Create a free Supabase project.
2. Copy the project URL and anon/service-role keys from **Project Settings → API**.
3. Keep service-role keys server-side only; never expose them through `NEXT_PUBLIC_*` variables.

## 2. Environment variables

Add these values to `.env` or your deployment provider when a Supabase-backed repository is implemented:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
```

Current MVP variables that remain required are:

```bash
APP_ENV=production
LOG_LEVEL=INFO
LLM_PROVIDER=mock
API_CORS_ORIGINS=https://your-frontend.vercel.app
NEXT_PUBLIC_API_URL=https://your-api.onrender.com
```

## 3. Migrations

The schema lives in:

- `supabase/migrations/001_initial_schema.sql`
- `supabase/migrations/002_create_vector_index_after_backfill.sql`

Apply migrations with the Supabase SQL editor or the Supabase CLI:

```bash
supabase login
supabase link --project-ref <project-ref>
supabase db push
```

If applying manually, run `001_initial_schema.sql` first, backfill embeddings only when a future free/local embedding workflow exists, then run `002_create_vector_index_after_backfill.sql`.

## 4. Seed data

Seed data is stored in `supabase/seed.sql`.

With the CLI:

```bash
supabase db reset
```

For a hosted project, paste `supabase/seed.sql` into the SQL editor after migrations have completed.

## 5. MVP repository behavior

The current deployable MVP intentionally does **not** connect to Supabase at runtime. It keeps demo data in memory to avoid paid dependencies and to keep the frontend/backend integration deterministic. After database repositories are added, keep the existing API response envelopes unchanged so the frontend pages continue to work without contract changes.
