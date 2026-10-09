// POST { name, email, phone, nat, res, mkt, act, services, own, brand, msg, lang, company_website }
// Emails the enquiry to the Wizz team and sends the client a short confirmation, through Resend.
// Needs RESEND_API_KEY (a Resend key with sending access for wizz.com.my).
import { json } from "./_airwallex.mjs";

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const FIELDS = [
  ["name", "Name"], ["email", "Email"], ["phone", "WhatsApp / phone"], ["nat", "Nationality"],
  ["res", "Country of residence"], ["mkt", "Target country"], ["act", "Business activity"],
  ["services", "Services"], ["own", "Owners"], ["brand", "Selling online"], ["msg", "Notes"], ["lang", "Site language"],
];
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

async function send(body) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
  return r.json();
}

function shell(inner, rtl) {
  return `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}">
<tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr>
<tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">${inner}</td></tr>
</table>
<p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p>
</td></tr></table></body></html>`;
}

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  if (!process.env.RESEND_API_KEY) return json(503, { error: "not_configured" });
  let d = {};
  try { d = await req.json(); } catch {}
  if (d.company_website) return json(200, { ok: true }); // spam trap
  const v = {};
  for (const [k] of FIELDS) v[k] = typeof d[k] === "string" ? d[k].trim().slice(0, k === "msg" ? 4000 : 300) : "";
  if (!v.name || !emailOk(v.email) || !v.act) return json(400, { error: "missing_fields" });

  const rows = FIELDS.filter(([k]) => v[k]).map(([k, label]) =>
    `<tr><td style="padding:6px 12px 6px 0;color:#666;vertical-align:top;white-space:nowrap">${label}</td><td style="padding:6px 0;white-space:pre-wrap">${esc(v[k])}</td></tr>`).join("");
  const wa = v.phone ? `https://wa.me/${v.phone.replace(/[^0-9]/g, "")}` : "";
  const teamHtml = shell(`<h2 style="margin:0 0 6px;font-size:19px">New website enquiry</h2>
<p style="margin:0 0 16px;color:#555">Reply to this email to answer ${esc(v.name)} directly.</p>
<table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14px;border-collapse:collapse">${rows}</table>
${wa ? `<p style="margin:18px 0 0"><a href="${esc(wa)}" style="background:#25d366;color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;display:inline-block;font-weight:bold">Open WhatsApp chat</a></p>` : ""}`);
  const text = FIELDS.filter(([k]) => v[k]).map(([k, label]) => `${label}: ${v[k]}`).join("\n");

  const ar = v.lang === "ar";
  const first = esc(v.name.split(/\s+/)[0]);
  const clientHtml = ar
    ? shell(`<p>مرحباً ${first}،</p><p>شكراً لتواصلك مع ويز للخدمات الذكية. استلمنا استفسارك بخصوص <b>${esc(v.mkt || "مشروعك")}</b>، وسيراجعه فريقنا ويرد عليك بتوصية والخطوات التالية، عادةً خلال يوم عمل واحد.</p><p>إن أردت إضافة أي تفاصيل، يمكنك الرد على هذه الرسالة مباشرة.</p><p>مع التحية،<br>فريق ويز</p>`, true)
    : shell(`<p>Hi ${first},</p><p>Thank you for contacting Wizz Smart Services. We've received your enquiry about <b>${esc(v.mkt || "your business")}</b>. Our team will review it and reply with a recommendation and next steps, usually within one business day.</p><p>If you'd like to add anything, just reply to this email.</p><p>Kind regards,<br>The Wizz team</p>`);

  try {
    await send({
      from: FROM, to: [TEAM], reply_to: v.email,
      subject: `Website enquiry: ${v.name}${v.mkt ? ` (${v.mkt})` : ""}`,
      html: teamHtml, text,
    });
  } catch (e) {
    console.error(e);
    return json(502, { error: "send_failed" });
  }
  try {
    await send({
      from: FROM, to: [v.email], reply_to: TEAM,
      subject: ar ? "استلمنا استفسارك – ويز للخدمات الذكية" : "We've received your enquiry – Wizz Smart Services",
      html: clientHtml,
    });
  } catch (e) { console.error("auto-reply failed", e); }
  return json(200, { ok: true });
};
