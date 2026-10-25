// B2B partner offices.
// POST { action:"apply", company, name, email, phone, country, city, cr, services, volume, message, lang, company_website }   (public)
//      -> saves a lead (source partner) and emails the team. Wizz adds the office in Admin → Partners after KYC.
// POST { action:"invite", partner_id }      (admin token)   -> emails the office its sign-in instructions
// POST { action:"order_new", order_id }     (partner token) -> emails the team about a new partner order, and the office a copy
// POST { action:"order_update", order_id }  (admin token)   -> emails the office the order's new status (with invoice link when invoiced)
// Tokens are the signed-in user's Supabase access token (Authorization: Bearer ...). Row-level security decides what each one can read.
import { json } from "./_airwallex.mjs";
import { dbOn, rpc, SUPABASE_URL, SUPABASE_ANON } from "./_db.mjs";

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const KEY = () => process.env.RESEND_API_KEY || process.env.resend;
const SITE = () => process.env.SITE_URL || "https://wizz.com.my";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
const str = (v, n = 200) => (typeof v === "string" ? v.trim().slice(0, n) : "");
const money = (n, c) => `${c} ${Number(n).toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;

async function send(body) {
  if (!KEY()) throw new Error("no email key");
  const r = await fetch("https://api.resend.com/emails", { method: "POST", headers: { Authorization: `Bearer ${KEY()}`, "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}
const shell = (inner, rtl) => `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111"><table role="presentation" width="100%"><tr><td align="center"><table role="presentation" width="100%" style="max-width:600px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}"><tr><td style="padding:24px 28px 8px"><img src="https://wizz.com.my/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr><tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.6;text-align:${rtl ? "right" : "left"}">${inner}</td></tr></table><p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. (202501029005) · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p></td></tr></table></body></html>`;
const btn = (href, label) => `<p style="margin:18px 0"><a href="${esc(href)}" style="background:#1F2328;color:#fff;text-decoration:none;padding:11px 18px;border-radius:6px;display:inline-block;font-weight:bold">${label}</a></p>`;
const rows = (pairs) => `<table role="presentation" style="font-size:14px;border-collapse:collapse">${pairs.filter(([, v]) => v).map(([k, v]) => `<tr><td style="padding:5px 14px 5px 0;color:#666;vertical-align:top;white-space:nowrap">${esc(k)}</td><td style="padding:5px 0;white-space:pre-wrap">${esc(v)}</td></tr>`).join("")}</table>`;

// Supabase REST as the signed-in user
const bearer = (req) => (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
async function asUser(token, path, init = {}) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, { ...init, headers: { apikey: SUPABASE_ANON, authorization: `Bearer ${token}`, "content-type": "application/json", ...(init.headers || {}) } });
  const t = await r.text();
  if (!r.ok) throw new Error(`db ${r.status}: ${t.slice(0, 200)}`);
  return t ? JSON.parse(t) : null;
}
const isAdmin = async (token) => { try { return (await asUser(token, "rpc/is_admin", { method: "POST", body: "{}" })) === true; } catch { return false; } };

const ST = {
  submitted: ["Received", "تم الاستلام"], invoiced: ["Invoice issued", "صدرت الفاتورة"], paid: ["Payment received", "تم استلام الدفع"],
  in_progress: ["In progress", "قيد التنفيذ"], completed: ["Completed", "مكتمل"], cancelled: ["Cancelled", "ملغى"],
};
const itemsText = (o) => (o.items || []).map((i) => `${i.qty} × ${i.name_en} (${money(i.unit, o.currency)})`).join("\n");

export default async (req) => {
  if (req.method !== "POST") return json(405, { error: "Use POST" });
  let d = {};
  try { d = await req.json(); } catch {}

  if (d.action === "apply") {
    if (d.company_website) return json(200, { ok: true });
    const lang = ["ar", "ms"].includes(d.lang) ? d.lang : "en";
    const v = { company: str(d.company, 150), name: str(d.name, 120), email: str(d.email).toLowerCase(), phone: str(d.phone, 60), country: str(d.country, 80),
      city: str(d.city, 80), cr: str(d.cr, 60), services: str(d.services, 500), volume: str(d.volume, 40), message: str(d.message, 2000) };
    if (!v.company || !v.name || !emailOk(v.email) || !v.phone || !v.country) return json(400, { error: "missing_fields" });
    let lead = null;
    if (dbOn()) {
      try {
        const [ref] = String(await rpc("server_add_lead", { p_lead: { name: `${v.name} (${v.company})`, email: v.email, phone: v.phone, nat: "", res: v.country, mkt: "B2B partner",
          act: `Partner office: ${v.services || "services"}`.slice(0, 300), services: "B2B partner application", own: "", brand: "",
          msg: [`Company: ${v.company}`, `City: ${v.city}`, `CR: ${v.cr}`, `Clients per month: ${v.volume}`, v.message].filter((x) => !/: $/.test(x)).join("\n"), ref: "", lang } })).split("|");
        lead = ref;
      } catch (e) { console.error("lead save failed", e); }
    }
    try {
      await send({ from: FROM, to: [TEAM], reply_to: v.email, subject: `B2B partner application: ${v.company} (${v.country})`,
        html: shell(`<h2 style="margin:0 0 6px;font-size:19px">New partner office application</h2><p style="color:#555;margin:0 0 14px">${lead ? `Lead <b>${esc(lead)}</b>. ` : ""}Do KYC first (commercial registration, owner's ID, office address). Then add the office in <a href="${SITE()}/admin.html#partners">Admin → Partners</a> and send the invite.</p>${rows([["Company", v.company], ["Contact", v.name], ["Email", v.email], ["WhatsApp", v.phone], ["Country", v.country], ["City", v.city], ["CR number", v.cr], ["Services", v.services], ["Clients per month", v.volume], ["Message", v.message]])}`) });
    } catch (e) { console.error(e); if (!lead) return json(502, { error: "send_failed" }); }
    const ar = lang === "ar";
    try {
      await send({ from: FROM, to: [v.email], reply_to: TEAM, subject: ar ? "استلمنا طلب الشراكة – ويز للخدمات الذكية" : "We've received your partner application – Wizz Smart Services",
        html: shell(ar ? `<p>مرحباً ${esc(v.name.split(/\s+/)[0])}،</p><p>شكراً لاهتمام <b>${esc(v.company)}</b> بالشراكة مع ويز. سيتواصل معك فريقنا خلال يومي عمل لإكمال التحقق (KYC). نحتاج عادةً: السجل التجاري، وهوية المالك أو المدير، وعنوان المكتب.</p><p>بعد التحقق نفتح لك حساب شريك بأسعار المكاتب.</p><p>مع التحية،<br>فريق ويز</p>`
          : `<p>Hi ${esc(v.name.split(/\s+/)[0])},</p><p>Thank you for your interest in partnering with Wizz. Our team will contact you within two business days to complete KYC. We usually need your commercial registration, the owner's or manager's ID, and your office address.</p><p>Once KYC is done, we open your partner account with office prices.</p><p>Kind regards,<br>The Wizz team</p>`, ar) });
    } catch (e) { console.error(e); }
    return json(200, { ok: true });
  }

  const token = bearer(req);
  if (!token) return json(401, { error: "sign_in" });

  if (d.action === "invite") {
    if (!(await isAdmin(token))) return json(403, { error: "admin_only" });
    const [p] = (await asUser(token, `partners?id=eq.${encodeURIComponent(str(d.partner_id, 40))}&select=*`)) || [];
    if (!p) return json(404, { error: "not_found" });
    const link = `${SITE()}/account.html?email=${encodeURIComponent(p.email)}`;
    await send({ from: FROM, to: [p.email], reply_to: TEAM, subject: "Your Wizz partner account is ready | حساب الشريك لدى ويز جاهز",
      html: shell(`<p>Hi ${esc(p.contact_name || p.company)},</p><p>Your partner account for <b>${esc(p.company)}</b> (${esc(p.code)}) is ready. In it you can see your office prices, place orders for each client, upload documents, follow progress and download invoices.</p>
<p><b>To sign in the first time:</b> open the link below, choose <b>Create an account</b> and use this email: <b>${esc(p.email)}</b>. Confirm your email, and you'll go straight to the partner portal.</p>${btn(link, "Open my partner account")}
<hr style="border:0;border-top:1px solid #eee;margin:22px 0"><div dir="rtl" style="text-align:right"><p>مرحباً ${esc(p.contact_name || p.company)}،</p><p>حساب الشريك الخاص بـ <b>${esc(p.company)}</b> (<span dir="ltr">${esc(p.code)}</span>) جاهز. يمكنك من خلاله الاطلاع على أسعار المكاتب، وتقديم الطلبات لكل عميل، ورفع المستندات، ومتابعة الإنجاز، وتنزيل الفواتير.</p><p><b>للدخول أول مرة:</b> افتح الرابط أعلاه، واختر <b>أنشئ حساباً</b> بهذا البريد: <b dir="ltr">${esc(p.email)}</b>، ثم أكّد بريدك وستنتقل مباشرة إلى بوابة الشركاء.</p></div>`) });
    return json(200, { ok: true });
  }

  if (d.action === "order_new" || d.action === "order_update") {
    const admin = d.action === "order_update";
    if (admin && !(await isAdmin(token))) return json(403, { error: "admin_only" });
    const id = encodeURIComponent(str(d.order_id, 40));
    const [o] = (await asUser(token, `partner_orders?id=eq.${id}&select=*,partners(company,code,email,contact_name,phone,country)`)) || [];
    if (!o) return json(404, { error: "not_found" });
    const p = o.partners || {};
    const portal = `${SITE()}/partner.html#${o.ref}`;
    if (!admin) {
      await send({ from: FROM, to: [TEAM], reply_to: p.email, subject: `Partner order ${o.ref}: ${p.company} – ${o.client_name} – ${money(o.total, o.currency)}`,
        html: shell(`<h2 style="margin:0 0 6px;font-size:19px">New partner order</h2><p style="color:#555;margin:0 0 14px">Open it in <a href="${SITE()}/admin.html#partners">Admin → Partners → Orders</a>, then set it to <b>Invoiced</b> to issue the invoice.</p>${rows([["Order", o.ref], ["Partner", `${p.company} (${p.code})`], ["Partner email", p.email], ["Partner phone", p.phone], ["End client", o.client_name], ["Client nationality", o.client_nationality], ["Client country", o.client_country], ["Services", itemsText(o)], ["Total", money(o.total, o.currency)], ["Payment", o.pay_method === "usdt" ? "USDT (TRC-20)" : "Bank transfer"], ["Notes", o.client_notes]])}`) });
      try {
        await send({ from: FROM, to: [p.email], reply_to: TEAM, subject: `Order ${o.ref} received – ${o.client_name} | تم استلام الطلب`,
          html: shell(`<p>We've received order <b>${esc(o.ref)}</b> for <b>${esc(o.client_name)}</b>, total <b>${esc(money(o.total, o.currency))}</b>. We'll issue the invoice shortly. Please upload the client's documents in your portal.</p>${btn(portal, "Open the order")}<p dir="rtl" style="text-align:right">استلمنا الطلب <b dir="ltr">${esc(o.ref)}</b> للعميل <b>${esc(o.client_name)}</b> بإجمالي <b dir="ltr">${esc(money(o.total, o.currency))}</b>. سنصدر الفاتورة قريباً. يرجى رفع مستندات العميل من البوابة.</p>`) });
      } catch (e) { console.error(e); }
      return json(200, { ok: true });
    }
    const [en, ar] = ST[o.status] || [o.status, o.status];
    const inv = o.invoice_no && o.status !== "cancelled" ? `${SITE()}/invoice.html?o=${o.id}` : "";
    const extra = o.status === "invoiced" ? ["Please pay by bank transfer or USDT as shown on the invoice, then send us the payment proof.", "يرجى الدفع بالتحويل البنكي أو USDT كما هو موضح في الفاتورة، ثم إرسال إثبات الدفع."]
      : o.status === "completed" ? ["The client's documents are in your portal.", "مستندات العميل متاحة في البوابة."] : ["", ""];
    await send({ from: FROM, to: [p.email], reply_to: TEAM, subject: `${o.ref} – ${o.client_name}: ${en} | ${ar}`,
      html: shell(`<p>Order <b>${esc(o.ref)}</b> for <b>${esc(o.client_name)}</b>: <b>${esc(en)}</b>.</p>${extra[0] ? `<p>${esc(extra[0])}</p>` : ""}${o.note_to_partner ? `<p style="background:#f6f6f4;padding:10px 12px;border-radius:6px;white-space:pre-wrap">${esc(o.note_to_partner)}</p>` : ""}${inv ? btn(inv, `Invoice ${esc(o.invoice_no)}`) : ""}${btn(portal, "Open the order")}<p dir="rtl" style="text-align:right">الطلب <b dir="ltr">${esc(o.ref)}</b> للعميل <b>${esc(o.client_name)}</b>: <b>${esc(ar)}</b>.${extra[1] ? "<br>" + esc(extra[1]) : ""}</p>`) });
    return json(200, { ok: true });
  }
  return json(400, { error: "unknown_action" });
};
