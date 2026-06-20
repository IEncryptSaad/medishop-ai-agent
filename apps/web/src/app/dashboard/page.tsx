import { AppShell } from "@/components/app-shell";
import { DashboardPanel } from "@/components/features/dashboard-panel";
export default function DashboardPage(){return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Overview</p><h1 className="text-4xl font-bold">Dashboard</h1><p className="mt-3 max-w-2xl text-slate-600">Snapshot of catalog coverage, conversations, bookings, support volume, and recent activity.</p></div><DashboardPanel /></AppShell>}
