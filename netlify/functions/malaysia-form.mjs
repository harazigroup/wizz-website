// POST from malaysia-company-form.html: a client's details for a Malaysian Sdn. Bhd.
// { name, email, phone, country, names:[3], activities:[{code,desc}], business, capital, budget,
//   partners:[{name, nat, passport, dob, share, address, residency}], notes, ref, lang, company_website }
// Emails the full details to the team, sends the client a confirmation, and saves a lead (without passport numbers or dates of birth).
// Needs RESEND_API_KEY (or "resend"); the lead needs WIZZ_DB_SECRET.
import { json } from "./_airwallex.mjs";
import { dbOn, rpc } from "./_db.mjs";

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const KEY = () => process.env.RESEND_API_KEY || process.env.resend;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
const str = (v, n = 200) => (typeof v === "string" ? v.trim().slice(0, n) : "");
const SUFFIX = " SDN. BHD.";
const coName = (n) => n.toUpperCase().replace(/\s*\b(SDN\.?\s*BHD\.?|SENDIRIAN\s+BERHAD)\s*$/i, "").trim() + SUFFIX;

async function send(body) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST", headers: { Authorization: `Bearer ${KEY()}`, "Content-Type": "application/json" }, body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}
const shell = (inner, rtl) => `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111"><table role="presentation" width="100%"><tr><td align="center"><table role="presentation" width="100%" style="max-width:600px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}"><tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr><tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">${inner}</td></tr></table><p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. (202501029005) · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p></td></tr></table></body></html>`;
const row = (k, v) => v ? `<tr><td style="padding:5px 14px 5px 0;color:#666;vertical-align:top;white-space:nowrap">${esc(k)}</td><td style="padding:5px 0;white-space:pre-wrap">${esc(v)}</td></tr>` : "";
const table = (rows) => `<table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14px;border-collapse:collapse;margin:0 0 14px">${rows}</table>`;
const h3 = (t) => `<h3 style="font-size:15px;margin:20px 0 6px;border-bottom:1px solid #eee;padding-bottom:4px">${esc(t)}</h3>`;

const TXT = {
  en: { s: "We've received your Malaysia company details – Wizz Smart Services", hi: "Hi", p: "Thank you. We've received your details for your Malaysian company. Our team will check your proposed names with SSM and reply with your quote and the documents we need, usually within one business day.", names: "Your proposed names", acts: "Activities", ref: "Your reference", end: "If anything needs changing, just reply to this email.<br><br>Kind regards,<br>The Wizz team" },
  ar: { s: "استلمنا بيانات شركتك في ماليزيا – ويز للخدمات الذكية", hi: "مرحباً", p: "شكراً لك. استلمنا بيانات شركتك في ماليزيا. سيتحقق فريقنا من الأسماء المقترحة لدى هيئة الشركات الماليزية (SSM) ويرد عليك بعرض السعر والمستندات المطلوبة، عادةً خلال يوم عمل واحد.", names: "الأسماء المقترحة", acts: "الأنشطة", ref: "رقم المرجع", end: "إن احتجت إلى تعديل أي شيء، يمكنك الرد على هذه الرسالة مباشرة.<br><br>مع التحية،<br>فريق ويز" },
  ms: { s: "Kami telah menerima butiran syarikat Malaysia anda – Wizz Smart Services", hi: "Hai", p: "Terima kasih. Kami telah menerima butiran untuk syarikat Malaysia anda. Pasukan kami akan menyemak nama yang dicadangkan dengan SSM dan membalas dengan sebut harga serta dokumen yang diperlukan, biasanya dalam satu hari bekerja.", names: "Nama yang dicadangkan", acts: "Aktiviti", ref: "Rujukan anda", end: "Jika ada apa-apa yang perlu diubah, balas sahaja e-mel ini.<br><br>Salam hormat,<br>Pasukan Wizz" },
};

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  let d = {};
  try { d = await req.json(); } catch {}
  if (d.company_website) return json(200, { ok: true }); // spam trap
  const lang = ["ar", "ms"].includes(d.lang) ? d.lang : "en";
  const v = { name: str(d.name, 120), email: str(d.email).toLowerCase(), phone: str(d.phone, 60), country: str(d.country, 80),
    business: str(d.business, 1000), capital: str(d.capital, 60), budget: str(d.budget, 120), notes: str(d.notes, 3000),
    ref: str(d.ref, 16).toUpperCase().replace(/[^A-Z0-9]/g, "") };
  const names = (Array.isArray(d.names) ? d.names : []).map((x) => str(x, 120)).filter(Boolean).slice(0, 3).map(coName);
  const acts = (Array.isArray(d.activities) ? d.activities : []).slice(0, 3)
    .map((a) => ({ code: str(a?.code, 5).replace(/\D/g, ""), desc: str(a?.desc, 300) })).filter((a) => /^\d{5}$/.test(a.code));
  const partners = (Array.isArray(d.partners) ? d.partners : []).slice(0, 6).map((p) => ({
    name: str(p?.name, 150), nat: str(p?.nat, 80), passport: str(p?.passport, 40), dob: str(p?.dob, 10),
    share: str(String(p?.share ?? ""), 6), address: str(p?.address, 400), residency: str(p?.residency, 80) }));
  if (!v.name || !emailOk(v.email) || !v.phone || !names.length || (!acts.length && !v.business) ||
      !partners.length || partners.some((p) => !p.name || !p.passport || !p.dob || !p.nat))
    return json(400, { error: "missing_fields" });

  const actLine = acts.map((a) => `${a.code} ${a.desc}`).join("; ");
  // 1) lead in the database (no passport numbers or dates of birth there)
  let lead = null;
  if (dbOn()) {
    const summary = [`Malaysia company form`, `Names: ${names.join(" / ")}`, acts.length ? `MSIC: ${actLine}` : "",
      v.business ? `Business: ${v.business}` : "", `Capital: ${v.capital || "–"}`, v.budget ? `Budget: ${v.budget}` : "",
      `Shareholders: ${partners.map((p) => `${p.name} (${p.nat}${p.share ? ", " + p.share + "%" : ""}${p.residency ? ", " + p.residency : ""})`).join("; ")}`,
      v.notes ? `Notes: ${v.notes}` : ""].filter(Boolean).join("\n");
    try {
      const [ref, priority, score] = String(await rpc("server_add_lead", { p_lead: {
        name: v.name, email: v.email, phone: v.phone, nat: partners[0].nat, res: v.country, mkt: "Malaysia",
        act: (actLine || v.business).slice(0, 300), services: "Company formation (Malaysia Sdn. Bhd. form)",
        own: partners.length > 1 ? `${partners.length} partners` : "Single owner", brand: "", msg: summary.slice(0, 4000), ref: v.ref, lang } })).split("|");
      lead = { ref, priority, score };
    } catch (e) { console.error("lead save failed", e); }
  }
  if (!KEY()) return lead ? json(200, { ok: true, ref: lead.ref }) : json(503, { error: "not_configured" });

  // 2) full details to the team
  const pHtml = partners.map((p, i) => h3(`Shareholder ${i + 1}`) + table(
    row("Name (passport)", p.name) + row("Nationality", p.nat) + row("Passport no.", p.passport) + row("Date of birth", p.dob) +
    row("Share", p.share ? p.share + "%" : "") + row("Residential address", p.address) + row("Malaysian residency", p.residency))).join("");
  const total = partners.reduce((t, p) => t + (parseFloat(p.share) || 0), 0);
  const wa = `https://wa.me/${v.phone.replace(/[^0-9]/g, "")}`;
  const teamHtml = shell(`<h2 style="margin:0 0 6px;font-size:19px">Malaysia company form: ${esc(v.name)}</h2>
<p style="margin:0 0 10px;color:#555">${lead ? `Lead <b>${esc(lead.ref)}</b> saved in <a href="https://wizz.com.my/admin.html#leads">Leads</a>. ` : ""}Reply to this email to answer the client.</p>
${h3("Contact")}${table(row("Name", v.name) + row("Email", v.email) + row("WhatsApp", v.phone) + row("Country of residence", v.country) + row("Referral code", v.ref) + row("Language", lang))}
${h3("Proposed names (in order)")}${table(names.map((n, i) => row(`${i + 1}`, n)).join(""))}
${h3("Activities (MSIC)")}${table(acts.map((a) => row(a.code, a.desc)).join("") + row("Description", v.business))}
${h3("Capital and budget")}${table(row("Paid-up capital", v.capital) + row("Setup budget", v.budget))}
${pHtml}
${partners.length > 1 && Math.abs(total - 100) > 0.01 ? `<p style="color:#b00"><b>Shares add up to ${total}%, not 100%.</b></p>` : ""}
${v.notes ? h3("Notes") + `<p style="white-space:pre-wrap">${esc(v.notes)}</p>` : ""}
<p style="margin:18px 0 0"><a href="${esc(wa)}" style="background:#25d366;color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;display:inline-block;font-weight:bold">Open WhatsApp chat</a></p>`);
  try {
    await send({ from: FROM, to: [TEAM], reply_to: v.email, subject: `🇲🇾 Malaysia company form: ${v.name} · ${names[0]}`, html: teamHtml });
  } catch (e) {
    console.error(e);
    if (!lead) return json(502, { error: "send_failed" });
  }
  // 3) confirmation to the client (no passport numbers)
  const t = TXT[lang];
  try {
    await send({ from: FROM, to: [v.email], reply_to: TEAM, subject: t.s, html: shell(`<p>${t.hi} ${esc(v.name.split(/\s+/)[0])},</p><p>${t.p}</p>
<p><b>${t.names}</b><br><span dir="ltr">${names.map(esc).join("<br>")}</span></p>
${acts.length ? `<p><b>${t.acts}</b><br><span dir="ltr">${acts.map((a) => esc(a.code + " " + a.desc)).join("<br>")}</span></p>` : ""}
${lead ? `<p>${t.ref}: <b dir="ltr">${esc(lead.ref)}</b></p>` : ""}<p>${t.end}</p>`, lang === "ar") });
  } catch (e) { console.error("client copy failed", e); }
  return json(200, lead ? { ok: true, ref: lead.ref } : { ok: true });
};
