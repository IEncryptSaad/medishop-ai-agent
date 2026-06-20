import { AppShell } from "@/components/app-shell";
import { PlaceholderPage } from "@/components/placeholder-page";

export default function HomePage() {
  return (
    <AppShell>
      <PlaceholderPage
        title="MediShop AI Agent"
        description="Production-grade monorepo foundation for an AI agent MVP serving Shopify medical stores."
      />
    </AppShell>
  );
}
