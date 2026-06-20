import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MediShop AI Agent",
  description: "AI agent workspace for Shopify medical stores.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
