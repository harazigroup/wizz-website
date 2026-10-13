// Emails a quote link to the client. Called from the team admin with the signed-in admin's token;
// the database only returns the quote if that user is on the admin list (row-level security).
import { SUPABASE_URL, SUPABASE_ANON } from "./_db.mjs";
import { json } from "./_airwallex.mjs";

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const money = (n, c) => { try { return new Intl.NumberFormat("en-US", { style: "currency", currency: c, currencyDisplay: "code", maximumFractionDigits: 2 }).format(n); } catch { return `${c} ${n}`; } };
const T = {
  en: { s: (r) => `Your quotation from Wizz Smart Services (${r})`, hi: "Hi", p: "Thank you for your interest in Wizz Smart Services. Your quotation is ready. You can review it, download it as a PDF and accept it online:", b: "View your quotation", v: "Valid until", q: "Questions? Reply to this email or message us on WhatsApp at +60 11-2447 7685.", k: "Kind regards,<br>The Wizz team" },
  ar: { s: (r) => `عرض السعر من ويز للخدمات الذكية (${r})`, hi: "مرحباً", p: "شكراً لاهتمامك بويز للخدمات الذكية. عرض السعر جاهز، ويمكنك مراجعته وتنزيله PDF والموافقة عليه عبر الإنترنت:", b: "عرض السعر", v: "صالح حتى", q: "لديك سؤال؟ رد على هذه الرسالة أو راسلنا على واتساب على الرقم ‎+60 11-2447 7685.", k: "مع التحية،<br>فريق ويز" },
  ms: { s: (r) => `Sebut harga anda daripada Wizz Smart Services (${r})`, hi: "Hai", p: "Terima kasih atas minat anda terhadap Wizz Smart Services. Sebut harga anda sudah sedia. Anda boleh menyemaknya, memuat turun sebagai PDF dan menerimanya dalam talian:", b: "Lihat sebut harga anda", v: "Sah sehingga", q: "Ada soalan? Balas e-mel ini atau hantar mesej WhatsApp kepada kami di +60 11-2447 7685.", k: "Salam hormat,<br>Pasukan Wizz" },
};

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!process.env.RESEND_API_KEY) return json(503, { error: "Email is not set up (RESEND_API_KEY)" });
  const auth = req.headers.get("authorization") || "";
  let id = "";
  try { ({ id } = await req.json()); } catch {}
  if (!/^Bearer .{20,}/.test(auth) || !/^[0-9a-f-]{36}$/.test(id || "")) return json(400, { error: "bad request" });
  const r = await fetch(`${SUPABASE_URL}/rest/v1/quotes?id=eq.${id}&select=*`, { headers: { apikey: SUPABASE_ANON, authorization: auth } });
  const rows = r.ok ? await r.json() : [];
  const q = rows[0];
  if (!q) return json(403, { error: "not allowed or quote not found" });
  if (!q.client_email) return json(400, { error: "the lead has no email" });
  if (q.status === "cancelled") return json(400, { error: "quote is cancelled" });
  const t = T[q.lang] || T.en, rtl = q.lang === "ar";
  const url = `https://wizz.com.my/quote.html?t=${q.token}`;
  const first = esc(String(q.client_name || "").split(/\s+/)[0]);
  const html = `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}">
<tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr>
<tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">
<p>${t.hi} ${first},</p><p>${t.p}</p>
<p style="background:#f4f5f7;border-radius:8px;padding:12px 14px;margin:16px 0"><b dir="ltr">${esc(q.ref)}</b> · <b dir="ltr">${esc(money(q.total, q.currency))}</b><br><span style="color:#666;font-size:13px">${t.v} ${esc(q.valid_until)}</span></p>
<p><a href="${url}" style="background:#E01B22;color:#fff;text-decoration:none;padding:12px 18px;border-radius:6px;display:inline-block;font-weight:bold">${t.b}</a></p>
<p>${t.q}</p><p>${t.k}</p></td></tr></table>
<p style="font-size:12px;color:#777;margin:14px 0 0">WIZZ SMART SERVICES SDN. BHD. · Company No. 202501029005 · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p>
</td></tr></table></body></html>`;
  const s = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: FROM, to: [q.client_email], reply_to: TEAM, bcc: [TEAM], subject: t.s(q.ref), html }),
  });
  if (!s.ok) { console.error(await s.text()); return json(502, { error: "email failed" }); }
  return json(200, { ok: true, ref: q.ref, to: q.client_email });
};
