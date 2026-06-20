# MediShop AI Agent database schema

This database foundation targets Supabase PostgreSQL and keeps the first version simple while leaving room for Shopify synchronization, retrieval-augmented generation (RAG), customer support automation, and appointment scheduling.

## Design principles

- **UUID primary keys:** every table uses UUIDs so records can be created safely across services and synced systems.
- **Audit timestamps:** all tables include `created_at` and `updated_at`; the migration adds a trigger to maintain `updated_at`.
- **Extensible metadata:** integration-specific or workflow-specific fields live in JSONB columns such as `metadata_json` and `attributes` instead of forcing frequent migrations.
- **Clear status columns:** operational tables include status fields for queues, automations, and staff workflows.
- **RAG-ready knowledge base:** `knowledge_chunks` includes a `vector(1536)` embedding column powered by `pgvector` and an IVFFlat cosine index.

## Core entities

### Users

`users` stores customers, staff, and administrators. `external_customer_id` is reserved for Shopify or CRM customer IDs, while `metadata_json` can store preferences and consent flags.

### Product catalog

`product_categories` supports a parent-child hierarchy. `products` stores SKU, price, inventory, catalog status, optional `shopify_product_id`, and flexible `attributes` for product details such as brand, sizing, eligibility, tags, and synced platform payload fragments.

### Knowledge base and RAG

`knowledge_documents` represents source material such as FAQs, return policies, support macros, uploaded files, or product guides. `knowledge_chunks` stores searchable text chunks, token counts, metadata, and future embeddings. The schema supports semantic search with `pgvector` without requiring a paid vector database.

### Appointments

`appointments` links optional users to scheduled service windows. `appointment_type` is intentionally string-based to allow early iteration over pharmacist consultations, product setup calls, order support, and other services before introducing a dedicated appointment-type table.

### Support automation

`support_tickets` tracks customer issues with status, priority, and category fields. This is the main handoff object for support automation and staff escalation.

### Conversations and messages

`conversations` groups chat, email, SMS, or Shopify-chat interactions. `messages` stores the customer, assistant, staff, or system turns. Messages are indexed by conversation and creation time for fast transcript loading.

### Agent runs

`agent_runs` records automation executions such as RAG answers, ticket triage, appointment scheduling, and product recommendation flows. Input and output payloads are JSONB so prompts, retrieved sources, tool decisions, and model outputs can be audited and improved.

## Relationship overview

- A `product_category` can have many `products`.
- A `knowledge_document` can have many `knowledge_chunks`.
- A `user` can have many `appointments`, `support_tickets`, and `conversations`.
- A `support_ticket` can be linked to conversations and agent runs.
- A `conversation` can have many `messages` and many `agent_runs`.

## Indexing strategy

The migration creates indexes for common lookup and workflow paths:

- customer lookup by email and external platform customer ID;
- product lookup by SKU, category, name, and status;
- document filtering by source type and status;
- chunk retrieval by document and vector similarity;
- appointment filtering by status and start time;
- ticket filtering by status, priority, category, and user;
- conversation/message transcript loading;
- agent run filtering by status and linked conversation.

## Supabase notes

The migration enables only PostgreSQL extensions available in Supabase: `pgcrypto` for UUID generation and `vector` for pgvector embeddings. It does not require any paid external services. Row-level security policies are intentionally not defined yet because API routes and authentication behavior have not been implemented.
