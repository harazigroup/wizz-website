// POST from careers.html: a job application with the CV attached.
// { role, name, email, phone, country, setup, languages, link, message, lang, company_website, cv:{name, type, data(base64)} }
// Emails the team with the CV attached, saves the application (without the file) for Admin → Careers, and confirms to the applicant.
// Needs RESEND_API_KEY (or "resend"); saving needs WIZZ_DB_SECRET and supabase/migrations/20261024_job_applications.sql.
import { json } from "./_airwallex.mjs";
import { dbOn, rpc } from "./_db.mjs";

const TEAM = process.env.CAREERS_TO || process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const KEY = () => process.env.RESEND_API_KEY || process.env.resend;
const MAX = 4 * 1024 * 1024;
const TYPES = { pdf: "application/pdf", doc: "application/msword", docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
const str = (v, n = 200) => (typeof v === "string" ? v.trim().slice(0, n) : "");

async function send(body) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST", headers: { Authorization: `Bearer ${KEY()}`, "Content-Type": "application/json" }, body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}
const shell = (inner, rtl) => `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111"><table role="presentation" width="100%"><tr><td align="center"><table role="presentation" width="100%" style="max-width:560px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}"><tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr><tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">${inner}</td></tr></table><p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. (202501029005) · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p></td></tr></table></body></html>`;

const TXT = {
  en: { s: "We've received your application – Wizz Smart Services", b: (n, r) => `<p>Hi ${n},</p><p>Thank you for applying for <b>${r}</b> at Wizz Smart Services. We review every application. If your profile fits the role, we'll contact you within two weeks to arrange a short call.</p><p>Kind regards,<br>The Wizz team</p>` },
  ar: { s: "استلمنا طلبك – ويز للخدمات الذكية", b: (n, r) => `<p>مرحباً ${n}،</p><p>شكراً لتقديمك على وظيفة <b>${r}</b> في ويز للخدمات الذكية. نراجع كل الطلبات، وإن كان ملفك مناسباً للوظيفة سنتواصل معك خلال أسبوعين لترتيب مكالمة قصيرة.</p><p>مع التحية،<br>فريق ويز</p>` },
  ms: { s: "Kami telah menerima permohonan anda – Wizz Smart Services", b: (n, r) => `<p>Hai ${n},</p><p>Terima kasih kerana memohon jawatan <b>${r}</b> di Wizz Smart Services. Kami menyemak setiap permohonan. Jika profil anda sesuai, kami akan menghubungi anda dalam masa dua minggu untuk mengatur panggilan ringkas.</p><p>Salam hormat,<br>Pasukan Wizz</p>` },
};

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  let d = {};
  try { d = await req.json(); } catch { return json(400, { error: "bad_request" }); }
  if (d.company_website) return json(200, { ok: true }); // spam trap
  const lang = ["ar", "ms"].includes(d.lang) ? d.lang : "en";
  const v = { role: str(d.role, 80), name: str(d.name, 120), email: str(d.email).toLowerCase(), phone: str(d.phone, 60), country: str(d.country, 80),
    setup: str(d.setup, 60), languages: str(d.languages, 200), link: str(d.link, 300), message: str(d.message, 3000), lang };
  if (!v.role || !v.name || !emailOk(v.email) || !v.phone) return json(400, { error: "missing_fields" });
  const cv = d.cv || {};
  const ext = String(cv.name || "").toLowerCase().split(".").pop();
  const data = typeof cv.data === "string" ? cv.data.replace(/^data:[^,]*,/, "") : "";
  const size = Math.floor(data.length * 3 / 4);
  if (!TYPES[ext] || !data || size > MAX) return json(400, { error: "bad_cv" });
  const cvName = `CV - ${v.name.replace(/[^\p{L}\p{N} .-]/gu, "").slice(0, 60)}.${ext}`;
  v.cv_name = cvName;

  let ref = null;
  if (dbOn()) { try { ref = String(await rpc("server_add_application", { p_data: v })); } catch (e) { console.error("application save failed", e); } }
  if (!KEY()) return ref ? json(200, { ok: true, ref }) : json(503, { error: "not_configured" });

  const rows = [["Role", v.role], ["Name", v.name], ["Email", v.email], ["WhatsApp / phone", v.phone], ["State / city", v.country], ["Malaysian citizen", d.citizen ? "Yes (confirmed)" : ""], ["Setup", v.setup],
    ["Languages", v.languages], ["LinkedIn / portfolio", v.link], ["Message", v.message], ["Site language", lang]]
    .filter(([, x]) => x).map(([k, x]) => `<tr><td style="padding:5px 14px 5px 0;color:#666;vertical-align:top;white-space:nowrap">${k}</td><td style="padding:5px 0;white-space:pre-wrap">${esc(x)}</td></tr>`).join("");
  const wa = `https://wa.me/${v.phone.replace(/[^0-9]/g, "")}`;
  try {
    await send({ from: FROM, to: [TEAM], reply_to: v.email, subject: `Job application: ${v.role} – ${v.name}`,
      attachments: [{ filename: cvName, content: data }],
      html: shell(`<h2 style="margin:0 0 6px;font-size:19px">New job application</h2><p style="margin:0 0 14px;color:#555">${ref ? `Ref <b>${esc(ref)}</b> · saved in <a href="https://wizz.com.my/admin.html#careers">Admin → Careers</a>. ` : ""}CV attached. Reply to this email to answer ${esc(v.name)}.</p><table role="presentation" style="font-size:14px;border-collapse:collapse">${rows}</table><p style="margin:18px 0 0"><a href="${esc(wa)}" style="background:#25d366;color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;display:inline-block;font-weight:bold">Open WhatsApp chat</a></p>`) });
  } catch (e) {
    console.error(e);
    if (!ref) return json(502, { error: "send_failed" });
  }
  try { await send({ from: FROM, to: [v.email], reply_to: TEAM, subject: TXT[lang].s, html: shell(TXT[lang].b(esc(v.name.split(/\s+/)[0]), esc(v.role)), lang === "ar") }); }
  catch (e) { console.error("applicant copy failed", e); }
  return json(200, ref ? { ok: true, ref } : { ok: true });
};
