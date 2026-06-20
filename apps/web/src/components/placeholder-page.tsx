export function PlaceholderPage({ title, description }: Readonly<{ title: string; description: string }>) {
  return (
    <div className="rounded-2xl border bg-white p-8 shadow-sm">
      <p className="text-sm font-semibold uppercase tracking-wide text-brand-600">Foundation</p>
      <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-950">{title}</h1>
      <p className="mt-4 max-w-2xl text-slate-600">{description}</p>
    </div>
  );
}
