import { AppShell } from "@/components/app-shell";
import { SupportPanel } from "@/components/features/support-panel";
export default function SupportPage(){return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Care operations</p><h1 className="text-4xl font-bold">Support</h1><p className="mt-3 max-w-2xl text-slate-600">Create support tickets and review priority, category, and triage status in one workspace.</p></div><SupportPanel /></AppShell>}
