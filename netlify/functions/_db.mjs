// Calls the Wizz Supabase database from the server. The URL and anon key are public;
// the server-only database functions also need WIZZ_DB_SECRET, which lives only in Netlify.
export const SUPABASE_URL = "https://mzkkhotipmgqczavrfqy.supabase.co";
export const SUPABASE_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16a2tob3RpcG1ncWN6YXZyZnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEzNjA5OTEsImV4cCI6MjEwNjkzNjk5MX0.-RX74vfMP8qedH2F7XvBN4OGj_dL8yEX96VlXO8ONA0";
export const dbOn = () => Boolean(process.env.WIZZ_DB_SECRET);

export async function rpc(name, args) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${name}`, {
    method: "POST",
    headers: { apikey: SUPABASE_ANON, authorization: `Bearer ${SUPABASE_ANON}`, "content-type": "application/json" },
    body: JSON.stringify({ p_secret: process.env.WIZZ_DB_SECRET, ...args })
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`db ${name} failed (${r.status}): ${text.slice(0, 200)}`);
  return text ? JSON.parse(text) : null;
}

// "uk-businessx1,addon-bankx2" -> [{sku, qty}]
export const parseSkus = s => String(s || "").split(",").map(x => /^(.+)x(\d+)$/.exec(x.trim())).filter(Boolean).map(m => ({ sku: m[1], qty: +m[2] }));

// Save a paid Stripe Checkout Session as an order. Safe to call more than once.
export async function recordStripeOrder(s) {
  if (!dbOn() || s.payment_status !== "paid" || !s.client_reference_id) return null;
  const c = s.customer_details || {};
  if (!c.email) return null;
  return rpc("server_record_order", { p_order: {
    order_ref: s.client_reference_id, stripe_session_id: s.id, email: c.email, customer_name: c.name || null, phone: c.phone || null,
    package: s.metadata?.package || "", items: parseSkus(s.metadata?.sku), amount: (s.amount_total || 0) / 100, currency: s.currency
  } });
}
