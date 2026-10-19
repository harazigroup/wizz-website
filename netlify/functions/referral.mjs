// Referral programme.
// GET  ?check=CODE                       -> { valid }           (is this an active code?)
// POST { action:"signup", name, email, phone, country, payout_method, payout_details, lang, company_website }
//                                         -> { ok, code } for a new referrer, or { ok, emailed:true } when the email already has a code
// POST { action:"stats", code, email }    -> { ok, stats }      (only when code and email match)
// Rules: friends get RM 100 off orders of RM 1,000 or more (applied in checkout.mjs); referrers earn 10% of the amount paid,
// approved after the service is completed. Needs WIZZ_DB_SECRET; email needs RESEND_API_KEY (or "resend").
import { json } from "./_airwallex.mjs";
import { dbOn, rpc, SUPABASE_URL, SUPABASE_ANON } from "./_db.mjs";

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const KEY = () => process.env.RESEND_API_KEY || process.env.resend;
const SITE = () => process.env.SITE_URL || "https://wizz.com.my";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
const codeOk = (c) => /^[A-Z0-9]{4,16}$/.test(c);

export async function checkRef(code) {
  const c = String(code || "").trim().toUpperCase();
  if (!codeOk(c)) return null;
  try {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/rpc/public_check_ref`, {
      method: "POST", headers: { apikey: SUPABASE_ANON, authorization: `Bearer ${SUPABASE_ANON}`, "content-type": "application/json" },
      body: JSON.stringify({ p_code: c })
    });
    return r.ok && (await r.json()) === true ? c : null;
  } catch { return null; }
}

async function send(body) {
  if (!KEY()) return;
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST", headers: { Authorization: `Bearer ${KEY()}`, "Content-Type": "application/json" }, body: JSON.stringify(body)
  });
  if (!r.ok) console.error("referral email failed", r.status, await r.text());
}

const TXT = {
  en: { s: "Your Wizz referral code", hi: "Hi", body: (c, l) => `<p>Welcome to the Wizz referral programme. Your code is:</p><p style="font:700 26px monospace;letter-spacing:2px;margin:8px 0">${c}</p><p>Share your link: <a href="${l}">${l}</a></p><p>Your friends get <b>RM 100 off</b> orders of RM 1,000 or more. You earn <b>10% of what they pay</b>, paid after their service is completed.</p><p>Check your referrals any time at <a href="${SITE()}/refer.html#check">${SITE()}/refer.html</a> with your code and this email.</p>` },
  ar: { s: "رمز الإحالة الخاص بك من ويز", hi: "مرحباً", body: (c, l) => `<p>أهلاً بك في برنامج الإحالة من ويز. رمزك هو:</p><p style="font:700 26px monospace;letter-spacing:2px;margin:8px 0" dir="ltr">${c}</p><p>شارك رابطك: <a href="${l}">${l}</a></p><p>يحصل أصدقاؤك على <b>خصم 100 رينغيت</b> على الطلبات من 1,000 رينغيت فأكثر، وتحصل أنت على <b>10% مما يدفعونه</b>، تُصرف بعد إتمام الخدمة.</p><p>تابع إحالاتك في أي وقت عبر <a href="${SITE()}/ar/refer.html#check">${SITE()}/ar/refer.html</a> برمزك وهذا البريد.</p>` },
  ms: { s: "Kod rujukan Wizz anda", hi: "Hai", body: (c, l) => `<p>Selamat datang ke program rujukan Wizz. Kod anda ialah:</p><p style="font:700 26px monospace;letter-spacing:2px;margin:8px 0">${c}</p><p>Kongsi pautan anda: <a href="${l}">${l}</a></p><p>Rakan anda mendapat <b>RM 100 diskaun</b> untuk pesanan RM 1,000 ke atas. Anda memperoleh <b>10% daripada jumlah yang mereka bayar</b>, dibayar selepas perkhidmatan mereka selesai.</p><p>Semak rujukan anda bila-bila masa di <a href="${SITE()}/ms/refer.html#check">${SITE()}/ms/refer.html</a> dengan kod dan e-mel ini.</p>` },
};
const shell = (inner, rtl) => `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111"><table role="presentation" width="100%"><tr><td align="center"><table role="presentation" width="100%" style="max-width:560px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}"><tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr><tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">${inner}</td></tr></table><p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p></td></tr></table></body></html>`;

export default async (req) => {
  const url = new URL(req.url);
  if (req.method === "GET") {
    const c = await checkRef(url.searchParams.get("check"));
    return json(200, { valid: Boolean(c), code: c || undefined });
  }
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!dbOn()) return json(503, { error: "not_configured" });
  let d = {};
  try { d = await req.json(); } catch {}
  const s = (k, n = 200) => (typeof d[k] === "string" ? d[k].trim().slice(0, n) : "");

  if (d.action === "stats") {
    const code = s("code", 16).toUpperCase(), email = s("email").toLowerCase();
    if (!codeOk(code) || !emailOk(email)) return json(400, { error: "missing_fields" });
    try {
      const stats = await rpc("server_referral_stats", { p_code: code, p_email: email });
      return stats ? json(200, { ok: true, stats }) : json(404, { error: "not_found" });
    } catch (e) { console.error(e); return json(502, { error: "unavailable" }); }
  }

  if (d.action === "signup") {
    if (d.company_website) return json(200, { ok: true }); // spam trap
    const lang = ["ar", "ms"].includes(d.lang) ? d.lang : "en";
    const v = { name: s("name", 120), email: s("email").toLowerCase(), phone: s("phone", 60), country: s("country", 80),
                payout_method: s("payout_method", 40), payout_details: s("payout_details", 300), lang };
    if (!v.name || !emailOk(v.email)) return json(400, { error: "missing_fields" });
    let res;
    try { res = String(await rpc("server_referral_signup", { p_data: v })); } catch (e) { console.error(e); return json(502, { error: "unavailable" }); }
    const [state, code] = res.split("|");
    const link = `${SITE()}/?ref=${code}`;
    const t = TXT[lang];
    try {
      await send({ from: FROM, to: [v.email], reply_to: TEAM, subject: `${t.s}: ${code}`, html: shell(`<p>${t.hi} ${esc(v.name.split(/\s+/)[0])},</p>${t.body(code, link)}`, lang === "ar") });
      if (state === "new") await send({ from: FROM, to: [TEAM], reply_to: v.email, subject: `New referrer: ${v.name} (${code})`,
        html: shell(`<p><b>${esc(v.name)}</b> joined the referral programme.</p><p>Code: <b>${code}</b><br>Email: ${esc(v.email)}<br>Phone: ${esc(v.phone || "–")}<br>Country: ${esc(v.country || "–")}<br>Payout: ${esc(v.payout_method || "–")} ${esc(v.payout_details || "")}</p><p>See all referrers in <a href="${SITE()}/admin.html#referrals">Admin → Referrals</a>.</p>`) });
    } catch (e) { console.error(e); }
    return state === "new" ? json(200, { ok: true, code, link }) : json(200, { ok: true, emailed: true });
  }
  return json(400, { error: "unknown_action" });
};
