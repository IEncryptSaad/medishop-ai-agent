"use client";

import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";
import { Badge, Card, EmptyState } from "@/components/ui/card";

type Data = Awaited<ReturnType<typeof api.dashboard>>;

export function DashboardPanel() {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .dashboard()
      .then(setData)
      .catch((err) =>
        setError(
          err instanceof ApiError
            ? err.userMessage
            : "Dashboard metrics could not be loaded.",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <EmptyState
        title="Loading dashboard"
        description="Preparing dashboard metrics."
      />
    );
  }

  if (error) {
    return <EmptyState title="Dashboard unavailable" description={error} />;
  }

  if (!data) {
    return (
      <EmptyState title="No dashboard data" description="Refresh to retry." />
    );
  }

  const metrics = [
    ["Total products", data.products.length],
    ["Conversations", data.conversations],
    ["Appointments", data.appointments.length],
    ["Support tickets", data.tickets.length],
  ] as const;
  const activity = [
    ...data.appointments.slice(0, 2).map((appointment) => ({
      id: appointment.id,
      label: `Appointment booked: ${appointment.appointment_type}`,
      status: appointment.status,
      tone: "green" as const,
    })),
    ...data.tickets.slice(0, 2).map((ticket) => ({
      id: ticket.id,
      label: `Support ticket: ${ticket.subject}`,
      status: ticket.status,
      tone: "blue" as const,
    })),
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        {metrics.map(([label, value]) => (
          <Card key={label}>
            <p className="text-sm font-semibold text-slate-500">{label}</p>
            <p className="mt-3 text-4xl font-bold text-brand-700">{value}</p>
          </Card>
        ))}
      </div>
      <Card>
        <h2 className="text-xl font-bold">Recent activity</h2>
        <div className="mt-5 space-y-4">
          {activity.length === 0 ? (
            <EmptyState
              title="No recent activity"
              description="New appointments and support tickets will appear here."
            />
          ) : (
            activity.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between rounded-2xl bg-slate-50 p-4"
              >
                <span>{item.label}</span>
                <Badge tone={item.tone}>{item.status}</Badge>
              </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}
