// GET ?session_id=cs_... (Stripe) or ?intent=int_... (Airwallex) -> payment status for the thank-you page.
import { api, configured, json } from "./_airwallex.mjs";
import { stripe, stripeOn } from "./_stripe.mjs";
import { recordStripeOrder } from "./_db.mjs";

export default async (req) => {
  const q = new URL(req.url).searchParams;
  const sid = q.get("session_id") || "", id = q.get("intent") || "";
  try {
    if (sid) {
      if (!stripeOn()) return json(503, { error: "not_configured" });
      if (!/^cs_(test|live)_[A-Za-z0-9]{10,200}$/.test(sid)) return json(400, { error: "bad_id" });
      const s = await stripe(`/checkout/sessions/${sid}`);
      let saved = false;
      try { saved = Boolean(await recordStripeOrder(s)); } catch (e) { console.error("order not saved", e); }
      return json(200, { status: s.payment_status, paid: s.payment_status === "paid", amount: (s.amount_total || 0) / 100, currency: (s.currency || "").toUpperCase(), order_id: s.client_reference_id, package: s.metadata?.package || "", email: s.payment_status === "paid" ? (s.customer_details?.email || "") : "", account: saved });
    }
    if (!configured()) return json(503, { error: "not_configured" });
    if (!/^int_[A-Za-z0-9_-]{6,80}$/.test(id)) return json(400, { error: "bad_id" });
    const p = await api(`/api/v1/pa/payment_intents/${id}`);
    return json(200, { status: p.status, paid: p.status === "SUCCEEDED", amount: p.amount, currency: p.currency, order_id: p.merchant_order_id, package: p.metadata?.package || "" });
  } catch (e) {
    console.error(e);
    return json(502, { error: "lookup_failed" });
  }
};
