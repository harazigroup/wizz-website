// GET ?intent=int_... -> returns the payment status so the thank-you page can show the onboarding form.
import { api, configured, json } from "./_airwallex.mjs";

export default async (req) => {
  if (!configured()) return json(503, { error: "not_configured" });
  const id = new URL(req.url).searchParams.get("intent") || "";
  if (!/^int_[A-Za-z0-9_-]{6,80}$/.test(id)) return json(400, { error: "bad_id" });
  try {
    const p = await api(`/api/v1/pa/payment_intents/${id}`);
    return json(200, { status: p.status, paid: p.status === "SUCCEEDED", amount: p.amount, currency: p.currency, order_id: p.merchant_order_id, package: p.metadata?.package || "" });
  } catch (e) {
    console.error(e);
    return json(502, { error: "lookup_failed" });
  }
};
