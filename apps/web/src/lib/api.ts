
export type Product = {
  id: string;
  category_id?: string | null;
  sku: string;
  name: string;
  description?: string | null;
  price: number;
  currency: string;
  stock_quantity: number;
  status: string;
  attributes: Record<string, string | number | boolean>;
};

export type AgentSource = { title: string; source_type: string; uri?: string | null; score?: number | null };
export type AgentRecommendation = { id: string; type: string; title: string; reason?: string | null; metadata?: Record<string, unknown> };
export type ChatMessage = { id: string; role: "user" | "assistant"; content: string; sources?: AgentSource[]; recommendations?: AgentRecommendation[] };
export type Appointment = { id: string; appointment_type: string; scheduled_start: string; scheduled_end: string; status: string; notes?: string | null };
export type SupportTicket = { id: string; subject: string; description: string; status: string; priority: string; category?: string | null };

type Envelope<T> = { data: T };
type Page<T> = { items: T[]; total: number; page: number; page_size: number };
type ApiProduct = Omit<Product, "price"> & { price: number | string };

const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "";

const mockProducts: Product[] = [
  { id: "prod-1", sku: "MS-SALINE-001", name: "Gentle Saline Nasal Spray", description: "Drug-free saline spray for nasal dryness and everyday congestion support.", price: 12.99, currency: "USD", stock_quantity: 42, status: "active", category_id: "respiratory", attributes: { category: "Respiratory", tag: "Drug-free" } },
  { id: "prod-2", sku: "MS-SKIN-014", name: "Sensitive Skin Moisturizer", description: "Fragrance-free daily moisturizer for sensitive skin routines.", price: 18.5, currency: "USD", stock_quantity: 28, status: "active", category_id: "skincare", attributes: { category: "Skincare", tag: "Fragrance-free" } },
  { id: "prod-3", sku: "MS-FIRSTAID-221", name: "Compact First Aid Kit", description: "Travel-ready kit with bandages, gauze, and basic wound-care supplies.", price: 24.0, currency: "USD", stock_quantity: 15, status: "active", category_id: "first-aid", attributes: { category: "First Aid", tag: "Travel" } },
  { id: "prod-4", sku: "MS-VITD-1000", name: "Vitamin D3 1000 IU", description: "Daily wellness supplement. Consult a clinician for personal dosage guidance.", price: 9.75, currency: "USD", stock_quantity: 64, status: "active", category_id: "wellness", attributes: { category: "Wellness", tag: "Supplement" } },
];

let mockAppointments: Appointment[] = [
  { id: "appt-1", appointment_type: "Pharmacist consultation", scheduled_start: new Date(Date.now() + 86400000).toISOString(), scheduled_end: new Date(Date.now() + 88200000).toISOString(), status: "confirmed", notes: "Discuss product fit and usage questions." },
  { id: "appt-2", appointment_type: "Store pickup assistance", scheduled_start: new Date(Date.now() + 172800000).toISOString(), scheduled_end: new Date(Date.now() + 174600000).toISOString(), status: "pending", notes: "Review order pickup options." },
];

let mockTickets: SupportTicket[] = [
  { id: "ticket-1", subject: "Order tracking question", description: "Customer asked for estimated delivery timing.", status: "open", priority: "normal", category: "shipping" },
  { id: "ticket-2", subject: "Damaged package", description: "Package arrived with crushed exterior box.", status: "triage", priority: "high", category: "order" },
];

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!API_URL) throw new Error("API URL unavailable");
  const res = await fetch(`${API_URL}${path}`, { ...init, headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) }, cache: "no-store" });
  if (!res.ok) throw new Error(`API request failed: ${res.status}`);
  return res.json() as Promise<T>;
}

const page = <T>(items: T[]): Page<T> => ({ items, total: items.length, page: 1, page_size: items.length });
const parseProductPrice = (price: ApiProduct["price"]): number => {
  const normalizedPrice = typeof price === "number" ? price : Number.parseFloat(price);
  if (!Number.isFinite(normalizedPrice)) throw new Error("Invalid product price from API");
  return normalizedPrice;
};

const normalizeProduct = (product: ApiProduct): Product => ({ ...product, price: parseProductPrice(product.price) });

export const api = {
  async listProducts(query = "", category = "All"): Promise<Product[]> {
    try {
      const payload = query ? await request<Envelope<Page<ApiProduct>>>("/api/v1/products/search", { method: "POST", body: JSON.stringify({ query, in_stock_only: false }) }) : await request<Envelope<Page<ApiProduct>>>("/api/v1/products");
      return payload.data.items.map(normalizeProduct);
    } catch {
      return mockProducts.filter((p) => `${p.name} ${p.description}`.toLowerCase().includes(query.toLowerCase())).filter((p) => category === "All" || p.attributes.category === category);
    }
  },
  async sendChat(sessionId: string, message: string) {
    try {
      const payload = await request<Envelope<{ response: string; sources: AgentSource[]; recommendations: AgentRecommendation[]; conversation_id: string }>>("/api/v1/agent/chat", { method: "POST", body: JSON.stringify({ session_id: sessionId, message }) });
      return payload.data;
    } catch {
      const picks = mockProducts.filter((p) => message.toLowerCase().split(/\s+/).some((w) => p.name.toLowerCase().includes(w) || p.description?.toLowerCase().includes(w))).slice(0, 2);
      return { response: "I can help with product discovery, appointment routing, and support triage. Here are safe, non-diagnostic suggestions based on your message.", conversation_id: sessionId, sources: [{ title: "MediShop demo knowledge base", source_type: "mock", score: 0.91 }], recommendations: picks.map((p) => ({ id: p.id, type: "product", title: p.name, reason: p.description ?? "Catalog match", metadata: { price: p.price, sku: p.sku } })) };
    }
  },
  async listAppointments() { try { return (await request<Envelope<Page<Appointment>>>("/api/v1/appointments")).data.items; } catch { return mockAppointments; } },
  async createAppointment(input: Omit<Appointment, "id" | "status">) { try { return (await request<Envelope<Appointment>>("/api/v1/appointments", { method: "POST", body: JSON.stringify(input) })).data; } catch { const item = { ...input, id: `appt-${Date.now()}`, status: "pending" }; mockAppointments = [item, ...mockAppointments]; return item; } },
  async listTickets() { try { return (await request<Envelope<Page<SupportTicket>>>("/api/v1/support/tickets")).data.items; } catch { return mockTickets; } },
  async createTicket(input: Pick<SupportTicket, "subject" | "description" | "priority" | "category">) { try { return (await request<Envelope<SupportTicket>>("/api/v1/support/tickets", { method: "POST", body: JSON.stringify(input) })).data; } catch { const item = { ...input, id: `ticket-${Date.now()}`, status: "open" }; mockTickets = [item, ...mockTickets]; return item; } },
  async dashboard() { const [products, appointments, tickets] = await Promise.all([this.listProducts(), this.listAppointments(), this.listTickets()]); return { products, appointments, tickets, conversations: 12 }; },
};
