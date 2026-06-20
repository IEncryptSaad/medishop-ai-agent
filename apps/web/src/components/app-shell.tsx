import Link from "next/link";

const navigation = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/chat", label: "Chat" },
  { href: "/products", label: "Products" },
  { href: "/appointments", label: "Appointments" },
  { href: "/support", label: "Support" },
];

export function AppShell({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-blue-50 text-slate-950">
      <nav className="sticky top-0 z-20 border-b border-white/70 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-4 md:flex-row md:items-center md:justify-between">
          <Link href="/" className="flex items-center gap-3 text-lg font-bold text-brand-700">
            <span className="grid size-10 place-items-center rounded-2xl bg-brand-600 text-white shadow-lg shadow-blue-200">M</span>
            <span>MediShop AI Agent</span>
          </Link>
          <div className="flex flex-wrap gap-2 text-sm font-semibold text-slate-600">
            {navigation.map((item) => <Link key={item.href} href={item.href} className="rounded-full px-4 py-2 hover:bg-brand-50 hover:text-brand-700">{item.label}</Link>)}
          </div>
        </div>
      </nav>
      <section className="mx-auto max-w-7xl px-6 py-8 md:py-10">{children}</section>
    </main>
  );
}
