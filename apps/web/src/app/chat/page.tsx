import { AppShell } from "@/components/app-shell";
import { ChatConsole } from "@/components/features/chat-console";

export default function ChatPage() { return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Assistant</p><h1 className="text-4xl font-bold">Chat</h1><p className="mt-3 max-w-2xl text-slate-600">Demo a safe AI-agent flow with loading states, source cards, and product recommendation cards.</p></div><ChatConsole /></AppShell>; }
