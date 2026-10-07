// Stripe Checkout helpers. The secret key lives in the Netlify env var STRIPE_SECRET_KEY.
const API = "https://api.stripe.com/v1";
export const stripeOn = () => Boolean(process.env.STRIPE_SECRET_KEY);

function form(obj, prefix = "", out = new URLSearchParams()) {
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined || v === null) continue;
    const key = prefix ? `${prefix}[${k}]` : k;
    if (typeof v === "object") form(v, key, out); else out.append(key, String(v));
  }
  return out;
}

export async function stripe(path, { method = "GET", body, version } = {}) {
  const r = await fetch(`${API}${path}`, {
    method,
    headers: { authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`, "content-type": "application/x-www-form-urlencoded", ...(version ? { "stripe-version": version } : {}) },
    body: body ? form(body).toString() : undefined
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Stripe ${path} failed (${r.status}): ${d.error?.message || "unknown error"}`);
  return d;
}
