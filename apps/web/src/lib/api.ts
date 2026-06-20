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

export type AgentSource = {
  title: string;
  source_type: string;
  uri?: string | null;
  score?: number | null;
};
export type AgentRecommendation = {
  id: string;
  type: string;
  title: string;
  reason?: string | null;
  metadata?: Record<string, unknown>;
};
export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: AgentSource[];
  recommendations?: AgentRecommendation[];
};
export type Appointment = {
  id: string;
  appointment_type: string;
  scheduled_start: string;
  scheduled_end: string;
  status: string;
  notes?: string | null;
};
export type SupportTicket = {
  id: string;
  subject: string;
  description: string;
  status: string;
  priority: string;
  category?: string | null;
};
export type Health = { status: string; version: string; timestamp: string };

type Envelope<T> = { data: T; message?: string; request_id?: string | null };
type ErrorEnvelope = {
  message?: string;
  details?: Array<{ field?: string; message?: string }>;
};
type Page<T> = {
  items: T[];
  total?: number;
  page?: number;
  page_size?: number;
  pagination?: { total_items: number; page: number; page_size: number };
};

const DEFAULT_API_URL = "http://localhost:8000";
const API_URL = (process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL).replace(
  /\/$/,
  "",
);

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details: string[] = [],
    public backendUnavailable = false,
  ) {
    super(message);
    this.name = "ApiError";
  }

  get userMessage() {
    return this.details.length
      ? `${this.message} ${this.details.join(" ")}`
      : this.message;
  }
}

const mockProducts: Product[] = [
  {
    id: "prod-1",
    sku: "MS-SALINE-001",
    name: "Gentle Saline Nasal Spray",
    description:
      "Drug-free saline spray for nasal dryness and everyday congestion support.",
    price: 12.99,
    currency: "USD",
    stock_quantity: 42,
    status: "active",
    category_id: "respiratory",
    attributes: { category: "Respiratory", tag: "Drug-free" },
  },
  {
    id: "prod-2",
    sku: "MS-SKIN-014",
    name: "Sensitive Skin Moisturizer",
    description:
      "Fragrance-free daily moisturizer for sensitive skin routines.",
    price: 18.5,
    currency: "USD",
    stock_quantity: 28,
    status: "active",
    category_id: "skincare",
    attributes: { category: "Skincare", tag: "Fragrance-free" },
  },
  {
    id: "prod-3",
    sku: "MS-FIRSTAID-221",
    name: "Compact First Aid Kit",
    description:
      "Travel-ready kit with bandages, gauze, and basic wound-care supplies.",
    price: 24.0,
    currency: "USD",
    stock_quantity: 15,
    status: "active",
    category_id: "first-aid",
    attributes: { category: "First Aid", tag: "Travel" },
  },
  {
    id: "prod-4",
    sku: "MS-VITD-1000",
    name: "Vitamin D3 1000 IU",
    description:
      "Daily wellness supplement. Consult a clinician for personal dosage guidance.",
    price: 9.75,
    currency: "USD",
    stock_quantity: 64,
    status: "active",
    category_id: "wellness",
    attributes: { category: "Wellness", tag: "Supplement" },
  },
];

let mockAppointments: Appointment[] = [
  {
    id: "appt-1",
    appointment_type: "Pharmacist consultation",
    scheduled_start: new Date(Date.now() + 86400000).toISOString(),
    scheduled_end: new Date(Date.now() + 88200000).toISOString(),
    status: "confirmed",
    notes: "Discuss product fit and usage questions.",
  },
  {
    id: "appt-2",
    appointment_type: "Store pickup assistance",
    scheduled_start: new Date(Date.now() + 172800000).toISOString(),
    scheduled_end: new Date(Date.now() + 174600000).toISOString(),
    status: "pending",
    notes: "Review order pickup options.",
  },
];

let mockTickets: SupportTicket[] = [
  {
    id: "ticket-1",
    subject: "Order tracking question",
    description: "Customer asked for estimated delivery timing.",
    status: "open",
    priority: "normal",
    category: "shipping",
  },
  {
    id: "ticket-2",
    subject: "Damaged package",
    description: "Package arrived with crushed exterior box.",
    status: "triage",
    priority: "high",
    category: "order",
  },
];

function normalizeProduct(product: Product): Product {
  return { ...product, price: Number(product.price) };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      cache: "no-store",
    });
  } catch {
    throw new ApiError(
      "Backend is unavailable; showing demo data instead.",
      undefined,
      [],
      true,
    );
  }

  if (!res.ok) {
    let body: ErrorEnvelope = {};
    try {
      body = await res.json();
    } catch {
      /* ignore invalid error bodies */
    }
    const details =
      body.details
        ?.map((detail) =>
          [detail.field, detail.message].filter(Boolean).join(": "),
        )
        .filter(Boolean) ?? [];
    throw new ApiError(
      body.message || `API request failed with status ${res.status}.`,
      res.status,
      details,
    );
  }
  return res.json() as Promise<T>;
}

const page = <T>(items: T[]): Page<T> => ({
  items,
  total: items.length,
  page: 1,
  page_size: items.length,
});
const isBackendUnavailable = (error: unknown) =>
  error instanceof ApiError && error.backendUnavailable;
const filterMockProducts = (query = "", category = "All") =>
  mockProducts
    .filter((p) =>
      `${p.name} ${p.description}`.toLowerCase().includes(query.toLowerCase()),
    )
    .filter((p) => category === "All" || p.attributes.category === category);

export const api = {
  async health(): Promise<Health> {
    return (await request<Envelope<Health>>("/api/v1/health")).data;
  },
  async listProducts(query = "", category = "All"): Promise<Product[]> {
    try {
      const payload = query
        ? await request<Envelope<Page<Product>>>("/api/v1/products/search", {
            method: "POST",
            body: JSON.stringify({ query, in_stock_only: false }),
          })
        : await request<Envelope<Page<Product>>>("/api/v1/products");
      return payload.data.items
        .map(normalizeProduct)
        .filter(
          (p) => category === "All" || p.attributes.category === category,
        );
    } catch (error) {
      if (isBackendUnavailable(error))
        return filterMockProducts(query, category);
      throw error;
    }
  },
  async sendChat(sessionId: string, message: string) {
    try {
      const payload = await request<
        Envelope<{
          response: string;
          sources: AgentSource[];
          recommendations: AgentRecommendation[];
          conversation_id: string;
        }>
      >("/api/v1/agent/chat", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, message }),
      });
      return payload.data;
    } catch (error) {
      if (!isBackendUnavailable(error)) throw error;
      const picks = mockProducts
        .filter((p) =>
          message
            .toLowerCase()
            .split(/\s+/)
            .some(
              (w) =>
                p.name.toLowerCase().includes(w) ||
                p.description?.toLowerCase().includes(w),
            ),
        )
        .slice(0, 2);
      return {
        response:
          "The backend is currently unavailable, so I am using demo product data. I can still help with safe, non-diagnostic product discovery suggestions.",
        conversation_id: sessionId,
        sources: [
          {
            title: "MediShop demo knowledge base",
            source_type: "mock",
            score: 0.91,
          },
        ],
        recommendations: picks.map((p) => ({
          id: p.id,
          type: "product",
          title: p.name,
          reason: p.description ?? "Catalog match",
          metadata: { price: p.price, sku: p.sku },
        })),
      };
    }
  },
  async listAppointments() {
    try {
      return (
        await request<Envelope<Page<Appointment>>>("/api/v1/appointments")
      ).data.items;
    } catch (error) {
      if (isBackendUnavailable(error)) return mockAppointments;
      throw error;
    }
  },
  async createAppointment(input: Omit<Appointment, "id" | "status">) {
    try {
      return (
        await request<Envelope<Appointment>>("/api/v1/appointments", {
          method: "POST",
          body: JSON.stringify(input),
        })
      ).data;
    } catch (error) {
      if (!isBackendUnavailable(error)) throw error;
      const item = { ...input, id: `appt-${Date.now()}`, status: "pending" };
      mockAppointments = [item, ...mockAppointments];
      return item;
    }
  },
  async updateAppointment(id: string, input: Partial<Omit<Appointment, "id">>) {
    return (
      await request<Envelope<Appointment>>(`/api/v1/appointments/${id}`, {
        method: "PATCH",
        body: JSON.stringify(input),
      })
    ).data;
  },
  async listTickets() {
    try {
      return (
        await request<Envelope<Page<SupportTicket>>>("/api/v1/support/tickets")
      ).data.items;
    } catch (error) {
      if (isBackendUnavailable(error)) return mockTickets;
      throw error;
    }
  },
  async createTicket(
    input: Pick<
      SupportTicket,
      "subject" | "description" | "priority" | "category"
    >,
  ) {
    try {
      return (
        await request<Envelope<SupportTicket>>("/api/v1/support/tickets", {
          method: "POST",
          body: JSON.stringify(input),
        })
      ).data;
    } catch (error) {
      if (!isBackendUnavailable(error)) throw error;
      const item = { ...input, id: `ticket-${Date.now()}`, status: "open" };
      mockTickets = [item, ...mockTickets];
      return item;
    }
  },
  async updateTicket(id: string, input: Partial<Omit<SupportTicket, "id">>) {
    return (
      await request<Envelope<SupportTicket>>(`/api/v1/support/tickets/${id}`, {
        method: "PATCH",
        body: JSON.stringify(input),
      })
    ).data;
  },
  async dashboard() {
    const [products, appointments, tickets] = await Promise.all([
      this.listProducts(),
      this.listAppointments(),
      this.listTickets(),
    ]);
    return { products, appointments, tickets, conversations: 12 };
  },
};
