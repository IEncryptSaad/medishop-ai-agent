"use client";
import { FormEvent, useEffect, useState } from "react";
import { ApiError, api, SupportTicket } from "@/lib/api";
import { Badge, Card, EmptyState } from "@/components/ui/card";

const priorityTone = (p: string) =>
  p === "high" ? "red" : p === "low" ? "slate" : "amber";
const statusTone = (s: string) =>
  s === "resolved" ? "green" : s === "triage" ? "purple" : "blue";

export function SupportPanel() {
  const [items, setItems] = useState<SupportTicket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listTickets()
      .then(setItems)
      .catch((err) =>
        setError(
          err instanceof ApiError
            ? err.userMessage
            : "Support tickets could not be loaded.",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const fd = new FormData(form);
    setError(null);
    try {
      const item = await api.createTicket({
        subject: String(fd.get("subject")),
        description: String(fd.get("description")),
        priority: String(fd.get("priority")),
        category: String(fd.get("category")),
      });
      setItems((current) => [item, ...current]);
      form.reset();
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.userMessage
          : "Support ticket could not be created.",
      );
    }
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}
      <div className="grid gap-6 lg:grid-cols-[420px_1fr]">
        <Card>
          <h2 className="text-xl font-bold">Open support ticket</h2>
          <form onSubmit={submit} className="mt-5 space-y-4">
            <input
              name="subject"
              required
              className="w-full rounded-2xl border px-4 py-3"
              placeholder="Subject"
            />
            <select
              name="priority"
              className="w-full rounded-2xl border px-4 py-3"
            >
              <option>normal</option>
              <option>high</option>
              <option>low</option>
            </select>
            <input
              name="category"
              className="w-full rounded-2xl border px-4 py-3"
              placeholder="Category"
            />
            <textarea
              name="description"
              required
              className="min-h-28 w-full rounded-2xl border px-4 py-3"
              placeholder="Describe the issue"
            />
            <button className="w-full rounded-2xl bg-brand-600 px-5 py-3 font-semibold text-white">
              Create ticket
            </button>
          </form>
        </Card>
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Tickets</h2>
          {loading ? (
            <EmptyState
              title="Loading tickets"
              description="Fetching support queue."
            />
          ) : items.length === 0 ? (
            <EmptyState
              title="No tickets"
              description="Create a support ticket to get started."
            />
          ) : (
            items.map((t) => (
              <Card key={t.id}>
                <div className="flex flex-col gap-3 md:flex-row md:justify-between">
                  <div>
                    <h3 className="font-bold">{t.subject}</h3>
                    <p className="mt-1 text-sm text-slate-600">
                      {t.description}
                    </p>
                    <p className="mt-2 text-xs text-slate-500">{t.category}</p>
                  </div>
                  <div className="flex gap-2">
                    <Badge tone={priorityTone(t.priority)}>{t.priority}</Badge>
                    <Badge tone={statusTone(t.status)}>{t.status}</Badge>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
