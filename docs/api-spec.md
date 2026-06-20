# MediShop AI Agent API Contract Specification

All v1 endpoints return a consistent JSON envelope. Successful responses use `success: true` with a `data` object. Error responses use `success: false` with a stable `error` code, a readable `message`, optional `details`, and optional `request_id`.

## Authentication Strategy

- Public endpoints: `GET /api/v1/health`, `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, and `POST /api/v1/auth/refresh`.
- Protected endpoints: all agent, product, appointment, support, and current-user endpoints unless explicitly opened later.
- Clients authenticate with `Authorization: Bearer <access_token>`.
- Access tokens should be short-lived JWTs. Refresh tokens should be opaque or signed, stored securely by the client, and rotated on refresh.
- Server responses may include `request_id` for tracing authentication and authorization failures.

## Shared Models

### Success Envelope

```json
{
  "success": true,
  "data": {},
  "message": "Optional success message",
  "request_id": "req_123"
}
```

### Pagination

List responses include pagination metadata:

```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 42,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "validation_error",
  "message": "One or more request fields are invalid.",
  "details": [
    { "field": "message", "message": "Field is required." }
  ],
  "request_id": "req_123"
}
```

Common error codes: `validation_error`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `rate_limited`, and `internal_error`.

## Health

### `GET /api/v1/health`

Response example:

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "version": "0.1.0",
    "timestamp": "2026-06-20T12:00:00Z"
  },
  "message": null,
  "request_id": "req_123"
}
```

## Auth

### `POST /api/v1/auth/register`

Request example:

```json
{
  "email": "customer@example.com",
  "password": "correct-horse-battery-staple",
  "full_name": "Ada Lovelace",
  "phone": "+15551234567"
}
```

Response example:

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "rt_abc123",
    "token_type": "bearer",
    "expires_at": "2026-06-20T12:15:00Z",
    "user": {
      "id": "11111111-1111-1111-1111-111111111111",
      "email": "customer@example.com",
      "full_name": "Ada Lovelace",
      "phone": "+15551234567",
      "role": "customer",
      "created_at": "2026-06-20T12:00:00Z",
      "updated_at": "2026-06-20T12:00:00Z"
    }
  },
  "message": "Registration successful.",
  "request_id": "req_123"
}
```

### `POST /api/v1/auth/login`

Request example:

```json
{
  "email": "customer@example.com",
  "password": "correct-horse-battery-staple"
}
```

Response: same `AuthEnvelope` shape as register.

### `POST /api/v1/auth/refresh`

Request example:

```json
{ "refresh_token": "rt_abc123" }
```

Response: same `AuthEnvelope` shape as register.

### `GET /api/v1/auth/me`

Response example:

```json
{
  "success": true,
  "data": {
    "id": "11111111-1111-1111-1111-111111111111",
    "email": "customer@example.com",
    "full_name": "Ada Lovelace",
    "phone": "+15551234567",
    "role": "customer",
    "created_at": "2026-06-20T12:00:00Z",
    "updated_at": "2026-06-20T12:00:00Z"
  },
  "message": null,
  "request_id": "req_123"
}
```

## Agent

### `POST /api/v1/agent/chat`

Request example:

```json
{
  "session_id": "web-session-123",
  "message": "Which moisturizer is best for sensitive skin?"
}
```

Response example:

```json
{
  "success": true,
  "data": {
    "response": "For sensitive skin, look for fragrance-free moisturizers with ceramides.",
    "sources": [
      {
        "title": "Sensitive Skin Care Guide",
        "source_type": "knowledge_document",
        "uri": "kb://sensitive-skin-care",
        "score": 0.92,
        "metadata": { "chunk_index": 3 }
      }
    ],
    "recommendations": [
      {
        "id": "22222222-2222-2222-2222-222222222222",
        "type": "product",
        "title": "Ceramide Daily Moisturizer",
        "reason": "Fragrance-free and in stock.",
        "metadata": { "sku": "CRM-001" }
      }
    ],
    "conversation_id": "33333333-3333-3333-3333-333333333333"
  },
  "message": null,
  "request_id": "req_123"
}
```

## Products

### `GET /api/v1/products`

Query parameters: `page`, `page_size`, `category_id`, `status`, `min_price`, `max_price`.

Response example:

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "22222222-2222-2222-2222-222222222222",
        "category_id": null,
        "sku": "CRM-001",
        "name": "Ceramide Daily Moisturizer",
        "description": "Lightweight daily moisturizer.",
        "price": "24.99",
        "currency": "USD",
        "stock_quantity": 12,
        "status": "active",
        "shopify_product_id": "gid://shopify/Product/1",
        "attributes": { "skin_type": "sensitive" },
        "created_at": "2026-06-20T12:00:00Z",
        "updated_at": "2026-06-20T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 1,
      "total_pages": 1,
      "has_next": false,
      "has_previous": false
    }
  },
  "message": null,
  "request_id": "req_123"
}
```

### `GET /api/v1/products/{id}`

Response: a single product in `ProductEnvelope`.

### `POST /api/v1/products/search`

Request example:

```json
{
  "query": "sensitive skin moisturizer",
  "page": 1,
  "page_size": 20,
  "category_id": null,
  "in_stock_only": true,
  "min_price": "10.00",
  "max_price": "50.00",
  "attributes": { "fragrance_free": true }
}
```

Response: same paginated product list shape as `GET /api/v1/products`.

## Appointments

### `POST /api/v1/appointments`

Request example:

```json
{
  "appointment_type": "pharmacist_consultation",
  "scheduled_start": "2026-06-21T15:00:00Z",
  "scheduled_end": "2026-06-21T15:30:00Z",
  "notes": "Discuss skincare routine.",
  "metadata": { "channel": "web" }
}
```

Response: created appointment in `AppointmentEnvelope`.

### `GET /api/v1/appointments`

Query parameters: `page`, `page_size`, `status`, `from_date`, `to_date`.

Response: paginated appointment list in `AppointmentListEnvelope`.

### `PATCH /api/v1/appointments/{id}`

Request example:

```json
{
  "scheduled_start": "2026-06-21T16:00:00Z",
  "scheduled_end": "2026-06-21T16:30:00Z",
  "status": "rescheduled",
  "notes": "Customer requested a later time.",
  "metadata": { "rescheduled_by": "customer" }
}
```

Response: updated appointment in `AppointmentEnvelope`.

## Support

### `POST /api/v1/support/tickets`

Request example:

```json
{
  "subject": "Order arrived damaged",
  "description": "The moisturizer bottle leaked during shipping.",
  "priority": "normal",
  "category": "order_issue",
  "metadata": { "order_id": "MS-1001" }
}
```

Response: created support ticket in `SupportTicketEnvelope`.

### `GET /api/v1/support/tickets`

Query parameters: `page`, `page_size`, `status`, `priority`, `category`, `created_from`, `created_to`.

Response: paginated support ticket list in `SupportTicketListEnvelope`.

### `PATCH /api/v1/support/tickets/{id}`

Request example:

```json
{
  "status": "in_progress",
  "priority": "high",
  "metadata": { "assigned_team": "customer_care" }
}
```

Response: updated support ticket in `SupportTicketEnvelope`.
