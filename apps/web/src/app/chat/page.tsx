import { AppShell } from "@/components/app-shell";
import { ChatConsole } from "@/components/features/chat-console";

export default function ChatPage() { return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Assistant</p><h1 className="text-4xl font-bold">Chat</h1><p className="mt-3 max-w-2xl text-slate-600">Ask healthcare product, appointment, support, and medical information questions with clear sources and recommendations.</p></div><ChatConsole /></AppShell>; }
