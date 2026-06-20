import assert from "node:assert/strict";
import { afterEach, test } from "node:test";

import { ApiError, api, normalizeProductPrice } from "./api";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

test("normalizeProductPrice accepts finite numbers and numeric strings", () => {
  assert.equal(normalizeProductPrice(24.99), 24.99);
  assert.equal(normalizeProductPrice("24.99"), 24.99);
  assert.equal(normalizeProductPrice("0"), 0);
  assert.equal(normalizeProductPrice("100"), 100);
});

test("normalizeProductPrice rejects malformed strings instead of truncating", () => {
  for (const price of ["24.99USD", "12.34.56", "", "abc"] as const) {
    assert.throws(() => normalizeProductPrice(price), ApiError);
  }
});

test("listProducts rejects API products with invalid prices", async () => {
  globalThis.fetch = async () =>
    new Response(
      JSON.stringify({
        data: {
          items: [
            {
              id: "prod-invalid-price",
              sku: "MS-BAD-PRICE",
              name: "Bad Price Product",
              description: "Malformed price should not render.",
              price: "24.99USD",
              currency: "USD",
              stock_quantity: 1,
              status: "active",
              attributes: { category: "General" },
            },
          ],
        },
      }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    );

  await assert.rejects(() => api.listProducts(), ApiError);
});
