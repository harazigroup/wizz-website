// GET -> { ok, items: [[code, desc_en, desc_bm], ...] }
// The 5-digit MSIC 2008 business activity codes that SSM uses, from the official DOSM dictionary
// (https://open.dosm.gov.my/data-catalogue/msic). Cached in memory and on Netlify's CDN for a week.
const SRC = "https://storage.dosm.gov.my/dictionaries/msic.csv";
let cache = null;

function parseCsv(text) {
  const rows = []; let row = [], f = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; }
      else f += c;
    } else if (c === '"') q = true;
    else if (c === ",") { row.push(f); f = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(f); rows.push(row); row = []; f = "";
    } else f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  return rows;
}

async function load() {
  if (cache) return cache;
  const r = await fetch(SRC, { headers: { "user-agent": "wizz.com.my MSIC lookup" } });
  if (!r.ok) throw new Error(`DOSM ${r.status}`);
  const rows = parseCsv((await r.text()).replace(/^﻿/, ""));
  const h = rows.shift().map((x) => x.trim().toLowerCase());
  const at = (k) => h.indexOf(k);
  const iD = at("digits"), iEn = at("desc_en"), iBm = at("desc_bm");
  const codeCols = ["item", "class", "group", "division"].map(at).filter((i) => i >= 0);
  const seen = new Set(), items = [];
  for (const r of rows) {
    if (!r || r.length < h.length - 1) continue;
    let code = "";
    for (const i of codeCols) { const v = (r[i] || "").trim(); if (/^\d{5}$/.test(v)) { code = v; break; } }
    if (!code || (iD >= 0 && String(r[iD]).trim() !== "5") || seen.has(code)) continue;
    seen.add(code);
    items.push([code, (r[iEn] || "").replace(/\s+/g, " ").trim(), (r[iBm] || "").replace(/\s+/g, " ").trim()]);
  }
  if (items.length < 200) throw new Error(`MSIC parse gave ${items.length} codes`);
  items.sort((a, b) => a[0].localeCompare(b[0]));
  cache = items;
  return items;
}

export default async () => {
  try {
    const items = await load();
    return new Response(JSON.stringify({ ok: true, items }), { status: 200, headers: {
      "content-type": "application/json", "cache-control": "public, max-age=86400",
      "netlify-cdn-cache-control": "public, max-age=604800, stale-while-revalidate=604800, durable" } });
  } catch (e) {
    console.error(e);
    return new Response(JSON.stringify({ ok: false }), { status: 502, headers: { "content-type": "application/json", "cache-control": "no-store" } });
  }
};
