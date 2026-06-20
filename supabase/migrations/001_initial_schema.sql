-- MediShop AI Agent initial Supabase PostgreSQL schema.
-- Enables UUID generation and pgvector for future RAG similarity search.
create extension if not exists "pgcrypto";
create extension if not exists "vector";

-- Keeps updated_at current without application-side timestamp plumbing.
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table public.users (
  id uuid primary key default gen_random_uuid(),
  email varchar(320) not null unique,
  full_name varchar(200),
  phone varchar(40),
  role varchar(40) not null default 'customer', -- customer, staff, admin
  external_customer_id varchar(120), -- Shopify/customer-platform sync key
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.product_categories (
  id uuid primary key default gen_random_uuid(),
  name varchar(160) not null unique,
  slug varchar(180) not null unique,
  description text,
  parent_id uuid references public.product_categories(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.products (
  id uuid primary key default gen_random_uuid(),
  category_id uuid references public.product_categories(id) on delete set null,
  sku varchar(120) not null unique,
  name varchar(240) not null,
  description text,
  price numeric(12,2) not null check (price >= 0),
  currency char(3) not null default 'USD',
  stock_quantity integer not null default 0 check (stock_quantity >= 0),
  status varchar(40) not null default 'active', -- active, draft, archived, out_of_stock
  shopify_product_id varchar(120) unique,
  attributes jsonb not null default '{}'::jsonb, -- dosage, brand, tags, Shopify payload fragments
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.knowledge_documents (
  id uuid primary key default gen_random_uuid(),
  title varchar(240) not null,
  source_type varchar(60) not null, -- faq, product_guide, policy, support_macro, uploaded_file
  source_uri text,
  status varchar(40) not null default 'draft', -- draft, indexed, archived
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.knowledge_chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.knowledge_documents(id) on delete cascade,
  chunk_index integer not null,
  content text not null,
  token_count integer,
  embedding vector(1536), -- pgvector embedding for semantic retrieval
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (document_id, chunk_index)
);

create table public.appointments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  appointment_type varchar(120) not null, -- pharmacist_consult, product_demo, order_help
  scheduled_start timestamptz not null,
  scheduled_end timestamptz not null,
  status varchar(40) not null default 'scheduled', -- requested, scheduled, completed, cancelled, no_show
  notes text,
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (scheduled_end > scheduled_start)
);

create table public.support_tickets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  subject varchar(240) not null,
  description text not null,
  status varchar(40) not null default 'open', -- open, pending_customer, escalated, resolved, closed
  priority varchar(40) not null default 'normal', -- low, normal, high, urgent
  category varchar(100), -- shipping, return, product_question, appointment, technical
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.conversations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  support_ticket_id uuid references public.support_tickets(id) on delete set null,
  channel varchar(60) not null default 'web', -- web, email, sms, shopify_chat
  status varchar(40) not null default 'active', -- active, waiting, closed, escalated
  summary text,
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.conversations(id) on delete cascade,
  sender_type varchar(40) not null, -- customer, assistant, staff, system
  content text not null,
  metadata_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.agent_runs (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid references public.conversations(id) on delete set null,
  support_ticket_id uuid references public.support_tickets(id) on delete set null,
  run_type varchar(80) not null, -- rag_answer, ticket_triage, appointment_scheduler, product_recommender
  status varchar(40) not null default 'queued', -- queued, running, succeeded, failed, cancelled
  model_name varchar(120),
  input_payload jsonb not null default '{}'::jsonb,
  output_payload jsonb not null default '{}'::jsonb,
  error_message text,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Lookup and filtering indexes for application workflows.
create index ix_users_email on public.users(email);
create index ix_users_external_customer_id on public.users(external_customer_id);
create index ix_product_categories_slug on public.product_categories(slug);
create index ix_products_category_id on public.products(category_id);
create index ix_products_status on public.products(status);
create index ix_products_name on public.products(name);
create index ix_knowledge_documents_status on public.knowledge_documents(status);
create index ix_knowledge_documents_source_type on public.knowledge_documents(source_type);
create index ix_knowledge_chunks_document_position on public.knowledge_chunks(document_id, chunk_index);
create index ix_appointments_user_id on public.appointments(user_id);
create index ix_appointments_status_start on public.appointments(status, scheduled_start);
create index ix_support_tickets_status_priority on public.support_tickets(status, priority);
create index ix_support_tickets_user_id on public.support_tickets(user_id);
create index ix_conversations_user_id on public.conversations(user_id);
create index ix_conversations_ticket_id on public.conversations(support_ticket_id);
create index ix_conversations_status on public.conversations(status);
create index ix_messages_conversation_created on public.messages(conversation_id, created_at);
create index ix_agent_runs_status on public.agent_runs(status);
create index ix_agent_runs_conversation_id on public.agent_runs(conversation_id);

-- Attach updated_at trigger to every mutable table.
do $$
declare
  table_name text;
begin
  foreach table_name in array array[
    'users', 'product_categories', 'products', 'knowledge_documents', 'knowledge_chunks',
    'appointments', 'support_tickets', 'conversations', 'messages', 'agent_runs'
  ] loop
    execute format('create trigger set_%I_updated_at before update on public.%I for each row execute function public.set_updated_at()', table_name, table_name);
  end loop;
end;
$$;
