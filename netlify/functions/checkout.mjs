// POST { sku } -> starts a checkout for a known package. Uses Stripe when STRIPE_SECRET_KEY is set, otherwise Airwallex.
import { api, configured, env, json, products } from "./_airwallex.mjs";
import { stripe, stripeOn } from "./_stripe.mjs";
import { RATES, localPrice } from "./_fx.mjs";

export default async (req) => {
  if (req.method === "GET" && new URL(req.url).searchParams.get("diag") === "wizz-1007") {
    // temporary: run a real checkout request for the cheapest package and report Stripe's answer
    const r = await handler(new Request(req.url, { method: "POST", body: JSON.stringify({ sku: "sa-assessment", currency: "MYR" }) }));
    return json(200, { status: r.status, body: await r.json(), key_type: (process.env.STRIPE_SECRET_KEY || "").slice(0, 8).replace(/[^a-z_]/gi, "") });
  }
  return handler(req);
};

async function handler(req) {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!stripeOn() && !configured()) return json(503, { error: "not_configured" });
  let input = {};
  try { input = await req.json(); } catch {}
  const item = products[input.sku];
  if (!item) return json(400, { error: "unknown_package" }); // price always comes from the server catalog
  const cur = RATES[(input.currency || "").toUpperCase()] ? input.currency.toUpperCase() : "USD";
  const amount = localPrice(item.amount, cur); // same rule the page used to show the price
  const site = process.env.SITE_URL || process.env.URL || new URL(req.url).origin;
  const orderId = `WZ-${new Date().toISOString().slice(2, 10).replace(/-/g, "")}-${Math.random().toString(36).slice(2, 7).toUpperCase()}`;
  try {
    if (stripeOn()) {
      const s = await stripe("/checkout/sessions", {
        method: "POST",
        body: {
          mode: "payment",
          client_reference_id: orderId,
          success_url: `${site}/thank-you.html?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${site}/packages.html`,
          line_items: { 0: { quantity: 1, price_data: { currency: cur.toLowerCase(), unit_amount: Math.round(amount * 100), product_data: { name: item.name, description: item.desc, images: item.image ? { 0: item.image } : undefined } } } },
          phone_number_collection: { enabled: true },
          custom_text: { submit: { message: `By paying you agree to our [Terms of Service](${site}/terms.html) and [Refund Policy](${site}/refund.html). After payment you will fill in a short onboarding form, and we confirm everything with you before filing.` } },
          metadata: { sku: input.sku, package: item.name, order_id: orderId, usd_price: String(item.amount) },
          payment_intent_data: { description: `${item.name} · ${orderId}`, metadata: { sku: input.sku, order_id: orderId } }
        }
      });
      return json(200, { provider: "stripe", url: s.url, order_id: orderId, package: item.name, amount, currency: cur });
    }
    const intent = await api("/api/v1/pa/payment_intents/create", {
      method: "POST",
      body: {
        request_id: crypto.randomUUID(),
        amount,
        currency: cur,
        merchant_order_id: orderId,
        descriptor: "WIZZ SMART SERVICES",
        return_url: `${site}/thank-you.html`,
        metadata: { sku: input.sku, package: item.name }
      }
    });
    return json(200, { provider: "airwallex", env, intent_id: intent.id, client_secret: intent.client_secret, currency: intent.currency, order_id: orderId, package: item.name, amount });
  } catch (e) {
    console.error(e);
    return json(502, { error: "payment_unavailable", detail: String(e.message).replace(/(sk|rk)_(live|test)_[A-Za-z0-9*]+/g, "[key]") });
  }
}
