import { AppShell } from "@/components/app-shell";
import { AppointmentsPanel } from "@/components/features/appointments-panel";
export default function AppointmentsPage(){return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Scheduling</p><h1 className="text-4xl font-bold">Appointments</h1><p className="mt-3 max-w-2xl text-slate-600">Book demo consultations and monitor status across pending and confirmed appointments.</p></div><AppointmentsPanel /></AppShell>}
