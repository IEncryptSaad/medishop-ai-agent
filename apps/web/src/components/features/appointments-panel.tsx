"use client";
import { FormEvent, useEffect, useState } from "react";
import { ApiError, api, Appointment } from "@/lib/api";
import { Badge, Card, EmptyState } from "@/components/ui/card";

const tone = (s: string) =>
  s === "confirmed" ? "green" : s === "cancelled" ? "red" : "amber";

export function AppointmentsPanel() {
  const [items, setItems] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listAppointments()
      .then(setItems)
      .catch((err) =>
        setError(
          err instanceof ApiError
            ? err.userMessage
            : "Appointments could not be loaded.",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const fd = new FormData(form);
    const start = new Date(String(fd.get("date")));
    const end = new Date(start.getTime() + 30 * 60000);
    setError(null);
    try {
      const item = await api.createAppointment({
        appointment_type: String(fd.get("type")),
        scheduled_start: start.toISOString(),
        scheduled_end: end.toISOString(),
        notes: String(fd.get("notes") || ""),
      });
      setItems((current) => [item, ...current]);
      form.reset();
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.userMessage
          : "Appointment could not be created.",
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
          <h2 className="text-xl font-bold">Book appointment</h2>
          <form onSubmit={submit} className="mt-5 space-y-4">
            <input
              name="type"
              required
              className="w-full rounded-2xl border px-4 py-3"
              placeholder="Appointment type"
            />
            <input
              name="date"
              required
              type="datetime-local"
              className="w-full rounded-2xl border px-4 py-3"
            />
            <textarea
              name="notes"
              className="min-h-28 w-full rounded-2xl border px-4 py-3"
              placeholder="Notes"
            />
            <button className="w-full rounded-2xl bg-brand-600 px-5 py-3 font-semibold text-white">
              Create booking
            </button>
          </form>
        </Card>
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Upcoming appointments</h2>
          {loading ? (
            <EmptyState
              title="Loading appointments"
              description="Checking current bookings."
            />
          ) : items.length === 0 ? (
            <EmptyState
              title="No appointments"
              description="Create the first demo booking."
            />
          ) : (
            items.map((a) => (
              <Card key={a.id}>
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <h3 className="font-bold">{a.appointment_type}</h3>
                    <p className="mt-1 text-sm text-slate-600">
                      {new Date(a.scheduled_start).toLocaleString()} · 30
                      minutes
                    </p>
                    <p className="mt-2 text-sm text-slate-500">{a.notes}</p>
                  </div>
                  <Badge tone={tone(a.status)}>{a.status}</Badge>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
