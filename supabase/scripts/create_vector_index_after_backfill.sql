-- Create the knowledge chunk vector index after embedding backfill.
--
-- Run this manual script only after knowledge_chunks.embedding has been populated.
-- HNSW does not require training on existing rows and is preferred when the
-- installed pgvector version supports it. Older pgvector versions may not expose
-- the hnsw index access method, so IVFFlat is used as a documented fallback.
do $$
begin
  if not exists (
    select 1
    from public.knowledge_chunks
    where embedding is not null
  ) then
    raise exception 'Create embeddings in public.knowledge_chunks before running this vector index script.';
  end if;

  if exists (select 1 from pg_catalog.pg_am where amname = 'hnsw') then
    execute 'create index if not exists ix_knowledge_chunks_embedding on public.knowledge_chunks using hnsw (embedding vector_cosine_ops)';
  else
    execute 'create index if not exists ix_knowledge_chunks_embedding on public.knowledge_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100)';
  end if;
end;
$$;
