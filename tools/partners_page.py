# Public B2B page (partners.html): office prices for business-service offices. Runs inside build_pkgs.py after careers_page.py.
# Applications go to netlify/functions/partner.mjs (action "apply"). Wizz adds offices after KYC in Admin → Partners.
PTX = [
 ("Partner offices (B2B)", "مكاتب شريكة (B2B)", "Pejabat rakan kongsi (B2B)"),
 ("Office prices for your clients' companies abroad", "أسعار مكاتب لشركات عملائك في الخارج", "Harga pejabat untuk syarikat pelanggan anda di luar negara"),
 ("For business-service offices, consultants and accountants in Saudi Arabia, Oman and the Gulf. Offer your clients companies in the US, UK, Europe, Malaysia and more, at partner prices, while we do the work behind you.",
  "للمكاتب الخدمية والاستشارية والمحاسبية في السعودية وعُمان والخليج. قدّم لعملائك شركات في أمريكا وبريطانيا وأوروبا وماليزيا وغيرها بأسعار الشركاء، ونحن ننجز العمل من خلفك.",
  "Untuk pejabat perkhidmatan perniagaan, perunding dan akauntan di Arab Saudi, Oman dan Teluk. Tawarkan pelanggan anda syarikat di AS, UK, Eropah, Malaysia dan lain-lain pada harga rakan kongsi, sementara kami melakukan kerja di belakang anda."),
 ("Apply to become a partner", "قدّم طلب الشراكة", "Mohon menjadi rakan kongsi"),
 ("Partner prices for every service", "أسعار شركاء لكل الخدمات", "Harga rakan kongsi untuk setiap perkhidmatan"),
 ("We deal only with your office", "نتعامل مع مكتبك فقط", "Kami berurusan dengan pejabat anda sahaja"),
 ("Online portal with invoices", "بوابة إلكترونية مع الفواتير", "Portal dalam talian dengan invois"),
 ("Pay by bank transfer or USDT", "الدفع بالتحويل البنكي أو USDT", "Bayar melalui pindahan bank atau USDT"),
 ("Your partner account", "حساب الشريك", "Akaun rakan kongsi anda"),
 ("After KYC", "بعد التحقق", "Selepas KYC"),
 ("What you get", "ما تحصل عليه", "Apa yang anda dapat"),
 ("Everything your office needs to sell international company services", "كل ما يحتاجه مكتبك لبيع خدمات الشركات الدولية", "Semua yang pejabat anda perlukan untuk menjual perkhidmatan syarikat antarabangsa"),
 ("Office price list", "قائمة أسعار المكاتب", "Senarai harga pejabat"),
 ("See your partner prices for company formation in 15 countries, established companies and add-on services. You set your own price for your client.", "اطّلع على أسعار الشركاء لتأسيس الشركات في 15 دولة، والشركات القائمة، والخدمات الإضافية. وأنت تحدد سعرك لعميلك.", "Lihat harga rakan kongsi untuk penubuhan syarikat di 15 negara, syarikat sedia ada dan perkhidmatan tambahan. Anda menetapkan harga sendiri untuk pelanggan anda."),
 ("White-label service", "خدمة باسم مكتبك", "Perkhidmatan label putih"),
 ("Your client stays your client. We don't contact them, and all documents come back to your office.", "عميلك يبقى عميلك. لا نتواصل معه، وكل المستندات تعود إلى مكتبك.", "Pelanggan anda kekal pelanggan anda. Kami tidak menghubungi mereka, dan semua dokumen dikembalikan ke pejabat anda."),
 ("Orders and documents in one place", "الطلبات والمستندات في مكان واحد", "Pesanan dan dokumen di satu tempat"),
 ("Place an order for each client, upload their documents and follow every step online.", "قدّم طلباً لكل عميل، وارفع مستنداته، وتابع كل خطوة عبر الإنترنت.", "Buat pesanan untuk setiap pelanggan, muat naik dokumen mereka dan ikuti setiap langkah dalam talian."),
 ("Invoices and statements", "الفواتير وكشوف الحساب", "Invois dan penyata"),
 ("Every order gets an invoice, and you can print an account statement for any period.", "لكل طلب فاتورة، ويمكنك طباعة كشف حساب لأي فترة.", "Setiap pesanan mendapat invois, dan anda boleh mencetak penyata akaun untuk sebarang tempoh."),
 ("How it works", "كيف تعمل الشراكة", "Cara ia berfungsi"),
 ("From application to your first order", "من الطلب إلى أول طلب لعميلك", "Dari permohonan ke pesanan pertama anda"),
 ("Apply", "قدّم الطلب", "Mohon"),
 ("Fill in the form below with your office details.", "املأ النموذج أدناه ببيانات مكتبك.", "Isi borang di bawah dengan butiran pejabat anda."),
 ("KYC check", "التحقق (KYC)", "Semakan KYC"),
 ("We verify your office: commercial registration, the owner's or manager's ID and your office address.", "نتحقق من مكتبك: السجل التجاري، وهوية المالك أو المدير، وعنوان المكتب.", "Kami mengesahkan pejabat anda: pendaftaran perniagaan, ID pemilik atau pengurus, dan alamat pejabat."),
 ("Your account opens", "يُفتح حسابك", "Akaun anda dibuka"),
 ("We create your partner account and email you the sign-in steps.", "ننشئ حساب الشريك ونرسل لك خطوات الدخول بالبريد.", "Kami mencipta akaun rakan kongsi anda dan menghantar langkah log masuk melalui e-mel."),
 ("Order for your clients", "اطلب لعملائك", "Buat pesanan untuk pelanggan anda"),
 ("Place orders, pay each invoice by bank transfer or USDT, and we start the work.", "قدّم الطلبات، وادفع كل فاتورة بالتحويل البنكي أو USDT، ونبدأ العمل.", "Buat pesanan, bayar setiap invois melalui pindahan bank atau USDT, dan kami mulakan kerja."),
 ("Apply now", "قدّم الآن", "Mohon sekarang"),
 ("Partner application", "طلب الشراكة", "Permohonan rakan kongsi"),
 ("We reply within two business days to arrange KYC.", "نرد خلال يومي عمل لترتيب إجراءات التحقق.", "Kami membalas dalam masa dua hari bekerja untuk mengatur KYC."),
 ("Company name", "اسم المكتب / الشركة", "Nama syarikat"),
 ("Your name", "اسمك", "Nama anda"),
 ("Email", "البريد الإلكتروني", "E-mel"),
 ("WhatsApp / phone", "واتساب / الهاتف", "WhatsApp / telefon"),
 ("Country", "الدولة", "Negara"),
 ("City", "المدينة", "Bandar"),
 ("Commercial registration number (optional)", "رقم السجل التجاري (اختياري)", "Nombor pendaftaran perniagaan (pilihan)"),
 ("Which services do your clients ask for?", "ما الخدمات التي يطلبها عملاؤك؟", "Perkhidmatan apa yang diminta oleh pelanggan anda?"),
 ("e.g. US LLC, UK company, established companies, bank accounts", "مثال: شركة أمريكية، شركة بريطانية، شركات قائمة، حسابات بنكية", "cth. LLC AS, syarikat UK, syarikat sedia ada, akaun bank"),
 ("Clients per month (estimate)", "عدد العملاء شهرياً (تقديري)", "Pelanggan sebulan (anggaran)"),
 ("Just starting", "في البداية", "Baru bermula"),
 ("Message (optional)", "رسالة (اختياري)", "Mesej (pilihan)"),
 ("Send application", "أرسل الطلب", "Hantar permohonan"),
 ("Please fill in the highlighted fields.", "يرجى تعبئة الحقول المحددة.", "Sila isi ruangan yang ditandakan."),
 ("Sorry, something went wrong. Please try again, or message us on WhatsApp.", "عذراً، حدث خطأ. حاول مرة أخرى، أو راسلنا عبر واتساب.", "Maaf, berlaku ralat. Sila cuba lagi, atau hantar mesej kepada kami di WhatsApp."),
 ("Application received", "استلمنا طلبك", "Permohonan diterima"),
 ("Thank you. We'll contact you within two business days to complete KYC, then open your partner account.", "شكراً لك. سنتواصل معك خلال يومي عمل لإكمال التحقق، ثم نفتح حساب الشريك.", "Terima kasih. Kami akan menghubungi anda dalam masa dua hari bekerja untuk melengkapkan KYC, kemudian membuka akaun rakan kongsi anda."),
 ("Already a partner?", "شريك بالفعل؟", "Sudah menjadi rakan kongsi?"),
 ("Sign in to the partner portal", "ادخل إلى بوابة الشركاء", "Log masuk ke portal rakan kongsi"),
 ("Partner questions", "أسئلة الشركاء", "Soalan rakan kongsi"),
 ("Who can become a partner?", "من يمكنه أن يصبح شريكاً؟", "Siapa boleh menjadi rakan kongsi?"),
 ("Registered offices that serve business clients: business-service and PRO offices, consultants, accountants, law and travel offices. We open accounts after KYC.", "المكاتب المرخّصة التي تخدم عملاء الأعمال: مكاتب الخدمات والتعقيب، والاستشاريون، والمحاسبون، ومكاتب المحاماة والسفر. نفتح الحسابات بعد التحقق.", "Pejabat berdaftar yang melayani pelanggan perniagaan: pejabat perkhidmatan perniagaan dan PRO, perunding, akauntan, pejabat guaman dan pelancongan. Kami membuka akaun selepas KYC."),
 ("Can I see the prices before applying?", "هل يمكنني رؤية الأسعار قبل التقديم؟", "Bolehkah saya melihat harga sebelum memohon?"),
 ("Partner prices are shown in the portal after KYC. If you need an idea first, message us on WhatsApp.", "تظهر أسعار الشركاء في البوابة بعد التحقق. وإن احتجت فكرة مسبقة، راسلنا عبر واتساب.", "Harga rakan kongsi ditunjukkan dalam portal selepas KYC. Jika anda perlukan gambaran dahulu, hantar mesej WhatsApp kepada kami."),
 ("How do I pay?", "كيف أدفع؟", "Bagaimana saya membayar?"),
 ("Each order gets an invoice. Pay by bank transfer or USDT (TRC-20). We start the work once payment and the client's documents are received.", "لكل طلب فاتورة، والدفع بالتحويل البنكي أو USDT (شبكة TRC-20). نبدأ العمل بعد استلام الدفع ومستندات العميل.", "Setiap pesanan mendapat invois. Bayar melalui pindahan bank atau USDT (TRC-20). Kami mulakan kerja selepas bayaran dan dokumen pelanggan diterima."),
 ("Do you guarantee bank accounts or approvals?", "هل تضمنون الحسابات البنكية أو الموافقات؟", "Adakah anda menjamin akaun bank atau kelulusan?"),
 ("No. Banks, payment providers, marketplaces and governments make their own decisions. We prepare complete applications. Please don't promise approvals to your clients.", "لا. البنوك ومزودو الدفع والمنصات والجهات الحكومية تتخذ قراراتها بنفسها. نحن نجهّز طلبات كاملة. يرجى عدم وعد عملائك بالموافقات.", "Tidak. Bank, penyedia pembayaran, pasaran dalam talian dan kerajaan membuat keputusan sendiri. Kami menyediakan permohonan lengkap. Sila jangan menjanjikan kelulusan kepada pelanggan anda."),
]
for en, ar, ms in PTX:
    AR_SRC.setdefault(en, ar)
_msx = json.load(open(_ms_path)); _ch = False
for en, ar, ms in PTX:
    if en not in _msx: _msx[en] = ms; _ch = True
if _ch: json.dump(_msx, open(_ms_path, "w"), ensure_ascii=False, indent=0)

PB_WA = "https://wa.me/601124477685?text=" + urllib.parse.quote("Hi Wizz, our office would like to become a partner.")
pb_hero = x_hero("B2B", "Partner offices (B2B)", "Office prices for your clients' companies abroad",
    "For business-service offices, consultants and accountants in Saudi Arabia, Oman and the Gulf. Offer your clients companies in the US, UK, Europe, Malaysia and more, at partner prices, while we do the work behind you.",
    PB_WA, ("#apply", "Apply to become a partner"),
    ["Partner prices for every service", "We deal only with your office", "Online portal with invoices", "Pay by bank transfer or USDT"],
    "Your partner account", "Partner offices (B2B)",
    [("Office price list", "Partner prices for every service", 0), ("White-label service", "We deal only with your office", 0), ("Invoices and statements", "Pay by bank transfer or USDT", 0)], price="After KYC")
pb_feats = "".join(f'<article class="jw">{T("h3", h)}{T("p", p)}</article>' for h, p in [
    ("Office price list", "See your partner prices for company formation in 15 countries, established companies and add-on services. You set your own price for your client."),
    ("White-label service", "Your client stays your client. We don't contact them, and all documents come back to your office."),
    ("Orders and documents in one place", "Place an order for each client, upload their documents and follow every step online."),
    ("Invoices and statements", "Every order gets an invoice, and you can print an account statement for any period.")])
pb_steps = "".join(f'<li>{T("h3", h)}{T("p", p)}</li>' for h, p in [
    ("Apply", "Fill in the form below with your office details."),
    ("KYC check", "We verify your office: commercial registration, the owner's or manager's ID and your office address."),
    ("Your account opens", "We create your partner account and email you the sign-in steps."),
    ("Order for your clients", "Place orders, pay each invoice by bank transfer or USDT, and we start the work.")])
def _pl(id_, en): return f'<label for="{id_}"{tk(en)}>{esc(en)}</label>'
pb_form = f'''<form id="pbForm" class="pb-form" novalidate>
  <p hidden><label>Leave this empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>
  <div>{_pl("pb_co", "Company name")}<input id="pb_co" name="company" maxlength="150" required autocomplete="organization"></div>
  <div>{_pl("pb_name", "Your name")}<input id="pb_name" name="name" maxlength="120" required autocomplete="name"></div>
  <div>{_pl("pb_email", "Email")}<input id="pb_email" name="email" type="email" dir="ltr" maxlength="200" required autocomplete="email"></div>
  <div>{_pl("pb_phone", "WhatsApp / phone")}<input id="pb_phone" name="phone" type="tel" dir="ltr" maxlength="60" required autocomplete="tel"></div>
  <div>{_pl("pb_country", "Country")}<input id="pb_country" name="country" maxlength="80" required autocomplete="country-name"></div>
  <div>{_pl("pb_city", "City")}<input id="pb_city" name="city" maxlength="80"></div>
  <div>{_pl("pb_cr", "Commercial registration number (optional)")}<input id="pb_cr" name="cr" dir="ltr" maxlength="60"></div>
  <div>{_pl("pb_vol", "Clients per month (estimate)")}<select id="pb_vol" name="volume"><option value="Just starting"{tk("Just starting")}>Just starting</option><option value="1-5">1–5</option><option value="6-20">6–20</option><option value="20+">20+</option></select></div>
  <div class="full">{_pl("pb_svc", "Which services do your clients ask for?")}<input id="pb_svc" name="services" maxlength="500" placeholder="e.g. US LLC, UK company, established companies, bank accounts"{kph("e.g. US LLC, UK company, established companies, bank accounts")}></div>
  <div class="full">{_pl("pb_msg", "Message (optional)")}<textarea id="pb_msg" name="message" maxlength="2000" rows="3"></textarea></div>
  <div class="full formfoot"><button class="btn solid" type="submit"><span class="dot"></span>{T("span", "Send application")}</button></div>
  {T("p", "Please fill in the highlighted fields.", "err full pb-e1")}
  {T("p", "Sorry, something went wrong. Please try again, or message us on WhatsApp.", "err full pb-e2")}
</form>
<div class="out" id="pbOut" hidden role="status" tabindex="-1"><span class="out-ic">{CHECK}</span>{T("h2", "Application received", "out-t")}{T("p", "Thank you. We'll contact you within two business days to complete KYC, then open your partner account.", "out-p")}</div>'''
pb_faq_html, pb_ld = x_faq([
 ("Who can become a partner?", "Registered offices that serve business clients: business-service and PRO offices, consultants, accountants, law and travel offices. We open accounts after KYC."),
 ("Can I see the prices before applying?", "Partner prices are shown in the portal after KYC. If you need an idea first, message us on WhatsApp."),
 ("How do I pay?", "Each order gets an invoice. Pay by bank transfer or USDT (TRC-20). We start the work once payment and the client's documents are received."),
 ("Do you guarantee bank accounts or approvals?", "No. Banks, payment providers, marketplaces and governments make their own decisions. We prepare complete applications. Please don't promise approvals to your clients.")])
PB_JS = r"""<script>
(function(){
  const f=document.getElementById('pbForm'),e1=f.querySelector('.pb-e1'),e2=f.querySelector('.pb-e2');
  const ok=v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  f.addEventListener('input',e=>e.target.classList.remove('bad'));
  f.addEventListener('submit',async e=>{e.preventDefault();e1.hidden=e2.hidden=true;
    const bad=[...f.querySelectorAll('[required]')].filter(x=>!x.value.trim()||(x.type==='email'&&!ok(x.value.trim())));
    f.querySelectorAll('.bad').forEach(x=>x.classList.remove('bad'));bad.forEach(x=>x.classList.add('bad'));
    if(bad.length){e1.hidden=false;bad[0].focus();return;}
    const d=Object.fromEntries(new FormData(f));d.action='apply';d.lang=document.documentElement.lang||'en';
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{const r=await fetch('/.netlify/functions/partner',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)});const j=await r.json().catch(()=>({}));if(!r.ok||!j.ok)throw 0;
      f.hidden=true;const o=document.getElementById('pbOut');o.hidden=false;o.scrollIntoView({behavior:'smooth',block:'start'});o.focus({preventScroll:true});
      if(window.gtag)gtag('event','generate_lead',{form:'b2b_partner'});}
    catch(_){e2.hidden=false;}finally{b.disabled=false;}
  });
})();
</script>"""
pb_body = pb_hero + f'''
<p class="us-disc wrap"><span{tk(DISC)}>{esc(DISC)}</span></p>
<section class="block">
  <div class="wrap">
    {head("What you get", "Everything your office needs to sell international company services")}
    <div class="jw-grid">{pb_feats}</div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("How it works", "From application to your first order")}
    <ol class="steps us-steps jb-steps">{pb_steps}</ol>
  </div>
</section>
<section class="block" id="apply">
  <div class="wrap jb-wrap">
    {head("Apply now", "Partner application", "We reply within two business days to arrange KYC.")}
    {pb_form}
    <p class="pb-in">{T("span", "Already a partner?")} <a href="partner.html">{T("span", "Sign in to the partner portal")}</a></p>
  </div>
</section>
<section class="block alt">
  <div class="wrap faq-layout">
    <div>{T("p", "Partner offices (B2B)", "eyebrow")}{T("h2", "Partner questions")}</div>
    <div class="faq">{pb_faq_html}</div>
  </div>
</section>
{x_final("Apply to become a partner", "We reply within two business days to arrange KYC.", PB_WA)}'''
for _c in ("err full pb-e1", "err full pb-e2"):
    pb_body = pb_body.replace(f'class="{_c}"', f'class="{_c}" hidden')
page("partners.html", "Partner Offices (B2B): Office Prices for Company Formation | Wizz Smart Services",
     "For business-service offices in Saudi Arabia, Oman and the Gulf: partner prices for company formation in 15 countries, white-label service, an online portal, invoices and payment by bank transfer or USDT.",
     pb_body, extra_head=f'<script type="application/ld+json">{pb_ld}</script>', scripts=ar_script() + PB_JS)

US_CSS += """
.pb-form .bad{border-color:var(--red)!important;box-shadow:0 0 0 1px var(--red)}
.pb-form .err{margin:0}
.pb-in{margin-top:18px;font-size:15px}
#pbOut{scroll-margin-top:96px}
/* partner portal */
.pt-gate{max-width:640px}
.pt-stats{margin:18px 0}
.pt-body{margin-top:16px}
.pt-sub{margin:18px 0 14px}
.ac-pkg small{display:block;color:var(--muted);font-size:13px;font-weight:400}
.pt-items{width:100%;border-collapse:collapse;margin:12px 0;font-size:14.5px}
.pt-items td{padding:8px 4px;border-bottom:1px solid var(--line)}
.pt-items td:not(:first-child){text-align:end;white-space:nowrap}
.pt-items tfoot td{font-weight:700;border:0}
.pt-acts{margin:6px 0 14px;flex-wrap:wrap}
.pt-prices{width:100%;border-collapse:collapse;font-size:15px}
.pt-prices td{padding:9px 4px;border-bottom:1px solid var(--line);vertical-align:top}
.pt-prices td small{display:block;color:var(--muted);font-size:13px}
.pt-prices td:nth-child(2){text-align:end;white-space:nowrap;font-weight:700}
.pt-prices td:last-child{text-align:end;width:1%}
.pt-new{display:flex;flex-direction:column;gap:16px}
.pt-new .wz-box{margin:0}
.pt-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.pt-grid label{display:flex;flex-direction:column;gap:6px;font-weight:600;font-size:13.5px}
.pt-grid .full{grid-column:1/-1}
.pt-cat{margin:14px 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
[dir="rtl"] .pt-cat{letter-spacing:0}
.pt-pick{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.pt-pick li{display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;border:1px solid var(--line);border-radius:var(--r);padding:8px 10px;background:var(--surface)}
.pt-pick li.on{border-color:var(--ink);box-shadow:inset 3px 0 0 var(--red)}
.pt-pick li.off{opacity:.45}
.pt-pick b{white-space:nowrap}
.pt-qty{display:inline-flex;align-items:center;gap:6px}
.pt-qty button{width:30px;height:30px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:6px;font:700 16px var(--body);cursor:pointer}
.pt-qty button:disabled{opacity:.4;cursor:default}
.pt-qty em{min-width:18px;text-align:center;font-style:normal;font-weight:700}
.pt-pay{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:8px}
.pt-pay label{display:flex;gap:8px;align-items:center;font-weight:600}
.pt-pay input{width:auto}
.pt-total{font-size:20px;margin:10px 0}
.pt-s-submitted{background:#FFF4D6;color:#7a5600}.pt-s-invoiced{background:#FDE2E2;color:#9b1c1c}.pt-s-paid,.pt-s-in_progress{background:#E3EEFF;color:#1d4ed8}.pt-s-completed{background:#DFF5E6;color:#17663a}.pt-s-cancelled{background:#eee;color:#666}
.pt-oform{display:grid;grid-template-columns:auto 1fr auto auto;gap:10px;align-items:end}
.pt-oform label{display:flex;flex-direction:column;gap:4px;font-size:13px;font-weight:600}
.pt-oform .pt-chk{flex-direction:row;align-items:center;gap:6px;font-weight:500}
.pt-oform .pt-chk input{width:auto}
.pt-ptable input,.pt-ptable select{padding:6px 8px;font-size:14px}
.pt-ptable .pt-n{min-width:220px;margin-bottom:4px}
@media (max-width:760px){.pt-grid{grid-template-columns:1fr}.pt-oform{grid-template-columns:1fr}.pt-pick li{grid-template-columns:1fr auto}.pt-pick b{grid-column:1}}
"""
