// POST { sku, currency, embedded } -> starts a checkout for a known package. With embedded:true (and STRIPE_PUBLISHABLE_KEY set)
// it returns a client secret for Stripe's embedded checkout on our own page; if that fails it falls back to Stripe's hosted page.
// Uses Stripe when STRIPE_SECRET_KEY is set, otherwise Airwallex.
import { api, configured, env, json, products } from "./_airwallex.mjs";
import { stripe, stripeOn } from "./_stripe.mjs";
import { RATES, localPrice } from "./_fx.mjs";

export default async (req) => {
  return handler(req);
};

async function handler(req) {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!stripeOn() && !configured()) return json(503, { error: "not_configured" });
  let input = {};
  try { input = await req.json(); } catch {}
  // items: [{sku, qty}] from the cart, or a single {sku}. Prices always come from the server catalog.
  const raw = Array.isArray(input.items) ? input.items : [{ sku: input.sku, qty: 1 }];
  const seen = new Map();
  for (const it of raw.slice(0, 10)) {
    if (!it || !products[it.sku]) return json(400, { error: "unknown_package" });
    const max = String(it.sku).startsWith("addon-") ? 10 : 1;
    seen.set(it.sku, Math.max(1, Math.min(max, (seen.get(it.sku) || 0) + (parseInt(it.qty, 10) || 1))));
  }
  if (!seen.size) return json(400, { error: "unknown_package" });
  const cur = RATES[(input.currency || "").toUpperCase()] ? input.currency.toUpperCase() : "USD";
  const lines = [...seen].map(([sku, qty]) => ({ sku, qty, item: products[sku], unit: products[sku].fixed?.[cur] ?? localPrice(products[sku].amount, cur) }));
  lines.forEach(l => { l.amount = Math.round(l.unit * l.qty * 100) / 100; });
  const amount = Math.round(lines.reduce((a, l) => a + l.amount, 0) * 100) / 100;
  const label = lines.map(l => l.item.name + (l.qty > 1 ? ` ×${l.qty}` : "")).join(" + ").slice(0, 480);
  const skus = lines.map(l => `${l.sku}x${l.qty}`).join(",").slice(0, 480);
  const usdTotal = lines.reduce((a, l) => a + l.item.amount * l.qty, 0);
  const site = process.env.SITE_URL || process.env.URL || new URL(req.url).origin;
  const orderId = `WZ-${new Date().toISOString().slice(2, 10).replace(/-/g, "")}-${Math.random().toString(36).slice(2, 7).toUpperCase()}`;
  try {
    if (stripeOn()) {
      const base = {
        mode: "payment",
        client_reference_id: orderId,
        line_items: Object.fromEntries(lines.map((l, i) => [i, { quantity: l.qty, price_data: { currency: cur.toLowerCase(), unit_amount: Math.round(l.unit * 100), product_data: { name: l.item.name, description: l.item.desc || undefined, images: l.item.image ? { 0: l.item.image } : undefined } } }])),
        phone_number_collection: { enabled: true },
        custom_text: { submit: { message: `By paying you agree to our [Terms of Service](${site}/terms.html) and [Refund Policy](${site}/refund.html). After payment you will fill in a short onboarding form, and we confirm everything with you before filing.` } },
        metadata: { sku: skus, package: label, order_id: orderId, usd_price: String(usdTotal) },
        payment_intent_data: { description: `${label} · ${orderId}`.slice(0, 990), metadata: { sku: skus, order_id: orderId } }
      };
      const done = { order_id: orderId, package: label, amount, currency: cur, lines: lines.map(l => ({ sku: l.sku, qty: l.qty, amount: l.amount })) };
      const pk = process.env.STRIPE_PUBLISHABLE_KEY || "";
      let embErr = "";
      if (input.embedded && pk.startsWith("pk_")) {
        try {
          const s = await stripe("/checkout/sessions", {
            method: "POST", version: "2026-03-25.dahlia",
            body: { ...base, ui_mode: "embedded_page", return_url: `${site}/thank-you.html?session_id={CHECKOUT_SESSION_ID}` }
          });
          if (s.client_secret) return json(200, { provider: "stripe", embedded: true, client_secret: s.client_secret, publishable_key: pk, ...done });
        } catch (e) { console.error("embedded checkout failed, using hosted page", e); embErr = String(e.message).replace(/(sk|rk)_(live|test)_[A-Za-z0-9*]+/g, "[key]").slice(0, 300); }
      }
      const s = await stripe("/checkout/sessions", {
        method: "POST",
        body: { ...base, success_url: `${site}/thank-you.html?session_id={CHECKOUT_SESSION_ID}`, cancel_url: `${site}/packages.html` }
      });
      return json(200, { provider: "stripe", url: s.url, ...done, ...(embErr ? { embedded_error: embErr } : {}) });
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
        metadata: { sku: skus, package: label }
      }
    });
    return json(200, { provider: "airwallex", env, intent_id: intent.id, client_secret: intent.client_secret, currency: intent.currency, order_id: orderId, package: label, amount });
  } catch (e) {
    console.error(e);
    return json(502, { error: "payment_unavailable" });
  }
}
