// Daily lead automation, 09:00 Malaysia time (01:00 UTC).
// 1) Emails the team a digest: new leads, leads nobody has contacted, follow-ups due today.
// 2) Emails clients a polite follow-up 3 and 7 days after a quote, unless the lead is won/lost or opted out.
// Needs WIZZ_DB_SECRET and RESEND_API_KEY.
import { createHmac } from "node:crypto";
import { dbOn, rpc } from "./_db.mjs";

export const config = { schedule: "0 1 * * *" };

const TEAM = process.env.CONTACT_TO || "info@wizz.com.my";
const FROM = process.env.CONTACT_FROM || "Wizz Smart Services <info@wizz.com.my>";
const SITE = "https://wizz.com.my";
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export const unsubToken = (ref) => createHmac("sha256", process.env.WIZZ_DB_SECRET || "").update("unsub:" + ref).digest("hex").slice(0, 24);

async function send(body) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${(process.env.RESEND_API_KEY || process.env.resend)}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}

function shell(inner, rtl, foot = "") {
  return `<!doctype html><html><body style="margin:0;background:#f4f4f2;padding:24px 12px;font-family:Arial,Helvetica,sans-serif;color:#111">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:10px;border:1px solid #e5e5e0" dir="${rtl ? "rtl" : "ltr"}">
<tr><td style="padding:24px 28px 8px"><img src="${SITE}/img/email-logo.png" alt="Wizz" height="32" style="display:block;height:32px"></td></tr>
<tr><td style="padding:8px 28px 28px;font-size:15px;line-height:1.55;text-align:${rtl ? "right" : "left"}">${inner}</td></tr>
</table>
<p style="font-size:12px;color:#777;margin:14px 0 0">Wizz Smart Services Sdn. Bhd. · B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia${foot}</p>
</td></tr></table></body></html>`;
}

const row = (l, extra = "") => `<tr><td style="padding:8px 0;border-top:1px solid #eee;vertical-align:top">
  <b>${esc(l.name)}</b> <span style="font-size:12px;color:#fff;background:${l.priority === "hot" ? "#E01B22" : l.priority === "warm" ? "#d08a1c" : "#999"};border-radius:99px;padding:2px 8px">${esc(l.priority)}</span><br>
  <span style="color:#555;font-size:13px">${esc([l.market, l.activity].filter(Boolean).join(" · "))}</span><br>
  <span style="color:#888;font-size:12px">${esc(l.ref)} · ${esc(l.source)}${l.phone ? ` · <a href="https://wa.me/${esc(String(l.phone).replace(/\D/g, ""))}">${esc(l.phone)}</a>` : ""}${extra}</span></td></tr>`;

function digest(q) {
  const block = (title, list, extra) => list.length ? `<h3 style="margin:22px 0 4px;font-size:16px">${title} (${list.length})</h3><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${list.slice(0, 25).map((l) => row(l, extra ? extra(l) : "")).join("")}</table>` : "";
  return shell(`<h2 style="margin:0 0 4px;font-size:20px">Leads today</h2>
<p style="margin:0;color:#555">${q.new_24h.length} new · ${q.untouched.length} not contacted yet · ${q.due.length} follow-ups due</p>
${block("Not contacted for over 24 hours", q.untouched)}
${block("Follow-ups due", q.due, (l) => ` · ${esc(l.status)}${l.assigned_to ? " · " + esc(l.assigned_to) : ""}`)}
${block("New in the last 24 hours", q.new_24h)}
<p style="margin:24px 0 0"><a href="${SITE}/admin.html#leads" style="background:#E01B22;color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;display:inline-block;font-weight:bold">Open Leads</a></p>`);
}

const CHASE = {
  en: [
    { s: "Any questions about your Wizz quotation?", b: (n) => `<p>Hi ${n},</p><p>We sent your quotation a few days ago and wanted to check whether you have any questions. We're happy to explain any step, adjust the package, or arrange a short call.</p><p>Just reply to this email or message us on WhatsApp at +60 11-2447 7685.</p><p>Kind regards,<br>The Wizz team</p>` },
    { s: "Should we keep your quotation open?", b: (n) => `<p>Hi ${n},</p><p>A quick last check on your quotation. If the timing isn't right, no problem: reply "later" and we'll get back to you when you're ready, or reply with any question and we'll answer the same day.</p><p>Kind regards,<br>The Wizz team</p>` },
  ],
  ar: [
    { s: "هل لديك أسئلة عن عرض السعر من ويز؟", b: (n) => `<p>مرحباً ${n}،</p><p>أرسلنا لك عرض السعر قبل أيام ونود التأكد إن كان لديك أي سؤال. يسعدنا شرح أي خطوة أو تعديل الباقة أو ترتيب مكالمة قصيرة.</p><p>رد على هذه الرسالة أو راسلنا على واتساب على الرقم ‎+60 11-2447 7685.</p><p>مع التحية،<br>فريق ويز</p>` },
    { s: "هل نُبقي عرض السعر مفتوحاً؟", b: (n) => `<p>مرحباً ${n}،</p><p>متابعة أخيرة بخصوص عرض السعر. إذا لم يكن الوقت مناسباً فلا مشكلة: رد بكلمة "لاحقاً" وسنتواصل معك عندما تكون جاهزاً، أو أرسل أي سؤال وسنرد في نفس اليوم.</p><p>مع التحية،<br>فريق ويز</p>` },
  ],
  ms: [
    { s: "Ada soalan tentang sebut harga Wizz anda?", b: (n) => `<p>Hai ${n},</p><p>Kami telah menghantar sebut harga anda beberapa hari lalu dan ingin memastikan sama ada anda mempunyai sebarang soalan. Kami sedia menerangkan mana-mana langkah, menyesuaikan pakej, atau mengatur panggilan ringkas.</p><p>Balas sahaja e-mel ini atau hantar mesej WhatsApp kepada kami di +60 11-2447 7685.</p><p>Salam hormat,<br>Pasukan Wizz</p>` },
    { s: "Perlukah kami simpan sebut harga anda?", b: (n) => `<p>Hai ${n},</p><p>Semakan terakhir tentang sebut harga anda. Jika masanya belum sesuai, tiada masalah: balas "nanti" dan kami akan menghubungi anda apabila anda bersedia, atau hantar sebarang soalan dan kami akan menjawab pada hari yang sama.</p><p>Salam hormat,<br>Pasukan Wizz</p>` },
  ],
};
const UNSUB = { en: "Don't want these emails?", ar: "لا تريد هذه الرسائل؟", ms: "Tidak mahu e-mel ini?" };

export default async () => {
  if (!dbOn() || !(process.env.RESEND_API_KEY || process.env.resend)) { console.log("followup: not configured"); return new Response("not configured", { status: 503 }); }
  const q = await rpc("server_followup_queue", {});
  let sent = 0;
  for (const l of q.quote_chasers || []) {
    const lang = CHASE[l.lang] ? l.lang : "en";
    const step = l.follow_up_step || 0;
    const t = CHASE[lang][step];
    if (!t) continue;
    const first = esc(String(l.name || "").split(/\s+/)[0]);
    const unsub = `${SITE}/.netlify/functions/unsubscribe?ref=${encodeURIComponent(l.ref)}&t=${unsubToken(l.ref)}`;
    try {
      await send({ from: FROM, to: [l.email], reply_to: TEAM, subject: t.s,
        html: shell(t.b(first), lang === "ar", ` · <a href="${unsub}" style="color:#777">${UNSUB[lang]}</a>`),
        headers: { "List-Unsubscribe": `<${unsub}>` } });
      await rpc("server_mark_followup", { p_lead: l.id, p_step: step + 1, p_note: `Quote follow-up email ${step + 1} sent` });
      sent++;
    } catch (e) { console.error("chaser failed", l.ref, e); }
  }
  const busy = q.new_24h.length + q.untouched.length + q.due.length;
  if (busy) {
    const d = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", timeZone: "Asia/Kuala_Lumpur" });
    await send({ from: FROM, to: [TEAM], subject: `Leads ${d}: ${q.untouched.length} not contacted · ${q.due.length} follow-ups due · ${q.new_24h.length} new`, html: digest(q) });
  }
  console.log(`followup: digest ${busy ? "sent" : "skipped"}, ${sent} client follow-ups`);
  return new Response("ok");
};
