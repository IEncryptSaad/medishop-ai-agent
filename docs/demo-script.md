# MediShop AI Agent Demo Script

## Demo flow

1. Open the home page and select **Open dashboard**.
2. Confirm dashboard metrics for products, conversations, appointments, and support tickets.
3. Open **Products** and search for `moisturizer`.
4. Open a product details card and point out SKU, stock, price, category, and status.
5. Open **Chat** and ask a product question. Highlight safe responses, sources, and recommendation cards.
6. Open **Appointments** and create a pharmacist consultation.
7. Open **Support** and create a support ticket for a delivery or product issue.
8. Return to **Dashboard** and confirm appointment and support activity appears.

## Sample chat questions

- `Which moisturizer is good for sensitive skin?`
- `Do you have a sunscreen recommendation?`
- `What can I do for cold symptoms?`
- `I received a damaged package. What should I do?`
- `Can I schedule a pharmacist consultation?`

## Sample appointment

- Type: `Pharmacist consultation`
- Date/time: choose any future 30-minute slot
- Notes: `Discuss whether the sensitive skin moisturizer fits a fragrance-free routine.`

## Sample support tickets

### Damaged package

- Subject: `Package arrived damaged`
- Priority: `high`
- Category: `order_issue`
- Description: `The package arrived crushed and the moisturizer bottle leaked during shipping.`

### Delivery question

- Subject: `Order tracking question`
- Priority: `normal`
- Category: `shipping`
- Description: `Customer wants to confirm estimated delivery timing for a recent order.`

## Demo safety note

The agent is a mock MVP assistant. It can provide general product and workflow information, but it does not diagnose conditions, provide treatment decisions, call Shopify APIs, or use paid LLM providers.
