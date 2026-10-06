// POST { sku } -> starts a checkout for a known package. Uses Stripe when STRIPE_SECRET_KEY is set, otherwise Airwallex.
import { api, configured, env, json, products } from "./_airwallex.mjs";
import { stripe, stripeOn } from "./_stripe.mjs";
import { RATES, localPrice } from "./_fx.mjs";

export default async (req) => {
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
          line_items: { 0: { quantity: 1, price_data: { currency: cur.toLowerCase(), unit_amount: Math.round(amount * 100), product_data: { name: item.name } } } },
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
    return json(502, { error: "payment_unavailable" });
  }
};
