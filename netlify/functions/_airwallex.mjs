// Shared Airwallex helpers. Keys live in Netlify environment variables, never in the browser.
import catalog from "./catalog.json" with { type: "json" };

const ENV = (process.env.AIRWALLEX_ENV || "demo").toLowerCase() === "prod" ? "prod" : "demo";
const BASE = process.env.AIRWALLEX_API_BASE || (ENV === "prod" ? "https://api.airwallex.com" : "https://api.sandbox.airwallex.com");
let cached = { token: null, exp: 0 };

export const env = ENV;
export const products = catalog;

export function json(status, body) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}

export function configured() {
  return Boolean(process.env.AIRWALLEX_CLIENT_ID && process.env.AIRWALLEX_API_KEY);
}

async function token() {
  if (cached.token && Date.now() < cached.exp) return cached.token;
  const r = await fetch(`${BASE}/api/v1/authentication/login`, {
    method: "POST",
    headers: { "content-type": "application/json", "x-client-id": process.env.AIRWALLEX_CLIENT_ID, "x-api-key": process.env.AIRWALLEX_API_KEY },
    body: "{}"
  });
  if (!r.ok) throw new Error(`Airwallex login failed (${r.status})`);
  const d = await r.json();
  cached = { token: d.token, exp: Date.now() + 25 * 60 * 1000 }; // tokens last 30 min
  return d.token;
}

export async function api(path, { method = "GET", body } = {}) {
  const t = await token();
  const r = await fetch(`${BASE}${path}`, {
    method,
    headers: { "content-type": "application/json", authorization: `Bearer ${t}` },
    body: body ? JSON.stringify(body) : undefined
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`Airwallex ${path} failed (${r.status}): ${d.message || d.code || "unknown error"}`);
  return d;
}
