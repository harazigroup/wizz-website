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

from catalog_ar import AR as AR_SRC
import hashlib
AR_OUT = {}
RAW = lambda x: x
def tk(en, render=None):
    """data-i18n attributes for an English string; records its Arabic for this page."""
    if en not in AR_SRC: raise SystemExit(f"Missing Arabic in tools/catalog_ar.py for: {en!r}")
    key = "pk_" + hashlib.md5(en.encode()).hexdigest()[:8]
    AR_OUT[key] = (render or esc)(AR_SRC[en])
    return f' data-i18n="{key}" data-html'
def kph(en):
    if en not in AR_SRC: raise SystemExit(f"Missing Arabic in tools/catalog_ar.py for: {en!r}")
    key = "pk_" + hashlib.md5(en.encode()).hexdigest()[:8]
    AR_OUT[key] = AR_SRC[en]
    return f' data-i18n-ph="{key}"'
def ar_script():
    """Arabic strings for site.js to merge before it applies the language. Clears the page buffer."""
    out = "<script>window.WIZZ_AR=" + json.dumps(AR_OUT, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"
    AR_OUT.clear()
    return out
def hero_t(eyebrow, title, lede):
    return f'''<section class="page-hero night">
  <div class="wrap noimg">
    <div>
      <p class="eyebrow"{tk(eyebrow)}>{esc(eyebrow)}</p>
      <h1{tk(title)}>{esc(title)}</h1>
      <p class="lede"{tk(lede)}>{esc(lede)}</p>
    </div>
  </div>
</section>'''

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
import re
def money(usd):
    return f'<span class="m" data-usd="{usd}">${usd:,}</span>'
def money_text(txt):
    return re.sub(r"\$([0-9][0-9,]*)", lambda m: money(int(m.group(1).replace(",", ""))), esc(txt))

def tier_html(c, t):
    if t["p"] is None:
        price = f'<div class="pk-price"{tk("Quote")}>Quote</div>'
    else:
        price = f'<div class="pk-price">{f'<span class="from"{tk("from")}>from</span>' if t.get("frm") else ""}{money(t["p"])}<small class="cur">USD</small></div>'
    if t.get("sku") and t.get("deposit"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}"><span{tk("Pay")}>Pay</span> {money(t["deposit"])} <span{tk("deposit")}>deposit</span></button>'
    elif t.get("sku"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}"{tk("Buy now")}>Buy now</button>'
    else:
        cta = f'<a class="btn ghost" href="contact.html"{tk("Get a quote")}>Get a quote</a>'
    plus = f'<p class="pk-plus"{tk(t["plus"], money_text)}>{money_text(t["plus"])}</p>' if t.get("plus") else ""
    items = "".join(f"<li{tk(i)}>{esc(i)}</li>" for i in t["i"])
    flag = f'<span class="pk-flag"{tk("Most popular")}>Most popular</span>' if t.get("pop") else ""
    return f'''<article class="pk{' pop' if t.get('pop') else ''}">{flag}
        <h3{tk(t["n"])}>{esc(t["n"])}</h3>{price}{plus}
        <ul>{items}</ul>
        <div class="pk-cta">{cta}</div>
      </article>'''

tabs, panels = [], []
for idx, c in enumerate(COUNTRIES):
    k = c["c"].lower()
    sel = "true" if idx == 0 else "false"
    tabs.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="p-{k}" aria-selected="{sel}" tabindex="{0 if idx==0 else -1}" data-k="{k}"><b class="ltr">{c["c"]}</b><span{tk(c["n"])}>{esc(c["n"])}</span></button>')
    notes = "".join(f'<p class="pk-note"{tk(n, money_text)}>{money_text(n)}</p>' for n in c["notes"])
    panels.append(f'''<div class="pk-panel" role="tabpanel" id="p-{k}" aria-labelledby="tab-{k}"{'' if idx==0 else ' hidden'}>
    <div class="pk-head"><span class="pk-code ltr">{c["c"]}<i>.</i></span><div><h2{tk(c["n"])}>{esc(c["n"])}</h2><p{tk(c["e"])}>{esc(c["e"])}</p></div></div>
    <div class="pk-grid">{"".join(tier_html(c, t) for t in c["tiers"])}</div>
    {notes}
  </div>''')
addons = "".join(f'<div class="pk-addon"><span{tk(a)}>{esc(a)}</span><b{tk(p, money_text)}>{money_text(p)}</b></div>' for a, p in ADDONS)

FP = 'By paying you agree to our <a href="terms.html">Terms of Service</a> and <a href="refund.html">Refund Policy</a>. If we find your case can\'t go ahead, you get a refund under the Refund Policy.'
pk_body = hero_t("Packages", "Clear prices for forming your company abroad",
               "Pick a country and a package. Prices show in your local currency, and you pay exactly the price you see. They include government filing fees unless a note says otherwise. Not sure which fits? Book a free consultation first.") + f'''
<section class="block">
  <div class="wrap">
    <div class="pk-curbar"><label for="pkCur"{tk("Prices in")}>Prices in</label><select id="pkCur"><option value="USD">USD · US dollar</option></select><span class="pk-curnote" id="pkCurNote">Set in US dollars. Change the currency if you prefer.</span></div>
    <div class="pk-tabs" role="tablist" aria-label="Countries">{"".join(tabs)}</div>
    {"".join(panels)}
    <div class="pk-msg" id="pkMsg" role="status" hidden></div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow"{tk('Add-ons')}>Add-ons</p><h2{tk('Add to any package')}>Add to any package</h2><p{tk('Bank, payment and marketplace accounts are approved by each provider. Our add-ons cover preparing and submitting a complete application.')}>Bank, payment and marketplace accounts are approved by each provider. Our add-ons cover preparing and submitting a complete application.</p></div>
    <div class="pk-addons">{addons}</div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow"{tk('After you pay')}>After you pay</p><h2{tk('What happens next')}>What happens next</h2></div>
    <ol class="steps">
      <li><h3{tk('Secure payment')}>Secure payment</h3><p{tk('You pay by card on a secure checkout page run by our payment provider.')}>You pay by card on a secure checkout page run by our payment provider.</p></li>
      <li><h3{tk('Onboarding form')}>Onboarding form</h3><p{tk('You send your details and documents so we can check eligibility.')}>You send your details and documents so we can check eligibility.</p></li>
      <li><h3{tk('Review')}>Review</h3><p{tk('We confirm everything with you before anything is filed.')}>We confirm everything with you before anything is filed.</p></li>
      <li><h3{tk('Filing')}>Filing</h3><p{tk('We register the company and send your documents as each step completes.')}>We register the company and send your documents as each step completes.</p></li>
      <li><h3{tk('Handover')}>Handover</h3><p{tk('You receive your company documents and next-step checklist.')}>You receive your company documents and next-step checklist.</p></li>
    </ol>
    <p class="fineprint"{tk(FP, RAW)}>By paying you agree to our <a href="terms.html">Terms of Service</a> and <a href="refund.html">Refund Policy</a>. If we find your case can't go ahead, you get a refund under the Refund Policy.</p>
  </div>
</section>'''

PK_JS = '''<script src="https://static.airwallex.com/components/sdk/v1/index.js"></script>
<script>
(function(){
  const tabs=[...document.querySelectorAll('.pk-tabs [role=tab]')];
  function sel(t,focus){tabs.forEach(b=>{const on=b===t;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;document.getElementById(b.getAttribute('aria-controls')).hidden=!on;});if(focus)t.focus();try{history.replaceState(null,'','#'+t.dataset.k)}catch(e){}}
  tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(t));t.addEventListener('keydown',e=>{let j=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')j=(i+1)%tabs.length;if(e.key==='ArrowLeft'||e.key==='ArrowUp')j=(i-1+tabs.length)%tabs.length;if(j!==null){e.preventDefault();sel(tabs[j],true)}})});
  const h=location.hash.slice(1);const start=tabs.find(t=>t.dataset.k===h);if(start)sel(start);
  const NAMES={USD:'US dollar',GBP:'British pound',EUR:'Euro',CAD:'Canadian dollar',AUD:'Australian dollar',SGD:'Singapore dollar',AED:'UAE dirham',SAR:'Saudi riyal',QAR:'Qatari riyal',MYR:'Malaysian ringgit',THB:'Thai baht'};
  const NAMES_AR={USD:'دولار أمريكي',GBP:'جنيه إسترليني',EUR:'يورو',CAD:'دولار كندي',AUD:'دولار أسترالي',SGD:'دولار سنغافوري',AED:'درهم إماراتي',SAR:'ريال سعودي',QAR:'ريال قطري',MYR:'رينغيت ماليزي',THB:'بات تايلاندي'};
  const ar=()=>document.documentElement.lang==='ar';
  const T=(en,a)=>ar()?a:en;
  const cs=document.getElementById('pkCur'),note=document.getElementById('pkCurNote');
  let FX=null,cur='USD';
  function local(usd,c){const r=FX&&FX.rates[c];if(!r||c==='USD')return usd;const raw=usd*r.rate*(1+FX.buffer);const up=Math.ceil(raw/r.step)*r.step;return r.nine?up-1:up;}
  function fmt(n,c){try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol',maximumFractionDigits:0,minimumFractionDigits:0}).format(n)}catch(e){return c+' '+n.toLocaleString('en-US')}}
  function apply(c){cur=(FX&&FX.rates[c])?c:'USD';
    document.querySelectorAll('.m[data-usd]').forEach(el=>{el.textContent=fmt(local(+el.dataset.usd,cur),cur)});
    document.querySelectorAll('.pk-price .cur').forEach(el=>{const shown=el.previousElementSibling?el.previousElementSibling.textContent:'';el.textContent=/[A-Z]{3}/.test(shown)?'':cur;});
    cs.value=cur;note.textContent=cur==='USD'?T('Set in US dollars. Change the currency if you prefer.','الأسعار بالدولار الأمريكي، ويمكنك تغيير العملة.'):T('Converted from our US dollar prices at a recent rate. You pay exactly this amount in '+cur+'.','محوّلة من أسعارنا بالدولار الأمريكي حسب سعر صرف حديث، وتدفع هذا المبلغ نفسه بعملة '+cur+'.');}
  function fill(){const list=FX?Object.keys(FX.rates):['USD'];cs.innerHTML=list.map(c=>'<option value="'+c+'">'+c+' · '+((ar()?NAMES_AR:NAMES)[c]||c)+'</option>').join('');}
  document.addEventListener('wizz:lang',()=>{fill();apply(cur);});
  fetch('/.netlify/functions/prices').then(r=>r.ok?r.json():Promise.reject()).then(d=>{FX=d;
    fill();
    let pick=d.currency;try{const s=localStorage.getItem('wizz-cur');if(s&&d.rates[s])pick=s}catch(e){}
    apply(pick);
  }).catch(()=>{});
  cs.addEventListener('change',()=>{apply(cs.value);try{localStorage.setItem('wizz-cur',cur)}catch(e){}});
  const msg=document.getElementById('pkMsg');
  function say(text){msg.textContent=text;msg.hidden=false;msg.scrollIntoView({block:'nearest',behavior:'smooth'});}
  document.querySelectorAll('.pk-buy').forEach(btn=>btn.addEventListener('click',async()=>{
    const kids=[...btn.childNodes];btn.disabled=true;btn.textContent=T('Opening secure checkout…','جارٍ فتح صفحة الدفع الآمنة…');msg.hidden=true;
    try{
      const r=await fetch('/.netlify/functions/checkout',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({sku:btn.dataset.sku,currency:cur})});
      const d=await r.json().catch(()=>({}));
      if(!r.ok){throw new Error(d.error==='not_configured'?T('Online payment is being set up. Message us on WhatsApp at +60 11-2447 7685 and we will send you a payment link.','الدفع الإلكتروني قيد الإعداد. راسلنا على واتساب على الرقم ‎+60 11-2447 7685 وسنرسل لك رابط الدفع.'):T('We couldn\\'t open the checkout. Please try again, or message us on WhatsApp at +60 11-2447 7685.','تعذّر فتح صفحة الدفع. حاول مرة أخرى، أو راسلنا على واتساب على الرقم ‎+60 11-2447 7685.'));}
      if(d.url){try{sessionStorage.setItem('wizz-order',JSON.stringify({order:d.order_id,pkg:d.package}))}catch(e){}location.href=d.url;return;}
      if(!window.AirwallexComponentsSDK)throw new Error(T('The payment page didn\\'t load. Check your connection and try again.','لم تُحمَّل صفحة الدفع. تحقّق من اتصالك وحاول مرة أخرى.'));
      const {payments}=await window.AirwallexComponentsSDK.init({env:d.env,enabledElements:['payments']});
      try{sessionStorage.setItem('wizz-order',JSON.stringify({order:d.order_id,pkg:d.package}))}catch(e){}
      payments.redirectToCheckout({env:d.env,mode:'payment',currency:d.currency,intent_id:d.intent_id,client_secret:d.client_secret,successUrl:location.origin+'/thank-you.html?intent='+encodeURIComponent(d.intent_id)});
    }catch(err){say(err.message);btn.disabled=false;btn.replaceChildren(...kids);}
  }));
})();
</script>
'''
page("packages.html", "Packages | Wizz Smart Services",
     "Company formation packages with clear prices in your currency for the USA, UK, Canada, Estonia, France, Malaysia, UAE, Saudi Arabia and more.",
     pk_body, current="packages.html", scripts=ar_script() + PK_JS)

# ---------------- server catalog for checkout (price, name, checkout description and image)
def checkout_desc(t):
    items = "; ".join(t["i"])
    if t.get("deposit"):
        return f"Deposit, credited to your final package price. Includes: {items}."
    return (f"{t['plus']}: {items}." if t.get("plus") else f"Includes: {items}.")
SERVER = {}
for c in COUNTRIES:
    for t in c["tiers"]:
        if not t.get("sku"): continue
        SERVER[t["sku"]] = {"name": f'{c["n"]} - {t["n"]}' + (" (deposit)" if t.get("deposit") else ""),
                            "amount": t.get("deposit") or t["p"], "currency": "USD",
                            "desc": checkout_desc(t)[:480], "image": f'https://wizz.com.my/img/pay/{c["c"].lower()}.png'}
open(f"{D}/netlify/functions/catalog.json", "w").write(json.dumps(SERVER, indent=1, ensure_ascii=False) + "\n")

# ---------------- thank you + onboarding
ty_body = hero_t("Payment", "Thank you", "We're confirming your payment.") + '''
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
      <label class="ty-agree"><input type="checkbox" required name="agree" value="yes"> <span>I confirm these details are correct and I agree to the <a href="terms.html">Terms of Service</a> and <a href="privacy.html">Privacy Policy</a>.</span></label>
      <button class="btn solid" type="submit"><span class="dot"></span>Send my details</button>
    </form>
    <div class="ty-done" id="tyDone" hidden><h2>Details received</h2><p>Thank you. We'll review your details and contact you on WhatsApp or email within one business day.</p></div>
  </div>
</section>'''
def auto_i18n(h):
    """Adds data-i18n to every element whose whole content is a string we have Arabic for."""
    def tag(m):
        name, attrs, inner = m.group(1), m.group(2), m.group(3)
        key = inner.strip()
        if "data-i18n" in attrs or key not in AR_SRC: return m.group(0)
        if name == "option" and "value=" not in attrs: attrs += f' value="{esc(key)}"'
        return f"<{name}{attrs}{tk(key, RAW)}>{inner}</{name}>"
    h = re.sub(r'<(\w+)((?:\s[^<>]*)?)>((?:[^<]|<a [^>]*>[^<]*</a>|<span class="dot"></span>)+?)</\1>', tag, h)
    return re.sub(r'placeholder="([^"]+)"', lambda m: m.group(0) + (kph(html.unescape(m.group(1))) if html.unescape(m.group(1)) in AR_SRC else ""), h)
ty_body = auto_i18n(ty_body)

TY_JS = '''<script>
(function(){
  const st=document.getElementById('tyStatus'),f=document.getElementById('onboard');
  const T=(en,a)=>document.documentElement.lang==='ar'?a:en;
  const qs=new URLSearchParams(location.search);const sid=qs.get('session_id')||'';const intent=qs.get('intent')||sid;
  let saved={};try{saved=JSON.parse(sessionStorage.getItem('wizz-order')||'{}')}catch(e){}
  function showForm(d){f.hidden=false;document.getElementById('ob_order').value=d.order_id||saved.order||'';document.getElementById('ob_intent').value=intent;document.getElementById('ob_pkg').value=d.package||saved.pkg||'';}
  if(!intent){st.innerHTML=T('We couldn\\'t find a payment reference. If you paid, message us on WhatsApp at <span class="ltr">+60 11-2447 7685</span> with your receipt.','لم نجد مرجعاً للدفع. إذا كنت قد دفعت، راسلنا على واتساب على الرقم <span class="ltr">+60 11-2447 7685</span> مع إيصال الدفع.');return;}
  fetch('/.netlify/functions/verify?'+(sid?'session_id=':'intent=')+encodeURIComponent(intent)).then(r=>r.json()).then(d=>{
    if(d.paid){st.className='ty-status ok';st.textContent=T('Payment received: ','تم استلام الدفع: ')+(d.package||T('your package','باقتك'))+' · '+d.currency+' '+Number(d.amount).toLocaleString('en-US')+' · '+T('Order ','رقم الطلب ')+d.order_id;showForm(d);}
    else{st.innerHTML=T('Your payment isn\\'t confirmed yet (status: '+(d.status||'unknown')+'). If you completed it, refresh in a minute or message us on WhatsApp at <span class="ltr">+60 11-2447 7685</span>.','لم يتم تأكيد الدفع بعد (الحالة: '+(d.status||'غير معروفة')+'). إذا أكملت الدفع، حدّث الصفحة بعد دقيقة أو راسلنا على واتساب على الرقم <span class="ltr">+60 11-2447 7685</span>.');}
  }).catch(()=>{st.innerHTML=T('We couldn\\'t check the payment right now. Fill in the form below and we\\'ll match it to your payment.','تعذّر التحقق من الدفع الآن. املأ النموذج أدناه وسنطابقه مع دفعتك.');showForm({});});
  f.addEventListener('submit',async e=>{e.preventDefault();if(!f.reportValidity())return;
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{const r=await fetch('/',{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()});if(!r.ok)throw 0;f.hidden=true;document.getElementById('tyDone').hidden=false;}
    catch(_){b.disabled=false;st.textContent=T('We couldn\\'t send the form. Please try again or email info@wizz.com.my.','تعذّر إرسال النموذج. حاول مرة أخرى أو راسلنا على info@wizz.com.my.');}
  });
})();
</script>
'''
page("thank-you.html", "Thank you | Wizz Smart Services", "Payment confirmation and onboarding.", ty_body, scripts=ar_script() + TY_JS,
     extra_head='<meta name="robots" content="noindex">')

# ---------------- legal pages
CO = "WIZZ SMART SERVICES SDN. BHD. (Registration No. 202501029005), B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia"
def legal(fname, title, lede, sections):
    def para(p):
        if isinstance(p, list):
            return "<ul>" + "".join(f"<li{tk(x, RAW)}>{x}</li>" for x in p) + "</ul>"
        return f"<p{tk(p, RAW)}>{p}</p>"
    secs = "".join(f"<h2{tk(h)}>{esc(h)}</h2>" + "".join(para(p) for p in ps) for h, ps in sections)
    contact = f'{CO}. Email <span class="ltr">info@wizz.com.my</span>, WhatsApp <span class="ltr">+60 11-2447 7685</span>.'
    body = hero_t("Legal", title, lede) + f'''
<section class="block">
  <div class="wrap legal-doc">
    <p class="muted"{tk("Last updated: 7 October 2026")}>Last updated: 7 October 2026</p>
    {secs}
    <h2{tk("Contact")}>Contact</h2><p{tk(contact, RAW)}>{contact}</p>
  </div>
</section>'''
    page(fname, f"{title} | Wizz Smart Services", lede, body, extra_head="", scripts=ar_script())

legal("terms.html", "Terms of Service", "The terms that apply when you buy a package or service from Wizz Smart Services.", [
 ("Who we are", [f"These terms are between you and {CO} (\"Wizz\", \"we\")."]),
 ("Our services", ["We provide business services: company formation, registered address and agent coordination, document preparation, applications to banks, payment providers and marketplaces, logistics coordination and related support, as described in the package you choose.",
   "We are not a law firm or a tax adviser. Where your situation needs legal or tax advice, we refer you to a qualified professional in the relevant country."]),
 ("Third-party decisions", ["Company registries, tax authorities, immigration authorities, banks, payment providers and marketplaces make their own decisions. We do not guarantee any registration, licence, visa, work permit, bank account, payment account, marketplace account, tax result or business result."]),
 ("Your responsibilities", [["Give us accurate, complete and current information and documents.","Use the company only for lawful activities.","Pay any government or third-party fees that your package does not include.","Keep up with yearly filings and renewals after the period included in your package."]]),
 ("Eligibility checks", ["Before filing, we check your identity and eligibility under anti-money-laundering and know-your-customer rules, ours and those of our partners. We may decline or stop work if a check fails or if information is false or incomplete."]),
 ("Prices and payment", ["Prices are set in US dollars and shown in your local currency where we support it. You pay the amount shown at checkout, in that currency. Payments are processed securely by our payment providers (Stripe or Airwallex); we never see or store your full card details. Prices marked \"from\" are confirmed in a written quote before work starts."]),
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
 ("What we collect", [["Contact details: name, email, phone or WhatsApp number.","Identity details: nationality, full residential address, national ID number, passport details and copies.","Company details: proposed names, activity, shareholders and directors.","Payment details: order and payment references. Card details are handled by our payment providers (Stripe or Airwallex), not by us."]]),
 ("Why we use it", [["To provide the services you buy, including filings with registries and authorities.","To carry out identity and eligibility checks required by law and by our partners.","To contact you about your order and your yearly obligations."]]),
 ("Who we share it with", ["Only as needed to deliver your service: company registries and government authorities, registered agents, company secretaries, address providers and professional partners in the relevant country, our payment processors (Stripe and Airwallex), and our website and form host (Netlify). We don't sell your data."]),
 ("International transfers", ["Because we form companies in other countries, your data is sent to the country of your company and to our partners there."]),
 ("How long we keep it", ["We keep your records for as long as needed to provide the service and to meet legal record-keeping duties, normally up to 7 years after our work ends."]),
 ("Your rights", ["Under Malaysia's Personal Data Protection Act 2010 you can ask to access or correct your personal data, or to limit how we use it. Email <span class=\"ltr\">info@wizz.com.my</span>.", "If you live in the UK or the European Union, you also have rights under the UK GDPR or the EU GDPR, including asking us to delete your data, and you can complain to your local data protection authority."]),
 ("Security", ["We limit access to your data to the people who need it and use secure services to store and send it."]),
])

# ---------------- nav + footer links on every page
# Payment methods shown in the footer. Keep this in line with what is switched on in Stripe.
PAY_METHODS = ["Visa", "Mastercard", "UnionPay", "Apple Pay", "Google Pay", "Link", "FPX", "GrabPay"]
PAY_ROW = ('      <div class="pay-row"><span class="pay-label" data-i18n="pay_secure">Secure payments by Stripe</span>'
           '<ul class="pay-list" aria-label="Accepted payment methods">' + "".join(f'<li>{m}</li>' for m in PAY_METHODS) + '</ul></div>\n')
LEGAL_COL = """      <div><h4 data-i18n="nav_legal">Legal</h4><ul>
          <li><a href="terms.html" data-i18n="lg_terms">Terms of Service</a></li>
          <li><a href="refund.html" data-i18n="lg_refund">Refund Policy</a></li>
          <li><a href="privacy.html" data-i18n="lg_privacy">Privacy Policy</a></li>
        </ul></div>
"""
WA_PATH = "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"
WA_FLOAT = f"""<a class="wa-float" href="https://wa.me/601124477685?text=Hi%20Wizz%2C%20I%27d%20like%20to%20ask%20about%20your%20services." target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{WA_PATH}"/></svg><span class="wa-tip" data-i18n="wa_chat">Chat with us</span></a>
"""
for f in glob.glob(f"{D}/*.html"):
    s = open(f).read()
    if 'data-i18n="nav_pkgs"' not in s:
        cur = ' aria-current="page"' if f.endswith("/packages.html") else ""
        s = s.replace('<a href="services.html" data-i18n="nav_services"', f'<a href="packages.html"{cur} data-i18n="nav_pkgs">Packages</a>\n      <a href="services.html" data-i18n="nav_services"', 1)
    # footer: Legal column (replaces the old one-line links)
    s = s.replace('      <span class="legal-links"><a href="terms.html">Terms</a> · <a href="refund.html">Refunds</a> · <a href="privacy.html">Privacy</a></span>\n', '')
    if 'data-i18n="nav_legal"' not in s:
        s, n = re.subn(r'(        </ul></div>\n)(    </div>\n    <div class="legal">)', r'\1' + LEGAL_COL + r'\2', s, count=1)
        assert n == 1, f
    # accepted payment methods, above the copyright line
    if 'class="pay-row"' not in s:
        s = s.replace('    <div class="legal">\n', '    <div class="legal">\n' + PAY_ROW, 1)
    # floating WhatsApp button on every page
    if 'class="wa-float"' not in s:
        s = s.replace("</body>", WA_FLOAT + "</body>", 1)
    # the hero CTA on home now points to packages as a second option
    open(f, "w").write(s)

# Arabic label for the new nav item
js = open(f"{D}/site.js").read()
if '"pay_secure"' not in js:
    js = js.replace('"nav_mp": ', '"pay_secure": "دفع آمن عبر Stripe", "nav_mp": ', 1)
    assert '"pay_secure"' in js
    open(f"{D}/site.js", "w").write(js)
if '"nav_legal"' not in js:
    js = js.replace('"nav_mp": ', '"nav_legal": "قانوني", "lg_terms": "شروط الخدمة", "lg_refund": "سياسة الاسترداد", "lg_privacy": "سياسة الخصوصية", "wa_chat": "تواصل معنا", "nav_mp": ', 1)
    assert '"nav_legal"' in js
    open(f"{D}/site.js", "w").write(js)
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
.pk-curbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:22px;font-size:14px}
.pk-curbar label{font-weight:600;margin:0;display:inline}
.pk-curbar select{width:auto;max-width:100%;min-width:0;margin:0;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);font:inherit;font-size:14px}
.pk-curnote{color:var(--muted);font-size:13px}
footer.site{padding-bottom:96px}
.pay-row{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;padding-bottom:6px}
.pay-label{display:inline-flex;align-items:center;gap:6px;font-weight:600;color:color-mix(in srgb,var(--on-ink) 80%,transparent)}
.pay-label::before{content:"";width:12px;height:12px;background:currentColor;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 1a5 5 0 0 0-5 5v4H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5zm-3 9V6a3 3 0 1 1 6 0v4z'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 1a5 5 0 0 0-5 5v4H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5zm-3 9V6a3 3 0 1 1 6 0v4z'/%3E%3C/svg%3E") center/contain no-repeat}
.pay-list{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.pay-list li{background:#fff;color:#1F2328;border-radius:5px;padding:4px 9px;font:700 12px/1.2 var(--body);letter-spacing:.01em}
footer.site .foot{grid-template-columns:1.4fr repeat(4,1fr)}
@media (max-width:1000px){footer.site .foot{grid-template-columns:1fr 1fr}}
@media (max-width:560px){footer.site .foot{grid-template-columns:1fr}}
.wa-float{position:fixed;inset-inline-end:20px;bottom:20px;z-index:60;display:flex;align-items:center;gap:10px;height:56px;padding:0 16px;border-radius:999px;background:#25D366;color:#fff;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.18);transition:transform .2s ease,box-shadow .2s ease}
.wa-float svg{width:28px;height:28px;flex:none}
.wa-float .wa-tip{font:600 15px var(--body);white-space:nowrap}
.wa-float:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgba(0,0,0,.22)}
.wa-float:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
@media (max-width:640px){.wa-float{width:56px;padding:0;justify-content:center;right:16px;bottom:16px}.wa-float .wa-tip{display:none}}
@media print{.wa-float{display:none}}
[dir=rtl] .pk-flag,[dir=rtl] .pk-price .from{letter-spacing:0;font-family:var(--body);text-transform:none}
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
# v6 is the last block in site.css: replace it on every build so CSS edits apply
css = css.split("\n/* ===== v6: packages")[0].rstrip("\n") + "\n"
open(f"{D}/site.css", "w").write(css + CSS)

# sitemap
pages = sorted(os.path.basename(p) for p in glob.glob(f"{D}/*.html") if not p.endswith("thank-you.html"))
open(f"{D}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>https://wizz.com.my/{"" if p=="index.html" else p}</loc></url>\n' for p in pages) + "</urlset>\n")
print("built", pages)
