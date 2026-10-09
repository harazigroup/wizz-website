#!/usr/bin/env python3
"""Adds Packages, Thank-you and legal pages to /home/claude/wizz-dist using about.html as the template."""
import re, html, glob, os, json
from catalog import COUNTRIES, ADDONS, ADDON_SKUS

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
def money(usd, fix=None):
    fx_attr = f" data-fix='{json.dumps(fix)}'" if fix else ""
    return f'<span class="m" data-usd="{usd}"{fx_attr}>${usd:,}</span>'
def money_text(txt):
    return re.sub(r"\$([0-9][0-9,]*)", lambda m: money(int(m.group(1).replace(",", ""))), esc(txt))

def tier_html(c, t):
    if t["p"] is None:
        price = f'<div class="pk-price"{tk("Quote")}>Quote</div>'
    else:
        price = f'<div class="pk-price">{f'<span class="from"{tk("from")}>from</span>' if t.get("frm") else ""}{money(t["p"], t.get("fix"))}<small class="cur">USD</small></div>'
    if t.get("sku") and t.get("deposit"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}"><span{tk("Add")}>Add</span> {money(t["deposit"])} <span{tk("deposit to cart")}>deposit to cart</span></button>'
    elif t.get("sku"):
        cta = f'<button class="btn solid pk-buy" type="button" data-sku="{t["sku"]}"{tk("Add to cart")}>Add to cart</button>'
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

def grp_html(c):
    out = ""
    for g, (title, lede) in c.get("groups", {}).items():
        ts = [t for t in c["tiers"] if t.get("grp") == g]
        out += f'''<div class="pk-sub"><h3{tk(title)}>{esc(title)}</h3><p{tk(lede)}>{esc(lede)}</p></div>
    <div class="pk-grid pk-grid-sm">{"".join(tier_html(c, t) for t in ts)}</div>'''
    return out
tabs, panels = [], []
for idx, c in enumerate(COUNTRIES):
    k = c["c"].lower()
    sel = "true" if idx == 0 else "false"
    tabs.append(f'<button type="button" role="tab" id="tab-{k}" aria-controls="p-{k}" aria-selected="{sel}" tabindex="{0 if idx==0 else -1}" data-k="{k}"><b class="ltr">{c["c"]}</b><span{tk(c["n"])}>{esc(c["n"])}</span></button>')
    notes = "".join(f'<p class="pk-note"{tk(n, money_text)}>{money_text(n)}</p>' for n in c["notes"])
    if k == "us": notes += f'<a class="pk-guide" href="usa.html"><span{tk("Everything about forming a US company")}>Everything about forming a US company</span> <span aria-hidden="true">→</span></a>'
    panels.append(f'''<div class="pk-panel" role="tabpanel" id="p-{k}" aria-labelledby="tab-{k}"{'' if idx==0 else ' hidden'}>
    <div class="pk-head"><span class="pk-code ltr">{c["c"]}<i>.</i></span><div><h2{tk(c["n"])}>{esc(c["n"])}</h2><p{tk(c["e"])}>{esc(c["e"])}</p></div></div>
    <div class="pk-grid">{"".join(tier_html(c, t) for t in c["tiers"] if not t.get("grp"))}</div>
    {grp_html(c)}
    {notes}
  </div>''')
def addon_html(a, p):
    btn = f'<button class="pk-add pk-buy" type="button" data-sku="{ADDON_SKUS[a][0]}"{tk("Add")}>Add</button>' if a in ADDON_SKUS else ""
    return f'<div class="pk-addon"><span{tk(a)}>{esc(a)}</span><span class="pk-addon-r"><b{tk(p, money_text)}>{money_text(p)}</b>{btn}</span></div>'
addons = "".join(addon_html(a, p) for a, p in ADDONS)

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

PK_JS = '''<script>
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
  function local(usd,c,fix){if(fix&&fix[c]!=null)return fix[c];const r=FX&&FX.rates[c];if(!r||c==='USD')return usd;const raw=usd*r.rate*(1+FX.buffer);const up=Math.ceil(raw/r.step)*r.step;return r.nine?up-1:up;}
  function fmt(n,c){const d=Number.isInteger(n)?0:2;try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol',maximumFractionDigits:d,minimumFractionDigits:d}).format(n)}catch(e){return c+' '+n.toLocaleString('en-US')}}
  function apply(c){cur=(FX&&FX.rates[c])?c:'USD';
    document.querySelectorAll('.m[data-usd]').forEach(el=>{el.textContent=fmt(local(+el.dataset.usd,cur,el.dataset.fix?JSON.parse(el.dataset.fix):null),cur)});
    document.querySelectorAll('.pk-price .cur').forEach(el=>{const shown=el.previousElementSibling?el.previousElementSibling.textContent:'';el.textContent=/[A-Z]{3}/.test(shown)?'':cur;});
    cs.value=cur;document.dispatchEvent(new CustomEvent('wizz:fx',{detail:{fx:FX,cur:cur}}));note.textContent=cur==='USD'?T('Set in US dollars. Change the currency if you prefer.','الأسعار بالدولار الأمريكي، ويمكنك تغيير العملة.'):T('Converted from our US dollar prices at a recent rate. You pay exactly this amount in '+cur+'.','محوّلة من أسعارنا بالدولار الأمريكي حسب سعر صرف حديث، وتدفع هذا المبلغ نفسه بعملة '+cur+'.');}
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
  document.querySelectorAll('.pk-buy').forEach(btn=>btn.addEventListener('click',()=>{if(window.WizzCart)window.WizzCart.add(btn.dataset.sku);else location.href='checkout.html?sku='+encodeURIComponent(btn.dataset.sku)+'&cur='+encodeURIComponent(cur);}));
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
                            "amount": t.get("deposit") or t["p"], "currency": "USD", **({"fixed": t["fix"]} if t.get("fix") and not t.get("deposit") else {}),
                            "desc": checkout_desc(t)[:480], "image": f'https://wizz.com.my/img/pay/{c["c"].lower()}.png'}
for a, (sku, usd) in ADDON_SKUS.items():
    SERVER[sku] = {"name": a, "amount": usd, "currency": "USD", "desc": "Add-on service. Approval of any account is decided by the provider.", "image": ""}
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
      <p class="muted">We use these details to check eligibility and prepare your filings. You can upload passport copies securely in your client account.</p>
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
    <div class="ty-acct" id="tyAcct" hidden><h2>Your client account</h2><p>Follow your order, upload your passport copy and other documents securely, and download your company documents when they're ready. Sign in with the email you paid with.</p><a class="btn solid" id="tyAcctBtn" href="account.html"><span class="dot"></span>Open my account</a></div>
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
    if(d.paid){if(sid){const a=document.getElementById('tyAcct');a.hidden=false;if(d.email)document.getElementById('tyAcctBtn').href='account.html?email='+encodeURIComponent(d.email);}try{if(window.WizzCart)window.WizzCart.clear();else localStorage.removeItem('wizz-cart')}catch(e){}st.className='ty-status ok';st.textContent=T('Payment received: ','تم استلام الدفع: ')+(d.package||T('your package','باقتك'))+' · '+d.currency+' '+Number(d.amount).toLocaleString('en-US')+' · '+T('Order ','رقم الطلب ')+d.order_id;showForm(d);}
    else{st.innerHTML=T('Your payment isn\\'t confirmed yet (status: '+(d.status||'unknown')+'). If you completed it, refresh in a minute or message us on WhatsApp at <span class="ltr">+60 11-2447 7685</span>.','لم يتم تأكيد الدفع بعد (الحالة: '+(d.status||'غير معروفة')+'). إذا أكملت الدفع، حدّث الصفحة بعد دقيقة أو راسلنا على واتساب على الرقم <span class="ltr">+60 11-2447 7685</span>.');}
  }).catch(()=>{st.innerHTML=T('We couldn\\'t check the payment right now. Fill in the form below and we\\'ll match it to your payment.','تعذّر التحقق من الدفع الآن. املأ النموذج أدناه وسنطابقه مع دفعتك.');showForm({});});
  f.addEventListener('submit',async e=>{e.preventDefault();if(!f.reportValidity())return;
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{const fd=new FormData(f);const r=await fetch('/',{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded'},body:new URLSearchParams(fd).toString()});if(!r.ok)throw 0;
      if(sid){try{await fetch('/.netlify/functions/onboarding',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({session_id:sid,data:Object.fromEntries(fd)})});}catch(_){}}
      f.hidden=true;document.getElementById('tyDone').hidden=false;}
    catch(_){b.disabled=false;st.textContent=T('We couldn\\'t send the form. Please try again or email info@wizz.com.my.','تعذّر إرسال النموذج. حاول مرة أخرى أو راسلنا على info@wizz.com.my.');}
  });
})();
</script>
'''
page("thank-you.html", "Thank you | Wizz Smart Services", "Payment confirmation and onboarding.", ty_body, scripts=ar_script() + TY_JS,
     extra_head='<meta name="robots" content="noindex">')

# ---------------- cart (cart.js on every page): stored in the visitor's browser, prices shown in their currency
CART_DATA = {}
for c in COUNTRIES:
    for t in c["tiers"]:
        if t.get("sku"):
            dep = bool(t.get("deposit"))
            CART_DATA[t["sku"]] = {"c": c["c"], "n": [f'{c["n"]} · {t["n"]}' + (" (deposit)" if dep else ""), f'{AR_SRC[c["n"]]} · {AR_SRC[t["n"]]}' + (" (عربون)" if dep else "")],
                                   "usd": t.get("deposit") or t["p"], "max": 1, **({"fix": t["fix"]} if t.get("fix") and not t.get("deposit") else {})}
for a, (sku, usd) in ADDON_SKUS.items():
    CART_DATA[sku] = {"c": "", "n": [a, AR_SRC[a]], "usd": usd, "max": 10}
CART_JS = "/* Wizz cart: generated by tools/build_pkgs.py, do not edit by hand */\n(function(){\n  const DATA=" + json.dumps(CART_DATA, ensure_ascii=False) + r""";
  const KEY='wizz-cart';
  const ar=()=>document.documentElement.lang==='ar';const T=(en,a)=>ar()?a:en;
  function read(){try{const v=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v.filter(x=>x&&DATA[x.sku]).map(x=>({sku:x.sku,qty:Math.max(1,Math.min(DATA[x.sku].max,x.qty|0||1))})):[]}catch(e){return []}}
  let items=read();
  function save(){try{localStorage.setItem(KEY,JSON.stringify(items))}catch(e){}render();}
  let FX=null,cur='USD';try{cur=localStorage.getItem('wizz-cur')||'USD'}catch(e){}
  function local(usd,fix){if(fix&&fix[cur]!=null)return fix[cur];const r=FX&&FX.rates[cur];if(!r||cur==='USD')return usd;const raw=usd*r.rate*(1+FX.buffer);const up=Math.ceil(raw/r.step)*r.step;return r.nine?up-1:up;}
  function fmt(n){const c=(FX&&FX.rates[cur])?cur:'USD';try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol',maximumFractionDigits:Number.isInteger(n)?0:2,minimumFractionDigits:Number.isInteger(n)?0:2}).format(n)}catch(e){return c+' '+n}}
  function loadFx(){if(FX||loadFx.busy)return;loadFx.busy=1;fetch('/.netlify/functions/prices').then(r=>r.ok?r.json():null).then(d=>{if(!d)return;FX=d;let s=null;try{s=localStorage.getItem('wizz-cur')}catch(e){}cur=(s&&d.rates[s])?s:d.currency;render();}).catch(()=>{});}
  document.addEventListener('wizz:fx',e=>{FX=e.detail.fx;cur=e.detail.cur;render();});
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  // header button
  const bag='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 8h14l-1.2 11.1a2 2 0 0 1-2 1.9H8.2a2 2 0 0 1-2-1.9L5 8zm4 0V6.5a3 3 0 0 1 6 0V8"/></svg>';
  const btn=document.createElement('button');btn.type='button';btn.className='cart-btn';btn.id='cartBtn';btn.innerHTML=bag+'<span class="cart-n" id="cartN" hidden>0</span>';
  const tools=document.querySelector('header.site .tools');if(tools)tools.insertBefore(btn,tools.firstChild);
  // drawer
  const wrap=document.createElement('div');wrap.className='cart-wrap';wrap.hidden=true;
  wrap.innerHTML='<div class="cart-scrim" data-close></div><aside class="cart" role="dialog" aria-modal="true" aria-labelledby="cartTitle"><div class="cart-top"><h2 id="cartTitle"></h2><button type="button" class="cart-x" data-close aria-label="Close">×</button></div><div class="cart-body" id="cartBody"></div><div class="cart-foot" id="cartFoot"></div></aside>';
  document.body.appendChild(wrap);
  let lastFocus=null;
  function open(){loadFx();lastFocus=document.activeElement;wrap.hidden=false;document.documentElement.classList.add('cart-open');render();setTimeout(()=>wrap.querySelector('.cart-x').focus(),30);}
  function close(){wrap.hidden=true;document.documentElement.classList.remove('cart-open');if(lastFocus&&lastFocus.focus)lastFocus.focus();}
  btn.addEventListener('click',open);
  wrap.addEventListener('click',e=>{if(e.target.closest('[data-close]'))close();const q=e.target.closest('[data-q]');if(q){const it=items.find(x=>x.sku===q.dataset.sku);if(it){it.qty=Math.max(1,Math.min(DATA[it.sku].max,it.qty+(+q.dataset.q)));save();}}const rm=e.target.closest('[data-rm]');if(rm){items=items.filter(x=>x.sku!==rm.dataset.rm);save();}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!wrap.hidden)close();});
  function render(){
    const n=items.reduce((a,x)=>a+x.qty,0);const badge=document.getElementById('cartN');badge.textContent=n;badge.hidden=!n;
    btn.setAttribute('aria-label',T('Cart','السلة')+(n?' ('+n+')':''));
    document.getElementById('cartTitle').textContent=T('Your cart','سلتك');
    wrap.querySelector('.cart-x').setAttribute('aria-label',T('Close','إغلاق'));
    const body=document.getElementById('cartBody'),foot=document.getElementById('cartFoot');
    if(!items.length){body.innerHTML='<p class="cart-empty">'+T('Your cart is empty.','سلتك فارغة.')+'</p>';foot.innerHTML='<a class="btn ghost" href="packages.html">'+T('Browse packages','تصفّح الباقات')+'</a>';return;}
    let total=0;
    body.innerHTML='<ul class="cart-list">'+items.map(x=>{const d=DATA[x.sku];const line=Math.round(local(d.usd,d.fix)*x.qty*100)/100;total=Math.round((total+line)*100)/100;
      const code=d.c?'<span class="cart-code ltr">'+d.c+'<i>.</i></span>':'<span class="cart-code plus">+</span>';
      const qty=d.max>1?'<span class="cart-qty"><button type="button" data-q="-1" data-sku="'+x.sku+'" aria-label="'+T('Fewer','أقل')+'">−</button><b>'+x.qty+'</b><button type="button" data-q="1" data-sku="'+x.sku+'" aria-label="'+T('More','أكثر')+'">+</button></span>':'';
      return '<li>'+code+'<div class="cart-info"><b>'+esc(d.n[ar()?1:0])+'</b><span class="cart-row">'+qty+'<button type="button" class="cart-rm" data-rm="'+x.sku+'">'+T('Remove','إزالة')+'</button></span></div><span class="cart-price ltr">'+fmt(line)+'</span></li>';}).join('')+'</ul>';
    foot.innerHTML='<div class="cart-total"><span>'+T('Total','الإجمالي')+'</span><b class="ltr">'+fmt(total)+'</b></div><a class="btn solid cart-go" href="checkout.html?cart=1&cur='+encodeURIComponent((FX&&FX.rates[cur])?cur:'USD')+'"><span class="dot"></span>'+T('Checkout','إتمام الطلب')+'</a><p class="cart-fine">'+T('Prices include government filing fees unless a note says otherwise.','تشمل الأسعار الرسوم الحكومية ما لم تذكر الملاحظة غير ذلك.')+'</p>';
  }
  document.addEventListener('wizz:lang',render);
  window.WizzCart={
    add(sku){if(!DATA[sku])return;const it=items.find(x=>x.sku===sku);if(it){if(it.qty<DATA[sku].max)it.qty++;}else items.push({sku,qty:1});save();open();},
    items(){return items.map(x=>({...x}))},
    clear(){items=[];save();}
  };
  render();
})();
"""
open(f"{D}/cart.js", "w").write(CART_JS)

# ---------------- checkout page: our order summary + Stripe's embedded payment form
CK_DATA = {}
for c in COUNTRIES:
    for t in c["tiers"]:
        if not t.get("sku"): continue
        CK_DATA[t["sku"]] = {"c": c["c"], "n": [c["n"], AR_SRC[c["n"]]], "t": [t["n"], AR_SRC[t["n"]]],
            "plus": [t["plus"], AR_SRC[t["plus"]]] if t.get("plus") else None,
            "i": [t["i"], [AR_SRC[x] for x in t["i"]]], "dep": bool(t.get("deposit"))}
for a_, (sku, usd) in ADDON_SKUS.items():
    CK_DATA[sku] = {"c": "", "n": [a_, AR_SRC[a_]], "t": None, "plus": None, "i": None, "dep": False, "addon": True}
LOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 1a5 5 0 0 0-5 5v4H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5zm-3 9V6a3 3 0 1 1 6 0v4z"/></svg>'
ck_body = f"""<section class="block ck">
  <div class="wrap ck-grid">
    <aside class="ck-sum" aria-labelledby="ckTitle">
      <a class="ck-back" href="packages.html"{tk("All packages")}>All packages</a>
      <p class="eyebrow"{tk("Secure checkout")}>Secure checkout</p>
      <h1 class="ck-title" id="ckTitle"{tk("Order summary")}>Order summary</h1>
      <ul class="ck-lines" id="ckLines"></ul>
      <div class="ck-totalrow"><span{tk("Total")}>Total</span><b id="ckTotal" class="ltr">…</b></div>
    </aside>
    <div class="ck-more">
      <h2 class="ck-h"{tk("What happens next")}>What happens next</h2>
      <ol class="ck-steps">
        <li{tk("You pay securely on this page.")}>You pay securely on this page.</li>
        <li{tk("You fill in a short onboarding form.")}>You fill in a short onboarding form.</li>
        <li{tk("We confirm everything with you before anything is filed.")}>We confirm everything with you before anything is filed.</li>
      </ol>
      <div class="ck-trust">
        <p>{LOCK}<span{tk("Payments are processed by Stripe. We never see your full card details.")}>Payments are processed by Stripe. We never see your full card details.</span></p>
        <p><a href="refund.html"{tk("Refund Policy")}>Refund Policy</a> · <a href="terms.html"{tk("Terms of Service")}>Terms of Service</a> · <a href="https://wa.me/601124477685" target="_blank" rel="noopener"{tk("Questions? WhatsApp us")}>Questions? WhatsApp us</a></p>
      </div>
    </div>
    <div class="ck-pay">
      <div class="ck-loading" id="ckLoading"><span class="ck-spin" aria-hidden="true"></span><span{tk("Loading secure payment form…")}>Loading secure payment form…</span></div>
      <div id="ckForm"></div>
      <div class="pk-msg" id="ckMsg" role="status" hidden></div>
    </div>
  </div>
</section>"""
CK_JS = """<script>
(function(){
  const DATA=""" + json.dumps(CK_DATA, ensure_ascii=False) + r""";
  const qs=new URLSearchParams(location.search);const cur=(qs.get('cur')||'USD').toUpperCase();
  let list=[];
  if(qs.get('sku')){list=[{sku:qs.get('sku'),qty:1}];}
  else{try{const v=JSON.parse(localStorage.getItem('wizz-cart')||'[]');if(Array.isArray(v))list=v.map(x=>({sku:x.sku,qty:Math.max(1,Math.min(10,x.qty|0||1))}));}catch(e){}}
  list=list.filter(x=>DATA[x.sku]);
  if(!list.length){location.replace('packages.html');return;}
  const ar=()=>document.documentElement.lang==='ar';const L=a=>a?a[ar()?1:0]:'';const T=(en,a)=>ar()?a:en;
  const $=id=>document.getElementById(id);let res=null;
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function fmt(n,c){try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol',maximumFractionDigits:2,minimumFractionDigits:Number.isInteger(n)?0:2}).format(n)}catch(e){return c+' '+n}}
  function render(){
    $('ckLines').innerHTML=list.map(x=>{const d=DATA[x.sku];const line=res&&res.lines?res.lines.find(l=>l.sku===x.sku):null;
      const code=d.c?'<span class="cart-code ltr">'+d.c+'<i>.</i></span>':'<span class="cart-code plus">+</span>';
      const name=d.addon?esc(L(d.n)):esc(L(d.t))+(d.dep?' · '+T('deposit','عربون'):'')+'<small>'+esc(L(d.n))+'</small>';
      const inc=d.i?'<ul class="ck-items">'+(d.plus?'<li class="ck-plus">'+esc(L(d.plus))+'</li>':'')+L(d.i).map(i=>'<li>'+esc(i)+'</li>').join('')+'</ul>':'';
      const dep=d.dep?'<p class="ck-dep">'+T('Credited to your final package price.','يُخصم من السعر النهائي لباقتك.')+'</p>':'';
      return '<li><div class="ck-line">'+code+'<div class="ck-name"><b>'+name+'</b>'+(x.qty>1?'<span class="ck-qty">× '+x.qty+'</span>':'')+'</div><span class="ck-amt ltr">'+(line?fmt(line.amount,res.currency):'')+'</span></div>'+dep+inc+'</li>';}).join('');
    $('ckTotal').textContent=res?fmt(res.amount,res.currency):'…';
    document.title=T('Checkout','إتمام الطلب')+' | Wizz Smart Services';
  }
  document.addEventListener('wizz:lang',render);render();
  function fail(msg){$('ckLoading').hidden=true;const m=$('ckMsg');m.innerHTML=msg;m.hidden=false;}
  const WA='<span class="ltr">+60 11-2447 7685</span>';
  async function start(embedded){
    const r=await fetch('/.netlify/functions/checkout',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({items:list,currency:cur,embedded})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok)throw Object.assign(new Error('server'),{code:j.error});
    return j;
  }
  function loadStripe(){return new Promise((ok,no)=>{if(window.Stripe)return ok();const s=document.createElement('script');s.src='https://js.stripe.com/dahlia/stripe.js';s.onload=()=>window.Stripe?ok():no(new Error('Stripe.js did not start'));s.onerror=()=>no(new Error('Stripe.js could not load'));document.head.appendChild(s);});}
  function remember(j){try{sessionStorage.setItem('wizz-order',JSON.stringify({order:j.order_id,pkg:j.package}))}catch(e){}}
  (async()=>{
    let j;
    try{j=await start(true);}catch(e){
      return fail(e.code==='not_configured'?T('Online payment is being set up. Message us on WhatsApp at '+WA+' and we will send you a payment link.','الدفع الإلكتروني قيد الإعداد. راسلنا على واتساب على الرقم '+WA+' وسنرسل لك رابط الدفع.'):T('We couldn\'t open the checkout. Please try again, or message us on WhatsApp at '+WA+'.','تعذّر فتح صفحة الدفع. حاول مرة أخرى، أو راسلنا على واتساب على الرقم '+WA+'.'));
    }
    res=j;render();remember(j);
    if(j.url){location.replace(j.url);return;}
    if(!j.embedded){return fail(T('Please message us on WhatsApp at '+WA+' to complete your payment.','راسلنا على واتساب على الرقم '+WA+' لإكمال الدفع.'));}
    try{
      await loadStripe();
      const stripe=window.Stripe(j.publishable_key);
      const make=stripe.createEmbeddedCheckoutPage||stripe.initEmbeddedCheckout;
      if(!make)throw new Error('This Stripe.js has no embedded checkout');
      const page=await make.call(stripe,{fetchClientSecret:()=>Promise.resolve(j.client_secret)});
      page.mount('#ckForm');$('ckLoading').hidden=true;
    }catch(e){
      console.error('Embedded checkout failed:',e);
      $('ckLoading').hidden=true;const m=$('ckMsg');m.textContent=T('Opening Stripe\'s secure payment page…','جارٍ فتح صفحة الدفع الآمنة من Stripe…')+' ('+String(e&&e.message||e).slice(0,140)+')';m.hidden=false;
      setTimeout(async()=>{try{const h=await start(false);remember(h);if(h.url){location.replace(h.url);return;}}catch(_){}
        fail(T('We couldn\'t load the payment form. Please refresh, or message us on WhatsApp at '+WA+'.','تعذّر تحميل نموذج الدفع. حدّث الصفحة، أو راسلنا على واتساب على الرقم '+WA+'.'));},2500);
    }
  })();
})();
</script>
"""
page("checkout.html", "Checkout | Wizz Smart Services", "Secure checkout for Wizz Smart Services packages.", ck_body, scripts=ar_script() + CK_JS,
     extra_head='<meta name="robots" content="noindex">')

# ---------------- client account + team admin (Supabase)
import shutil
SB_JS = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.117.2/dist/umd/supabase.js"></script>\n'
for n in ("account.js", "admin.js"):
    shutil.copy(f"{D}/tools/portal/{n}", f"{D}/{n}")
ac_body = f"""<section class="block ac">
  <div class="wrap ac-wrap">
    <div class="ac-loading" id="acLoading"><span class="ck-spin" aria-hidden="true"></span></div>
    <div class="ac-msg bad" id="acErr" hidden></div>
    <div class="ac-card ac-signin" id="acOutBox" hidden></div>
    <div id="acIn" hidden>
      <div class="ac-top">
        <div><p class="eyebrow"{tk("Client account")}>Client account</p><h1{tk("Your orders")}>Your orders</h1><p class="muted"><span{tk("Signed in as")}>Signed in as</span> <b id="acWho" class="ltr"></b></p></div>
        <div class="ac-actions"><a class="btn ghost small" id="acAdmin" href="admin.html" hidden>Team admin</a><button class="btn ghost small" id="acPwBtn" type="button"{tk("Change password")}>Change password</button><button class="btn ghost small" id="acOut" type="button"{tk("Sign out")}>Sign out</button></div>
      </div>
      <div class="ac-card ac-pw" id="acPw" hidden></div>
      <div id="acOrders" class="ac-orders"></div>
      <p class="ac-privacy"{tk('Your files are stored privately in the EU and only you and our team can open them. See our <a href="privacy.html">Privacy Policy</a>.', RAW)}>Your files are stored privately in the EU and only you and our team can open them. See our <a href="privacy.html">Privacy Policy</a>.</p>
    </div>
  </div>
</section>"""
page("account.html", "My account | Wizz Smart Services", "Sign in to follow your order and share documents securely.", ac_body,
     scripts=ar_script() + SB_JS + '<script src="account.js" defer></script>\n', extra_head='<meta name="robots" content="noindex">')

ad_body = """<section class="block ac">
  <div class="wrap">
    <div class="ac-msg" id="adMsg" hidden></div>
    <div class="ac-card" id="adGate" hidden></div>
    <div id="adApp" hidden>
      <div class="ac-top"><div><p class="eyebrow">Team</p><h1>Orders</h1><p class="muted">Signed in as <b id="adWho"></b></p></div><div class="ac-actions"><button class="btn ghost small" id="adOut" type="button">Sign out</button></div></div>
      <details class="ad-new" id="adNewBox"><summary>Add an order paid outside the website</summary>
        <form id="adNew" class="ad-form"><input name="email" type="email" required placeholder="Client email"><input name="name" placeholder="Client name"><input name="package" required placeholder="Package, e.g. United Kingdom - Business"><input name="amount" type="number" step="0.01" min="0" required placeholder="Amount"><select name="currency"><option>USD</option><option>GBP</option><option>EUR</option><option>MYR</option><option>AED</option><option>SAR</option><option>OMR</option><option>THB</option></select><button class="btn solid small" type="submit">Add order</button></form></details>
      <div class="ad-grid">
        <div class="ad-side"><div class="ad-filter"><input id="adQ" placeholder="Search ref, email, name"><select id="adF"><option value="">All statuses</option><option value="paid">Paid</option><option value="docs_needed">Documents needed</option><option value="review">Under review</option><option value="filed">Filed</option><option value="registered">Company registered</option><option value="delivered">Delivered</option><option value="on_hold">On hold</option><option value="cancelled">Cancelled</option></select></div><p class="ad-count" id="adCount"></p><div id="adList" class="ad-list"></div></div>
        <div class="ad-detail" id="adDetail"><p class="ac-none">Select an order.</p></div>
      </div>
    </div>
  </div>
</section>"""
page("admin.html", "Team admin | Wizz Smart Services", "Team admin.", ad_body,
     scripts=SB_JS + '<script src="admin.js" defer></script>\n', extra_head='<meta name="robots" content="noindex">')

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "us_page.py")).read())

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
 ("Who we share it with", ["Only as needed to deliver your service: company registries and government authorities, registered agents, company secretaries, address providers and professional partners in the relevant country, our payment processors (Stripe and Airwallex), our website and form host (Netlify), and our client-account database and file storage (Supabase, hosted in the EU). We don't sell your data."]),
 ("Your client account", ["You sign in with your email and a password, or with a one-time link sent to your email. Passwords are stored only in hashed (encrypted) form, so no one at Wizz can read them. Documents you upload are kept in private storage in the European Union. Only you and the members of our team who handle your order can open them, and each download link expires after a minute.", "You can delete a file you uploaded at any time from your account, or ask us to delete your account and files by emailing <span class=\"ltr\">info@wizz.com.my</span>, unless the law requires us to keep them."]),
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
    if 'class="acct-btn"' not in s:
        s = s.replace('<button class="lang" id="langBtn"', '<a class="acct-btn" href="account.html" aria-label="My account" title="My account"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm-7 8a7 7 0 0 1 14 0"/></svg></a>\n      <button class="lang" id="langBtn"', 1)
    if 'src="cart.js"' not in s:
        s = s.replace('<script src="site.js"></script>', '<script src="cart.js"></script>\n<script src="site.js"></script>', 1)
    # countries page: every card links to its packages tab (and the US card to its guide)
    if f.endswith("/countries.html") and 'class="clinks"' not in s:
        s = s.replace('\n        <a class="clink" href="usa.html"><span data-i18n="us_guide">US company formation guide</span> <span aria-hidden="true">→</span></a>', "")
        def _links(m):
            k = m.group(1)
            guide = '<a class="clink" href="usa.html"><span data-i18n="us_guide">US company formation guide</span> <span aria-hidden="true">→</span></a>' if k == "us" else ""
            return m.group(0).replace("</article>", f'  <div class="clinks"><a class="clink" href="packages.html#{k}"><span data-i18n="see_pkgs">Packages & prices</span> <span aria-hidden="true">→</span></a>{guide}</div>\n      </article>', 1)
        s = re.sub(r'<article class="ccard"[^>]*id="c-([a-z]+)">.*?</article>', _links, s, flags=re.S)
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
.acct-btn{display:inline-grid;place-items:center;width:40px;height:40px;border:1px solid var(--line);border-radius:8px;color:var(--ink)}
.acct-btn svg{width:21px;height:21px}
.acct-btn:hover{background:var(--surface)}
.ac{padding-top:clamp(28px,4vw,48px)}
.ac-wrap{max-width:980px}
.ac-loading{display:grid;place-items:center;min-height:300px}
.ac-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:clamp(22px,4vw,40px);box-shadow:0 10px 40px rgba(16,24,40,.06)}
.ac-signin{max-width:520px;margin:0 auto}
.ac-tabs{display:flex;gap:4px;background:var(--surface);border-radius:9px;padding:4px;margin:18px 0 4px}
.ac-tabs button{flex:1;border:0;background:transparent;padding:9px 10px;border-radius:7px;font:600 14px var(--body);color:var(--muted);cursor:pointer}
.ac-tabs button[aria-selected="true"]{background:#fff;color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.ac-row{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:14px}
.ac-pw{max-width:520px;margin:0 0 18px}
.ac-pw h2{font:800 20px var(--display);margin:0 0 6px}
.ac-pwhint{font-size:12.5px;color:var(--muted);margin:-4px 0 0}
.ac-signin h1,.ac-top h1{font:800 clamp(28px,3.4vw,38px)/1.1 var(--display);margin:6px 0 10px}
.ac-form{display:grid;gap:10px;grid-template-columns:1fr!important;margin-top:18px}
.ac-form label{font-weight:600;font-size:14px}
.ac-msg{padding:12px 14px;border-radius:8px;font-size:14px;margin:0}
.ac-msg.bad{background:#FDECEC;color:#8A1C1C}.ac-msg.good{background:#E8F6EE;color:#1D6B3A}
.ac-sent{margin-top:18px}.ac-sent h2{font:800 22px var(--display);margin:0 0 6px}
.ac-link{border:0;background:none;padding:0;color:var(--ink);text-decoration:underline;cursor:pointer;font:inherit;font-size:14px}
.ac-link.danger{color:#B42318}
.ac-top{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:22px}
.ac-actions{display:flex;gap:8px}
.ac-orders{display:grid;gap:12px}
.ac-order{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.ac-head{all:unset;box-sizing:border-box;width:100%;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto;grid-template-areas:"ref pkg badge" "ref meta badge";gap:2px 16px;align-items:center;padding:16px 18px}
.ac-head:hover{background:var(--surface)}
.ac-head:focus-visible{outline:2px solid var(--ink);outline-offset:-2px}
.ac-ref{grid-area:ref;font:700 13px var(--mono);color:var(--muted)}
.ac-pkg{grid-area:pkg;font-weight:700}
.ac-meta{grid-area:meta;font-size:13.5px;color:var(--muted)}
.ac-badge{grid-area:badge;font:700 12px var(--body);padding:4px 10px;border-radius:999px;background:var(--surface);white-space:nowrap}
.ac-badge.s-paid,.ac-badge.s-review,.ac-badge.s-filed{background:#EAF0FB;color:#1E40AF}
.ac-badge.s-docs_needed,.ac-badge.s-on_hold{background:#FFF4E5;color:#92400E}
.ac-badge.s-registered,.ac-badge.s-delivered{background:#E8F6EE;color:#1D6B3A}
.ac-badge.s-cancelled{background:#F2F2F2;color:#555}
.ac-body{padding:4px 18px 20px;display:grid;gap:18px;border-top:1px solid var(--line)}
.ac-steps{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);gap:6px}
.ac-steps li{display:grid;gap:6px;font-size:12px;color:var(--muted)}
.ac-steps li span{height:6px;border-radius:3px;background:var(--line)}
.ac-steps li.done span{background:var(--ink)}
.ac-steps li.now span{background:var(--red)}
.ac-steps li.now em{color:var(--ink);font-weight:700}
.ac-steps em{font-style:normal}
.ac-steps.off{opacity:.45}
.ac-note{margin:0;padding:12px 14px;border-radius:8px;background:var(--surface);font-size:14.5px}
.ac-warn{margin:0;padding:12px 14px;border-radius:8px;background:#FFF4E5;color:#7A3E00;font-size:14px}
.ac-cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.ac-cols section,.ad-box{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:#fff}
.ac-body h3,.ad-box h3{font:700 15px var(--body);margin:0 0 8px}
.ac-hint{font-size:13px;color:var(--muted);margin:0 0 10px}
.ac-none{color:var(--muted);font-size:14px;margin:6px 0}
.ac-docs{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:8px}
.ac-docs li{display:flex;gap:12px;align-items:center;justify-content:space-between;border-bottom:1px dashed var(--line);padding-bottom:8px}
.ac-file{min-width:0;overflow-wrap:anywhere;font-size:14px}.ac-file small{display:block;color:var(--muted);font-size:12px}
.ac-up{cursor:pointer}
.ac-upmsg{font-size:13px;margin:8px 0 0}.ac-upmsg.bad{color:#B42318}.ac-upmsg.good{color:#1D6B3A}
.ac-ev ul,.ac-rem ul,.ad-ev{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:14px}
.ac-ev small,.ac-rem small,.ad-ev small{display:block;color:var(--muted);font-size:12px}
.ac-empty{background:#fff;border:1px solid var(--line);border-radius:12px;padding:28px;text-align:center}
.ac-empty h3{margin:0 0 6px}
.ac-privacy{font-size:13px;color:var(--muted);margin-top:20px}
@media (max-width:720px){.ac-cols{grid-template-columns:1fr}.ac-head{grid-template-columns:1fr auto;grid-template-areas:"pkg badge" "meta meta" "ref ref"}.ac-steps{grid-template-columns:repeat(3,1fr)}}
.ad-new{margin-bottom:16px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.ad-new summary{cursor:pointer;font-weight:600}
.ad-form{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.ad-form input,.ad-form select{width:auto;flex:1 1 160px}
.ad-grid{display:grid;grid-template-columns:minmax(260px,360px) 1fr;gap:18px;align-items:start}
.ad-filter{display:grid;gap:8px}
.ad-count{font-size:13px;color:var(--muted);margin:8px 0}
.ad-list{display:grid;gap:6px;max-height:70vh;overflow:auto}
.ad-row{all:unset;box-sizing:border-box;cursor:pointer;display:grid;gap:2px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;font-size:14px}
.ad-row.on{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.ad-row small{color:var(--muted);font-size:12px}.ad-row .ac-badge{justify-self:start}
.ad-pk{color:var(--muted)}
.ad-detail{display:grid;gap:12px}
.ad-top{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.ad-top h2{margin:0;font:800 24px var(--display)}.ad-top p{margin:2px 0}
.ad-sub{font-size:14px;color:var(--muted)}
.ad-amt{font:850 26px var(--display);text-align:end}.ad-amt small{display:block;font:500 13px var(--body);color:var(--muted)}
.ad-lbl{display:grid;gap:6px;font-size:13px;margin:12px 0 8px}
.ad-dl{display:grid;grid-template-columns:200px 1fr;gap:6px 12px;font-size:14px;margin:0}
.ad-dl dt{color:var(--muted)}.ad-dl dd{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
.ad-rems{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:14px}
.ad-rems input{width:auto;margin-inline-end:6px}
.ad-row .ac-badge{grid-area:auto}
.ac-file{flex:1}
.ac-docs li .ac-link{flex:none}
body[data-page="admin"] .wa-float{display:none}
@media (max-width:860px){.ad-grid{grid-template-columns:1fr}.ad-dl{grid-template-columns:1fr}}
.cart-btn{position:relative;display:inline-grid;place-items:center;width:40px;height:40px;border:1px solid var(--line);border-radius:8px;background:transparent;color:var(--ink);cursor:pointer}
.cart-btn svg{width:21px;height:21px}
.cart-btn:hover{background:var(--surface)}
.cart-n{position:absolute;top:-6px;inset-inline-end:-6px;min-width:19px;height:19px;padding:0 5px;border-radius:999px;background:var(--red);color:#fff;font:700 11px/19px var(--body);text-align:center}
.cart-wrap{position:fixed;inset:0;z-index:80}
.cart-scrim{position:absolute;inset:0;background:rgba(15,18,22,.42);animation:cfade .2s ease}
.cart{position:absolute;top:0;bottom:0;inset-inline-end:0;width:min(420px,100%);background:var(--bg,#fff);color:var(--ink);display:flex;flex-direction:column;box-shadow:-12px 0 40px rgba(0,0,0,.15);animation:cslide .25s ease}
[dir=rtl] .cart{box-shadow:12px 0 40px rgba(0,0,0,.15);animation-name:cslider}
@keyframes cfade{from{opacity:0}}@keyframes cslide{from{transform:translateX(30px);opacity:.6}}@keyframes cslider{from{transform:translateX(-30px);opacity:.6}}
.cart-top{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;border-bottom:1px solid var(--line)}
.cart-top h2{margin:0;font:800 20px var(--display)}
.cart-x{width:36px;height:36px;border:0;background:transparent;font-size:26px;line-height:1;color:var(--muted);cursor:pointer;border-radius:8px}
.cart-x:hover{background:var(--surface);color:var(--ink)}
.cart-body{flex:1;overflow:auto;padding:8px 20px}
.cart-empty{color:var(--muted);padding:30px 0}
.cart-list{list-style:none;margin:0;padding:0}
.cart-list li{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:start;padding:16px 0;border-bottom:1px solid var(--line)}
.cart-code{display:flex;align-items:center;justify-content:center;flex:none;width:46px;height:46px;border-radius:8px;background:var(--surface);font:900 17px var(--display);font-stretch:120%}
.cart-code i{font-style:normal;color:var(--red)}
.cart-code.plus{font-size:22px;color:var(--muted)}
.cart-info b{display:block;font-size:14.5px;line-height:1.35}
.cart-row{display:flex;gap:12px;align-items:center;margin-top:8px}
.cart-qty{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:7px}
.cart-qty button{width:28px;height:28px;border:0;background:transparent;cursor:pointer;font-size:16px;color:var(--ink)}
.cart-qty b{min-width:20px;text-align:center;font-size:13px}
.cart-rm{border:0;background:none;padding:0;color:var(--muted);text-decoration:underline;cursor:pointer;font-size:13px}
.cart-price{font:700 15px var(--body);white-space:nowrap}
.cart-foot{padding:16px 20px 20px;border-top:1px solid var(--line);display:grid;gap:12px}
.cart-total{display:flex;justify-content:space-between;align-items:baseline;font-size:15px}
.cart-total b{font:850 24px var(--display)}
.cart-go{justify-content:center;width:100%}
.cart-fine{margin:0;font-size:12px;color:var(--muted)}
html.cart-open{overflow:hidden}
.pk-addon:has(.pk-add){flex-direction:column;align-items:stretch;justify-content:space-between}
.pk-addon-r{display:flex;align-items:center;justify-content:space-between;gap:10px}
.pk-add{border:1px solid var(--ink);background:var(--ink);color:var(--on-ink);border-radius:6px;padding:5px 12px;font:600 13px var(--body);cursor:pointer}
.pk-add:hover{opacity:.88}
.ck{padding-top:clamp(28px,4vw,48px)}
.ck-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,520px);grid-template-areas:"sum pay" "more pay";column-gap:clamp(24px,4vw,56px);row-gap:22px;align-items:start;grid-template-rows:auto 1fr}
.ck-more{grid-area:more;display:grid;gap:14px;align-content:start}
.ck-pay{grid-area:pay}
.ck-sum{grid-area:sum;display:grid;gap:14px}
.ck-back{font-size:14px;color:var(--muted);text-decoration:none;width:fit-content}
.ck-back::before{content:"← "}
[dir=rtl] .ck-back::before{content:"→ "}
.ck-back:hover{color:var(--ink)}
.ck-head{display:flex;gap:16px;align-items:center}
.ck-title{font:800 clamp(26px,3vw,34px)/1.1 var(--display);margin:0}
.ck-lines{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.ck-lines>li{padding:16px 0;border-bottom:1px solid var(--line);display:grid;gap:10px}
.ck-line{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center}
.ck-name b{display:block;font-size:16px}
.ck-name small{display:block;font-weight:500;color:var(--muted);font-size:13.5px;margin-top:2px}
.ck-qty{font-size:13px;color:var(--muted)}
.ck-amt{font:700 16px var(--body);white-space:nowrap}
.ck-lines .ck-items{border-top:0;padding:0;padding-inline-start:58px;gap:6px}
.ck-lines .ck-items li{font-size:13.5px;color:var(--muted);padding-inline-start:22px}
.ck-lines .ck-items li::before{width:13px;height:13px;background-size:10px}
.ck-lines .ck-plus{font-style:italic;padding-inline-start:0!important}
.ck-lines .ck-plus::before{display:none}
.ck-lines .ck-dep{padding-inline-start:58px}
.ck-totalrow{display:flex;justify-content:space-between;align-items:baseline;padding-top:4px}
.ck-totalrow span{font-weight:600}
.ck-totalrow b{font:850 clamp(28px,3vw,36px)/1 var(--display);font-variant-numeric:tabular-nums}
.ck-head h1{font:800 clamp(26px,3vw,34px)/1.1 var(--display);margin:0}
.ck-head p{margin:4px 0 0;color:var(--muted)}
.ck-price{display:flex;align-items:baseline;gap:8px;font:850 clamp(34px,4vw,44px)/1 var(--display);font-variant-numeric:tabular-nums}
.ck-price small{font:500 14px var(--body);color:var(--muted)}
.ck-dep{margin:0;color:var(--muted);font-size:14px}
.ck-items{list-style:none;margin:0;padding:16px 0 0;border-top:1px solid var(--line);display:grid;gap:10px}
.ck-items li{position:relative;padding-inline-start:26px;font-size:15px}
.ck-items li::before{content:"";position:absolute;inset-inline-start:0;top:3px;width:16px;height:16px;border-radius:50%;background:var(--ink) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.2l2.4 2.4L12 5' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/12px no-repeat}
.ck-h{font:700 15px var(--body);margin:10px 0 0}
.ck-steps{margin:0;padding-inline-start:20px;display:grid;gap:6px;color:var(--muted);font-size:14.5px}
.ck-trust{border-top:1px solid var(--line);padding-top:14px;display:grid;gap:8px;font-size:13.5px;color:var(--muted)}
.ck-trust p{margin:0;display:flex;gap:8px;align-items:flex-start;flex-wrap:wrap}
.ck-trust svg{width:15px;height:15px;flex:none;margin-top:2px;color:var(--ink)}
.ck-trust a{color:inherit}
.ck-pay{background:#fff;border:1px solid var(--line);border-radius:14px;padding:clamp(8px,1.5vw,16px);box-shadow:0 10px 40px rgba(16,24,40,.06);min-height:420px}
.ck-loading{display:flex;align-items:center;justify-content:center;gap:12px;min-height:380px;color:var(--muted);font-size:15px}
.ck-spin{width:18px;height:18px;border:2px solid var(--line);border-top-color:var(--ink);border-radius:50%;animation:ckspin .8s linear infinite}
@keyframes ckspin{to{transform:rotate(360deg)}}
@media (max-width:900px){.ck-grid{grid-template-columns:1fr;grid-template-areas:"sum" "pay" "more";grid-template-rows:auto}}
body[data-page="checkout"] .wa-float .wa-tip{display:none}
body[data-page="checkout"] .wa-float{width:56px;padding:0;justify-content:center}
.g-label.g-uk{margin-left:-30px}
.g-label.g-nl{margin:-20px 0 0 2px}
.g-label.g-fr{margin-left:-30px}
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
.pk-sub{margin:40px 0 16px;padding-top:28px;border-top:1px dashed var(--line)}
.pk-sub h3{font-size:22px;margin:0 0 6px}
.pk-sub p{color:var(--muted);margin:0;max-width:44em}
.pk-grid-sm{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:900px){.pk-grid-sm{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.pk-grid-sm{grid-template-columns:1fr}}
.pk-grid-sm .pk h3{font-size:16px;line-height:1.3}
'''
css = open(f"{D}/site.css").read()
# v6 is the last block in site.css: replace it on every build so CSS edits apply
css = css.split("\n/* ===== v6: packages")[0].rstrip("\n") + "\n"
open(f"{D}/site.css", "w").write(css + CSS + US_CSS)

# sitemap
pages = sorted(os.path.basename(p) for p in glob.glob(f"{D}/*.html") if not p.endswith(("thank-you.html", "checkout.html", "account.html", "admin.html")))
open(f"{D}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>https://wizz.com.my/{"" if p=="index.html" else p}</loc></url>\n' for p in pages) + "</urlset>\n")
print("built", pages)
