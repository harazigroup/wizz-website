// One-click stop for automatic follow-up emails. Link: /.netlify/functions/unsubscribe?ref=L-XXXXXX&t=<token>
import { timingSafeEqual } from "node:crypto";
import { dbOn, rpc } from "./_db.mjs";
import { unsubToken } from "./followup.mjs";

const page = (msg) => new Response(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wizz Smart Services</title>
<body style="font-family:Arial,sans-serif;max-width:520px;margin:60px auto;padding:0 20px;color:#111;line-height:1.5"><img src="/img/email-logo.png" alt="Wizz" height="32"><p style="font-size:17px">${msg}</p><p><a href="/">wizz.com.my</a></p></body>`,
  { headers: { "content-type": "text/html; charset=utf-8" } });

export default async (req) => {
  const u = new URL(req.url);
  const ref = u.searchParams.get("ref") || "", t = u.searchParams.get("t") || "";
  const ok = /^L-[A-Z0-9]{6}$/.test(ref) && t.length === 24 && timingSafeEqual(Buffer.from(t), Buffer.from(unsubToken(ref)));
  if (!ok || !dbOn()) return page("This link isn't valid. Reply to our email and we'll stop the follow-ups for you.");
  try { await rpc("server_unsubscribe_lead", { p_ref: ref }); } catch (e) { console.error(e); return page("Something went wrong. Reply to our email and we'll stop the follow-ups for you."); }
  return page("Done. We won't send you any more automatic follow-up emails. You can still reach us any time on WhatsApp at +60 11-2447 7685.");
};
