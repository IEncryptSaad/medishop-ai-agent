import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MediShop AI Agent",
  description: "AI-powered healthcare assistant for product discovery, appointments, support, and medical information.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
