"use client";
import { FormEvent, useMemo, useState } from "react";
import { ApiError, api, ChatMessage } from "@/lib/api";
import { Badge, Card } from "@/components/ui/card";

export function ChatConsole() {
  const sessionId = useMemo(() => `web-${Date.now()}`, []);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hi, I’m the MediShop demo assistant. Ask about products, appointments, or support workflows.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    const text = input.trim();
    setInput("");
    setMessages((m) => [
      ...m,
      { id: crypto.randomUUID(), role: "user", content: text },
    ]);
    setLoading(true);
    try {
      const res = await api.sendChat(sessionId, text);
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: res.response,
          sources: res.sources,
          recommendations: res.recommendations,
        },
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            err instanceof ApiError
              ? err.userMessage
              : "I could not reach the assistant service. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }
  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
      <Card className="flex min-h-[620px] flex-col">
        <div className="flex-1 space-y-4 overflow-y-auto pr-1">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`max-w-[85%] rounded-3xl px-5 py-4 ${m.role === "user" ? "ml-auto bg-brand-600 text-white" : "bg-slate-100 text-slate-800"}`}
            >
              <p className="whitespace-pre-wrap text-sm leading-6">
                {m.content}
              </p>
              {m.sources?.length ? (
                <div className="mt-4 grid gap-2">
                  {m.sources.map((s) => (
                    <div
                      key={s.title}
                      className="rounded-2xl bg-white p-3 text-xs text-slate-600"
                    >
                      <b>{s.title}</b>
                      <br />
                      {s.source_type}
                      {s.score ? ` · ${(s.score * 100).toFixed(0)}% match` : ""}
                    </div>
                  ))}
                </div>
              ) : null}
            </div>
          ))}
          {loading && (
            <div className="w-fit rounded-3xl bg-slate-100 px-5 py-4 text-sm text-slate-500">
              Thinking through safe next steps...
            </div>
          )}
        </div>
        <form onSubmit={submit} className="mt-6 flex gap-3">
          <input
            className="flex-1 rounded-2xl border px-4 py-3"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about a product, pickup, or support issue..."
          />
          <button
            disabled={loading}
            className="rounded-2xl bg-brand-600 px-5 py-3 font-semibold text-white disabled:opacity-60"
          >
            Send
          </button>
        </form>
        <p className="mt-4 text-xs text-slate-500">
          Medical disclaimer: this demo provides general product and workflow
          information only and is not medical advice, diagnosis, or treatment.
          For personal health questions, consult a qualified clinician.
        </p>
      </Card>
      <aside className="space-y-4">
        <h2 className="text-lg font-bold">Recommendations</h2>
        {messages.flatMap((m) => m.recommendations ?? []).length === 0 ? (
          <Card>
            <p className="text-sm text-slate-500">
              Product recommendations will appear here when relevant.
            </p>
          </Card>
        ) : (
          messages
            .flatMap((m) => m.recommendations ?? [])
            .map((r) => (
              <Card key={r.id}>
                <Badge tone="blue">{r.type}</Badge>
                <h3 className="mt-3 font-bold">{r.title}</h3>
                <p className="mt-2 text-sm text-slate-600">{r.reason}</p>
              </Card>
            ))
        )}
      </aside>
    </div>
  );
}
