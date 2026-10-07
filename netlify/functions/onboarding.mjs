// POST { session_id, data } -> saves the onboarding form to the client's order, after checking the payment with Stripe.
import { json } from "./_airwallex.mjs";
import { stripe, stripeOn } from "./_stripe.mjs";
import { dbOn, recordStripeOrder, rpc } from "./_db.mjs";

const FIELDS = ["full_name", "email", "whatsapp", "nationality", "residential_address", "national_id_number", "passport_number", "company_names", "business_activity", "owners", "brand_model", "notes"];

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!stripeOn() || !dbOn()) return json(503, { error: "not_configured" });
  let input = {};
  try { input = await req.json(); } catch {}
  const sid = String(input.session_id || "");
  if (!/^cs_(test|live)_[A-Za-z0-9]{10,200}$/.test(sid)) return json(400, { error: "bad_id" });
  const data = {};
  for (const k of FIELDS) if (input.data && typeof input.data[k] === "string") data[k] = input.data[k].slice(0, 2000);
  try {
    const s = await stripe(`/checkout/sessions/${sid}`);
    if (s.payment_status !== "paid") return json(409, { error: "not_paid" });
    await recordStripeOrder(s);
    const ok = await rpc("server_save_onboarding", { p_order_ref: s.client_reference_id, p_data: data });
    return json(200, { saved: Boolean(ok) });
  } catch (e) {
    console.error(e);
    return json(502, { error: "save_failed" });
  }
};
