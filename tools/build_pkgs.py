#!/usr/bin/env python3
"""Adds Packages, Thank-you and legal pages to /home/claude/wizz-dist using about.html as the template."""
import re, html, glob, os, json
from catalog import COUNTRIES, ADDONS

D = "/home/claude/wizz-dist"
esc = lambda s: html.escape(s, quote=True)
tpl = open(f"{D}/about.html").read()
HEAD, rest = tpl.split("<main id=\"top\">", 1)
FOOT = rest.split("</main>", 1)[1]

def page(fname, title, desc, body, current=None, extra_head="", scripts=""):
    h = HEAD
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(title)}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">', h)
    url = f"https://wizz.com.my/{fname}"
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h)
    h = h.replace('<body data-page="about">', f'<body data-page="{fname[:-5]}">')
    h = h.replace(' aria-current="page"', "")
    if current:
        h = h.replace(f'href="{current}" data-i18n=', f'href="{current}" aria-current="page" data-i18n=', 1)
    h = h.replace("</head>", extra_head + "\n</head>", 1)
    foot = FOOT.replace('<script src="site.js"></script>', scripts + '<script src="site.js"></script>') if scripts else FOOT
    open(f"{D}/{fname}", "w").write(h + '<main id="top">\n' + body + "\n</main>" + foot)

def hero(eyebrow, title, lede):
    return f'''<section class="page-hero night">
  <div class="wrap noimg">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </div>
  </div>
</section>'''

# ---------------- packages
def tier_html(c, t):
    if t["p"] is None:
        price = '<div class="pk-price">Quote</div>'
    else:
        price = f'<div class="pk-price">{"<span class=\"from\">from</span>" if t.get("frm") else ""}${t["p"]:,}<small>USD</small></div>'
    if t.get("sku") and t.get("deposit"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}">Pay ${t["deposit"]} deposit</button>'
    elif t.get("sku"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}">Buy now</button>'
    else:
        cta = f'<a class="btn ghost" href="contact.html">Get a quote</a>'
    plus = f'<p class="pk-plus">{esc(t["plus"])}</p>' if t.get("plus") else ""
    items = "".join(f"<li>{esc(i)}</li>" for i in t["i"])
    flag = '<span class="pk-flag">Most popular</span>' if t.get("pop") else ""
    return f'''<article class="pk{' pop' if t.get('pop') else ''}">{flag}
        <h3>{esc(t["n"])}</h3>{price}{plus}
        <ul>{items}</ul>
        <div class="pk-cta">{cta}</div>
      </article>'''

tabs, panels = [], []
for idx, c in enumerate(COUNTRIES):
    k = c["c"].lower()
    sel = "true" if idx == 0 else "false"
    tabs.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="p-{k}" aria-selected="{sel}" tabindex="{0 if idx==0 else -1}" data-k="{k}"><b class="ltr">{c["c"]}</b><span>{esc(c["n"])}</span></button>')
    notes = "".join(f'<p class="pk-note">{esc(n)}</p>' for n in c["notes"])
    panels.append(f'''<div class="pk-panel" role="tabpanel" id="p-{k}" aria-labelledby="tab-{k}"{'' if idx==0 else ' hidden'}>
    <div class="pk-head"><span class="pk-code ltr">{c["c"]}<i>.</i></span><div><h2>{esc(c["n"])}</h2><p>{esc(c["e"])}</p></div></div>
    <div class="pk-grid">{"".join(tier_html(c, t) for t in c["tiers"])}</div>
    {notes}
  </div>''')
addons = "".join(f'<div class="pk-addon"><span>{esc(a)}</span><b>{esc(p)}</b></div>' for a, p in ADDONS)

pk_body = hero("Packages", "Clear prices for forming your company abroad",
               "Pick a country and a package. Prices are in USD and include government filing fees unless a note says otherwise. Not sure which fits? Book a free consultation first.") + f'''
<section class="block">
  <div class="wrap">
    <div class="pk-tabs" role="tablist" aria-label="Countries">{"".join(tabs)}</div>
    {"".join(panels)}
    <div class="pk-msg" id="pkMsg" role="status" hidden></div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Add-ons</p><h2>Add to any package</h2><p>Bank, payment and marketplace accounts are approved by each provider. Our add-ons cover preparing and submitting a complete application.</p></div>
    <div class="pk-addons">{addons}</div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">After you pay</p><h2>What happens next</h2></div>
    <ol class="steps">
      <li><h3>Secure payment</h3><p>You pay by card on Airwallex's secure checkout page.</p></li>
      <li><h3>Onboarding form</h3><p>You send your details and documents so we can check eligibility.</p></li>
      <li><h3>Review</h3><p>We confirm everything with you before anything is filed.</p></li>
      <li><h3>Filing</h3><p>We register the company and send your documents as each step completes.</p></li>
      <li><h3>Handover</h3><p>You receive your company documents and next-step checklist.</p></li>
    </ol>
    <p class="fineprint">By paying you agree to our <a href="terms.html">Terms of Service</a> and <a href="refund.html">Refund Policy</a>. If we find your case can't go ahead, you get a refund under the Refund Policy.</p>
  </div>
</section>'''

PK_JS = '''<script src="https://static.airwallex.com/components/sdk/v1/index.js"></script>
<script>
(function(){
  const tabs=[...document.querySelectorAll('.pk-tabs [role=tab]')];
  function sel(t,focus){tabs.forEach(b=>{const on=b===t;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;document.getElementById(b.getAttribute('aria-controls')).hidden=!on;});if(focus)t.focus();try{history.replaceState(null,'','#'+t.dataset.k)}catch(e){}}
  tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(t));t.addEventListener('keydown',e=>{let j=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')j=(i+1)%tabs.length;if(e.key==='ArrowLeft'||e.key==='ArrowUp')j=(i-1+tabs.length)%tabs.length;if(j!==null){e.preventDefault();sel(tabs[j],true)}})});
  const h=location.hash.slice(1);const start=tabs.find(t=>t.dataset.k===h);if(start)sel(start);
  const msg=document.getElementById('pkMsg');
  function say(text){msg.textContent=text;msg.hidden=false;msg.scrollIntoView({block:'nearest',behavior:'smooth'});}
  document.querySelectorAll('.pk-buy').forEach(btn=>btn.addEventListener('click',async()=>{
    const label=btn.textContent;btn.disabled=true;btn.textContent='Opening secure checkout…';msg.hidden=true;
    try{
      const r=await fetch('/.netlify/functions/checkout',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({sku:btn.dataset.sku})});
      const d=await r.json().catch(()=>({}));
      if(!r.ok){throw new Error(d.error==='not_configured'?'Online payment is being set up. Message us on WhatsApp at +60 11-2447 7685 and we will send you a payment link.':'We couldn\\'t open the checkout. Please try again, or message us on WhatsApp at +60 11-2447 7685.');}
      if(!window.AirwallexComponentsSDK)throw new Error('The payment page didn\\'t load. Check your connection and try again.');
      const {payments}=await window.AirwallexComponentsSDK.init({env:d.env,enabledElements:['payments']});
      try{sessionStorage.setItem('wizz-order',JSON.stringify({order:d.order_id,pkg:d.package}))}catch(e){}
      payments.redirectToCheckout({env:d.env,mode:'payment',currency:d.currency,intent_id:d.intent_id,client_secret:d.client_secret,successUrl:location.origin+'/thank-you.html?intent='+encodeURIComponent(d.intent_id)});
    }catch(err){say(err.message);btn.disabled=false;btn.textContent=label;}
  }));
})();
</script>
'''
page("packages.html", "Packages | Wizz Smart Services",
     "Company formation packages with clear USD prices for the USA, UK, Canada, Estonia, France, Malaysia, UAE, Saudi Arabia and more.",
     pk_body, current="packages.html", scripts=PK_JS)

# ---------------- thank you + onboarding
ty_body = hero("Payment", "Thank you", "We're confirming your payment with Airwallex.") + '''
<section class="block">
  <div class="wrap ty">
    <div class="ty-status" id="tyStatus" role="status">Checking your payment…</div>
    <form class="ty-form" id="onboard" name="onboarding" method="POST" data-netlify="true" netlify-honeypot="company_website" hidden>
      <input type="hidden" name="form-name" value="onboarding">
      <input type="hidden" name="order_id" id="ob_order">
      <input type="hidden" name="payment_intent" id="ob_intent">
      <input type="hidden" name="package" id="ob_pkg">
      <p class="hp"><label>Leave this empty <input name="company_website"></label></p>
      <h2>Onboarding details</h2>
      <p class="muted">We use these details to check eligibility and prepare your filings. We'll ask for passport copies separately over a secure channel.</p>
      <div class="ty-grid">
        <div><label for="ob_name">Full name (as on passport)</label><input id="ob_name" name="full_name" required autocomplete="name"></div>
        <div><label for="ob_email">Email</label><input id="ob_email" name="email" type="email" required autocomplete="email"></div>
        <div><label for="ob_phone">WhatsApp number</label><input id="ob_phone" name="whatsapp" required autocomplete="tel"></div>
        <div><label for="ob_nat">Nationality</label><input id="ob_nat" name="nationality" required></div>
        <div class="full"><label for="ob_addr">Full residential address</label><textarea id="ob_addr" name="residential_address" required autocomplete="street-address"></textarea></div>
        <div><label for="ob_nid">National ID number</label><input id="ob_nid" name="national_id_number" required></div>
        <div><label for="ob_pass">Passport number</label><input id="ob_pass" name="passport_number" required></div>
        <div class="full"><label for="ob_names">Proposed company names (up to 3, in order of preference)</label><textarea id="ob_names" name="company_names" required></textarea></div>
        <div class="full"><label for="ob_act">Business activity</label><input id="ob_act" name="business_activity" required placeholder="e.g. selling skincare products on Amazon US"></div>
        <div><label for="ob_owners">Owners</label><select id="ob_owners" name="owners"><option>Single owner</option><option>Two or more partners</option></select></div>
        <div><label for="ob_brand">If selling online</label><select id="ob_brand" name="brand_model"><option>Not applicable</option><option>My own private brand</option><option>Reselling other brands</option></select></div>
        <div class="full"><label for="ob_notes">Anything else we should know?</label><textarea id="ob_notes" name="notes"></textarea></div>
      </div>
      <label class="ty-agree"><input type="checkbox" required name="agree" value="yes"> I confirm these details are correct and I agree to the <a href="terms.html">Terms of Service</a> and <a href="privacy.html">Privacy Policy</a>.</label>
      <button class="btn solid" type="submit"><span class="dot"></span>Send my details</button>
    </form>
    <div class="ty-done" id="tyDone" hidden><h2>Details received</h2><p>Thank you. We'll review your details and contact you on WhatsApp or email within one business day.</p></div>
  </div>
</section>'''
TY_JS = '''<script>
(function(){
  const st=document.getElementById('tyStatus'),f=document.getElementById('onboard');
  const intent=new URLSearchParams(location.search).get('intent')||'';
  let saved={};try{saved=JSON.parse(sessionStorage.getItem('wizz-order')||'{}')}catch(e){}
  function showForm(d){f.hidden=false;document.getElementById('ob_order').value=d.order_id||saved.order||'';document.getElementById('ob_intent').value=intent;document.getElementById('ob_pkg').value=d.package||saved.pkg||'';}
  if(!intent){st.innerHTML='We couldn\\'t find a payment reference. If you paid, message us on WhatsApp at <span class="ltr">+60 11-2447 7685</span> with your receipt.';return;}
  fetch('/.netlify/functions/verify?intent='+encodeURIComponent(intent)).then(r=>r.json()).then(d=>{
    if(d.paid){st.className='ty-status ok';st.textContent='Payment received: '+(d.package||'your package')+' · '+d.currency+' '+Number(d.amount).toLocaleString('en-US')+' · Order '+d.order_id;showForm(d);}
    else{st.innerHTML='Your payment isn\\'t confirmed yet (status: '+(d.status||'unknown')+'). If you completed it, refresh in a minute or message us on WhatsApp at <span class="ltr">+60 11-2447 7685</span>.';}
  }).catch(()=>{st.innerHTML='We couldn\\'t check the payment right now. Fill in the form below and we\\'ll match it to your payment.';showForm({});});
  f.addEventListener('submit',async e=>{e.preventDefault();if(!f.reportValidity())return;
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{const r=await fetch('/',{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()});if(!r.ok)throw 0;f.hidden=true;document.getElementById('tyDone').hidden=false;}
    catch(_){b.disabled=false;st.textContent='We couldn\\'t send the form. Please try again or email info@wizz.com.my.';}
  });
})();
</script>
'''
page("thank-you.html", "Thank you | Wizz Smart Services", "Payment confirmation and onboarding.", ty_body, scripts=TY_JS,
     extra_head='<meta name="robots" content="noindex">')

# ---------------- legal pages
CO = "WIZZ SMART SERVICES SDN. BHD. (Registration No. 202501029005), B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia"
def legal(fname, title, lede, sections):
    secs = "".join(f"<h2>{esc(h)}</h2>" + "".join(f"<p>{p}</p>" if not isinstance(p, list) else "<ul>" + "".join(f"<li>{x}</li>" for x in p) + "</ul>" for p in ps) for h, ps in sections)
    body = hero("Legal", title, lede) + f'''
<section class="block">
  <div class="wrap legal-doc">
    <p class="muted">Last updated: 5 October 2026</p>
    {secs}
    <h2>Contact</h2><p>{CO}. Email <span class="ltr">info@wizz.com.my</span>, WhatsApp <span class="ltr">+60 11-2447 7685</span>.</p>
  </div>
</section>'''
    page(fname, f"{title} | Wizz Smart Services", lede, body, extra_head="")

legal("terms.html", "Terms of Service", "The terms that apply when you buy a package or service from Wizz Smart Services.", [
 ("Who we are", [f"These terms are between you and {CO} (\"Wizz\", \"we\")."]),
 ("Our services", ["We provide business services: company formation, registered address and agent coordination, document preparation, applications to banks, payment providers and marketplaces, logistics coordination and related support, as described in the package you choose.",
   "We are not a law firm or a tax adviser. Where your situation needs legal or tax advice, we refer you to a qualified professional in the relevant country."]),
 ("Third-party decisions", ["Company registries, tax authorities, immigration authorities, banks, payment providers and marketplaces make their own decisions. We do not guarantee any registration, licence, visa, work permit, bank account, payment account, marketplace account, tax result or business result."]),
 ("Your responsibilities", [["Give us accurate, complete and current information and documents.","Use the company only for lawful activities.","Pay any government or third-party fees that your package does not include.","Keep up with yearly filings and renewals after the period included in your package."]]),
 ("Eligibility checks", ["Before filing, we check your identity and eligibility under anti-money-laundering and know-your-customer rules, ours and those of our partners. We may decline or stop work if a check fails or if information is false or incomplete."]),
 ("Prices and payment", ["Prices are shown in US dollars. Payments are processed securely by Airwallex; we never see or store your full card details. Prices marked \"from\" are confirmed in a written quote before work starts."]),
 ("Timelines", ["Timelines we give are estimates. Delays caused by authorities, providers or missing information are outside our control."]),
 ("Refunds", ["Refunds follow our <a href=\"refund.html\">Refund Policy</a>."]),
 ("Liability", ["To the extent the law allows, our total liability for any claim is limited to the fees you paid us for the service concerned. We are not liable for decisions made by third parties or for indirect losses."]),
 ("Governing law", ["These terms are governed by the laws of Malaysia, and the courts of Kuala Lumpur have jurisdiction."]),
])
legal("refund.html", "Refund Policy", "When and how you can get your money back.", [
 ("Before we start", ["If you cancel before we submit anything on your behalf, you get a full refund of the amount you paid."]),
 ("After we submit", ["Once an application or filing has been submitted, government fees and fees paid to third parties (such as registered agents, address providers and partners) can't be refunded. We refund the unused part of our service fee, based on the work already done."]),
 ("If your case can't go ahead", ["If our eligibility check shows we can't complete your package, we refund what you paid, less any government or third-party fees already paid on your behalf."]),
 ("Decisions by third parties", ["A refusal by a bank, payment provider, marketplace or authority is not by itself a reason for a refund of work already completed, because those decisions are outside our control."]),
 ("Deposits", ["Deposits are credited to your final package price. A deposit is refundable in full until work starts."]),
 ("How to request a refund", ["Email <span class=\"ltr\">info@wizz.com.my</span> with your order number. We reply within 5 business days and send approved refunds to the original payment method, normally within 10 business days."]),
])
legal("privacy.html", "Privacy Policy", "How we collect, use and protect your personal data.", [
 ("What we collect", [["Contact details: name, email, phone or WhatsApp number.","Identity details: nationality, full residential address, national ID number, passport details and copies.","Company details: proposed names, activity, shareholders and directors.","Payment details: order and payment references. Card details are handled by Airwallex, not by us."]]),
 ("Why we use it", [["To provide the services you buy, including filings with registries and authorities.","To carry out identity and eligibility checks required by law and by our partners.","To contact you about your order and your yearly obligations."]]),
 ("Who we share it with", ["Only as needed to deliver your service: company registries and government authorities, registered agents, company secretaries, address providers and professional partners in the relevant country, our payment processor (Airwallex), and our website and form host (Netlify). We don't sell your data."]),
 ("International transfers", ["Because we form companies in other countries, your data is sent to the country of your company and to our partners there."]),
 ("How long we keep it", ["We keep your records for as long as needed to provide the service and to meet legal record-keeping duties, normally up to 7 years after our work ends."]),
 ("Your rights", ["Under Malaysia's Personal Data Protection Act 2010 you can ask to access or correct your personal data, or to limit how we use it. Email <span class=\"ltr\">info@wizz.com.my</span>."]),
 ("Security", ["We limit access to your data to the people who need it and use secure services to store and send it."]),
])

# ---------------- nav + footer links on every page
for f in glob.glob(f"{D}/*.html"):
    s = open(f).read()
    if 'href="packages.html" data-i18n="nav_pkgs"' not in s:
        cur = ' aria-current="page"' if f.endswith("/packages.html") else ""
        s = s.replace('<a href="services.html" data-i18n="nav_services"', f'<a href="packages.html"{cur} data-i18n="nav_pkgs">Packages</a>\n      <a href="services.html" data-i18n="nav_services"', 1)
    if 'href="terms.html">Terms</a>' not in s:
        s = s.replace('<div class="legal">\n', '<div class="legal">\n      <span class="legal-links"><a href="terms.html">Terms</a> · <a href="refund.html">Refunds</a> · <a href="privacy.html">Privacy</a></span>\n', 1)
    # the hero CTA on home now points to packages as a second option
    open(f, "w").write(s)

# Arabic label for the new nav item
js = open(f"{D}/site.js").read()
if '"nav_pkgs"' not in js:
    js = js.replace('"nav_mp": ', '"nav_pkgs": "الباقات", "nav_mp": ', 1)
    assert '"nav_pkgs"' in js
    open(f"{D}/site.js", "w").write(js)

# CSS
CSS = '''
/* ===== v6: packages, checkout, legal ===== */
.pk-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}
.pk-tabs button{font:600 14px var(--body);display:flex;gap:8px;align-items:center;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:8px 14px;cursor:pointer}
.pk-tabs button b{font-family:var(--display);font-stretch:125%;font-weight:900}
.pk-tabs button[aria-selected="true"]{background:var(--ink);color:var(--on-ink);border-color:var(--ink)}
.pk-tabs button:hover{border-color:var(--ink)}
.pk-head{display:flex;gap:18px;align-items:center;margin-bottom:24px}
.pk-head>div{min-width:0}
.pk-code{font:900 clamp(48px,6vw,72px)/.9 var(--display);font-stretch:125%;letter-spacing:-.02em}
.pk-code i{font-style:normal;color:var(--red)}
.pk-head h2{font-size:clamp(24px,3vw,32px);font-weight:850}
.pk-head p{color:var(--muted);margin-top:4px}
.pk-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-bottom:16px}
.pk{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:24px 22px;display:flex;flex-direction:column;gap:12px;position:relative;min-width:0}
.pk.pop{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.pk-flag{position:absolute;top:-11px;inset-inline-start:18px;background:var(--red);color:#fff;font:600 11px var(--mono);letter-spacing:.06em;padding:3px 9px;border-radius:999px}
.pk h3{font-size:19px;font-weight:800}
.pk-price{font:850 38px/1 var(--display);font-stretch:110%;font-variant-numeric:tabular-nums}
.pk-price small{font:500 13px var(--body);color:var(--muted);margin-inline-start:6px}
.pk-price .from{display:block;font:600 13px var(--body);color:var(--muted);margin-bottom:4px}
.pk-plus{font-size:13px;color:var(--muted);font-style:italic}
.pk ul{list-style:none;margin:0;padding:0;display:grid;gap:8px;font-size:14.5px}
.pk li{display:grid;grid-template-columns:14px 1fr;gap:8px}
.pk li::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--ink);margin-top:8px}
.pk-cta{margin-top:auto;padding-top:14px;border-top:1px dashed var(--line)}
.pk-cta .btn{width:100%;justify-content:center}
.pk-cta .btn:disabled{opacity:.6;cursor:progress}
.pk-note{font-size:14px;border-inline-start:3px solid var(--red);padding:6px 12px;color:var(--muted);margin-top:8px}
.pk-msg{margin-top:20px;border:1.5px solid var(--red);background:var(--surface);border-radius:8px;padding:14px 16px;font-weight:500}
.pk-addons{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.pk-addon{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:flex;justify-content:space-between;gap:12px;align-items:baseline}
.pk-addon b{font:700 15px var(--mono);white-space:nowrap}
.ty{max-width:820px}
.ty-status{border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:16px 18px;font-weight:500;margin-bottom:28px}
.ty-status.ok{border-color:var(--ink);box-shadow:inset 4px 0 0 var(--red)}
.ty-form{display:grid;gap:16px}
.ty-form h2{font-size:26px;font-weight:850}
.ty-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 18px}
.ty-grid .full{grid-column:1/-1}
.ty-grid>*{min-width:0}
.ty-agree{display:flex;gap:10px;align-items:flex-start;font-weight:500;font-size:14.5px}
.ty-agree input{width:auto;margin-top:4px}
.hp{position:absolute;left:-9999px}
@media (max-width:600px){.ty-grid{grid-template-columns:1fr}}
.legal-doc{max-width:760px;display:grid;gap:12px}
.legal-doc h2{font-size:21px;font-weight:800;margin-top:18px}
.legal-doc p,.legal-doc li{color:var(--ink);font-size:16px}
.legal-doc ul{margin:0;padding-inline-start:20px;display:grid;gap:6px}
.legal-links a{color:inherit}
.steps h3{font-size:17px}
'''
css = open(f"{D}/site.css").read()
if "v6: packages" not in css:
    open(f"{D}/site.css", "w").write(css + CSS)

# sitemap
pages = sorted(os.path.basename(p) for p in glob.glob(f"{D}/*.html") if not p.endswith("thank-you.html"))
open(f"{D}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>https://wizz.com.my/{"" if p=="index.html" else p}</loc></url>\n' for p in pages) + "</urlset>\n")
print("built", pages)
