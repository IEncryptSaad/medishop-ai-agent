import Link from "next/link";

const navigation = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/chat", label: "Chat" },
  { href: "/appointments", label: "Appointments" },
  { href: "/support", label: "Support" },
];

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <main className="min-h-screen bg-slate-50">
      <nav className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="text-lg font-semibold text-brand-700">
            MediShop AI Agent
          </Link>
          <div className="flex gap-4 text-sm font-medium text-slate-600">
            {navigation.map((item) => (
              <Link key={item.href} href={item.href} className="hover:text-brand-700">
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>
      <section className="mx-auto max-w-6xl px-6 py-10">{children}</section>
    </main>
  );
}
