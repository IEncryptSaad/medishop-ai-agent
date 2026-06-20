import { AppShell } from "@/components/app-shell";
import { ProductBrowser } from "@/components/features/product-browser";

export default function ProductsPage() {
  return <AppShell><div className="mb-8"><p className="font-semibold text-brand-700">Catalog</p><h1 className="text-4xl font-bold">Products</h1><p className="mt-3 max-w-2xl text-slate-600">Browse demo medical-store inventory with search, category filtering, stock states, and product details.</p></div><ProductBrowser /></AppShell>;
}
