// POST { sku, email? } -> creates an Airwallex PaymentIntent for a known package and returns what the browser needs.
import { api, configured, env, json, products } from "./_airwallex.mjs";

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!configured()) return json(503, { error: "not_configured" });
  let input = {};
  try { input = await req.json(); } catch {}
  const item = products[input.sku];
  if (!item) return json(400, { error: "unknown_package" }); // price always comes from the server catalog
  const site = process.env.SITE_URL || process.env.URL || new URL(req.url).origin;
  const orderId = `WZ-${new Date().toISOString().slice(2, 10).replace(/-/g, "")}-${Math.random().toString(36).slice(2, 7).toUpperCase()}`;
  try {
    const intent = await api("/api/v1/pa/payment_intents/create", {
      method: "POST",
      body: {
        request_id: crypto.randomUUID(),
        amount: item.amount,
        currency: item.currency,
        merchant_order_id: orderId,
        descriptor: "WIZZ SMART SERVICES",
        return_url: `${site}/thank-you.html`,
        metadata: { sku: input.sku, package: item.name },
        ...(typeof input.email === "string" && input.email.includes("@") ? { customer: { email: input.email.slice(0, 120) } } : {})
      }
    });
    return json(200, { env, intent_id: intent.id, client_secret: intent.client_secret, currency: intent.currency, order_id: orderId, package: item.name, amount: item.amount });
  } catch (e) {
    console.error(e);
    return json(502, { error: "payment_unavailable" });
  }
};
