# Refer & earn page (refer.html). Runs inside build_pkgs.py after extra_pages.py (uses its x_hero, x_faq, x_final, XMARK2).
# Programme rules live here, in netlify/functions/referral.mjs (emails) and checkout.mjs (REF_OFF_MYR / REF_MIN_MYR). Keep them in step.
RTX = [
 ("Refer & earn", "أحِل واربح", "Rujuk & peroleh"),
 ("Refer a friend. They save RM 100, you earn 10%.", "أحِل صديقاً: يوفّر 100 رينغيت، وتربح أنت 10%.", "Rujuk rakan. Mereka jimat RM 100, anda peroleh 10%."),
 ("Know someone who wants a company abroad, a bank account or a marketplace store? Share your Wizz code. Your friend gets RM 100 off, and you earn 10% of what they pay once their service is completed.",
  "تعرف شخصاً يريد شركة في الخارج أو حساباً بنكياً أو متجراً على المنصات؟ شارك رمزك من ويز. يحصل صديقك على خصم 100 رينغيت، وتربح أنت 10% مما يدفعه بعد إتمام خدمته.",
  "Kenal seseorang yang mahukan syarikat di luar negara, akaun bank atau kedai di pasaran dalam talian? Kongsi kod Wizz anda. Rakan anda mendapat RM 100 diskaun, dan anda memperoleh 10% daripada bayaran mereka selepas perkhidmatan mereka selesai."),
 ("Get my code", "احصل على رمزي", "Dapatkan kod saya"),
 ("Free to join, open to anyone", "الانضمام مجاني ومتاح للجميع", "Percuma untuk menyertai, terbuka kepada semua"),
 ("RM 100 off for your friend", "خصم 100 رينغيت لصديقك", "RM 100 diskaun untuk rakan anda"),
 ("10% for you on every paid client", "10% لك عن كل عميل يدفع", "10% untuk anda bagi setiap pelanggan yang membayar"),
 ("Track your referrals online", "تابع إحالاتك عبر الإنترنت", "Jejak rujukan anda dalam talian"),
 ("Your referral code", "رمز الإحالة الخاص بك", "Kod rujukan anda"),
 ("Share it anywhere", "شاركه في أي مكان", "Kongsi di mana-mana"),
 ("Free", "مجاناً", "Percuma"),
 ("Your friend gets", "يحصل صديقك على", "Rakan anda dapat"),
 ("RM 100 off", "خصم 100 رينغيت", "RM 100 diskaun"),
 ("You earn", "تربح أنت", "Anda peroleh"),
 ("10% of the sale", "10% من قيمة البيع", "10% daripada jualan"),
 ("Paid", "الصرف", "Dibayar"),
 ("After the service", "بعد إتمام الخدمة", "Selepas perkhidmatan"),
 ("Three steps", "ثلاث خطوات", "Tiga langkah"),
 ("Sign up, share your link, get paid", "سجّل، شارك رابطك، احصل على عمولتك", "Daftar, kongsi pautan, terima bayaran"),
 ("Sign up", "سجّل", "Daftar"),
 ("Fill in the form below. You get your code and link straight away, and by email.", "املأ النموذج أدناه. تحصل على رمزك ورابطك فوراً، وعبر البريد.", "Isi borang di bawah. Anda terima kod dan pautan serta-merta, dan melalui e-mel."),
 ("Share your link", "شارك رابطك", "Kongsi pautan anda"),
 ("Send it on WhatsApp, post it, or give friends your code to type in on our contact form or at checkout.", "أرسله عبر واتساب أو انشره، أو أعطِ أصدقاءك رمزك ليكتبوه في نموذج التواصل أو عند الدفع.", "Hantar di WhatsApp, siarkan, atau beri rakan kod anda untuk ditaip dalam borang hubungan atau semasa pembayaran."),
 ("Earn 10%", "اربح 10%", "Peroleh 10%"),
 ("When your friend pays and their service is completed, we approve your 10% and pay you.", "عندما يدفع صديقك وتكتمل خدمته، نعتمد عمولتك البالغة 10% ونحوّلها لك.", "Apabila rakan anda membayar dan perkhidmatan mereka selesai, kami meluluskan 10% anda dan membayar anda."),
 ("What your friend gets", "ما يحصل عليه صديقك", "Apa yang rakan anda dapat"),
 ("A welcome discount on their first order.", "خصم ترحيبي على أول طلب.", "Diskaun sambutan untuk pesanan pertama mereka."),
 ("RM 100 off orders of RM 1,000 or more", "خصم 100 رينغيت على الطلبات من 1,000 رينغيت فأكثر", "RM 100 diskaun untuk pesanan RM 1,000 ke atas"),
 ("Applied at checkout, or on their written quote", "يُطبَّق عند الدفع أو في عرض السعر المكتوب", "Digunakan semasa pembayaran, atau dalam sebut harga bertulis mereka"),
 ("For new clients, once per client", "للعملاء الجدد، مرة واحدة لكل عميل", "Untuk pelanggan baharu, sekali bagi setiap pelanggan"),
 ("What you earn", "ما تربحه", "Apa yang anda peroleh"),
 ("A real commission, not points.", "عمولة حقيقية، وليست نقاطاً.", "Komisen sebenar, bukan mata ganjaran."),
 ("10% of what your friend pays for our services", "10% مما يدفعه صديقك مقابل خدماتنا", "10% daripada bayaran rakan anda untuk perkhidmatan kami"),
 ("Approved once their service is completed", "تُعتمد بعد إتمام خدمته", "Diluluskan selepas perkhidmatan mereka selesai"),
 ("Paid by bank transfer, Wise or PayPal", "تُصرف بتحويل بنكي أو Wise أو PayPal", "Dibayar melalui pindahan bank, Wise atau PayPal"),
 ("No limit on how many friends you refer", "لا حد لعدد الأصدقاء الذين تحيلهم", "Tiada had bilangan rakan yang anda rujuk"),
 ("Join the programme", "انضم إلى البرنامج", "Sertai program"),
 ("Get your referral code", "احصل على رمز الإحالة", "Dapatkan kod rujukan anda"),
 ("It takes a minute. We email your code too, so you can find it later.", "يستغرق الأمر دقيقة. ونرسل رمزك بالبريد أيضاً لتجده لاحقاً.", "Ia mengambil masa seminit. Kami juga menghantar kod anda melalui e-mel, supaya anda boleh mencarinya kemudian."),
 ("Full name", "الاسم الكامل", "Nama penuh"),
 ("Email", "البريد الإلكتروني", "E-mel"),
 ("WhatsApp / phone (optional)", "واتساب / الهاتف (اختياري)", "WhatsApp / telefon (pilihan)"),
 ("Country of residence", "دولة الإقامة", "Negara kediaman"),
 ("How should we pay you?", "كيف نحوّل لك العمولة؟", "Bagaimana kami patut membayar anda?"),
 ("Bank transfer", "تحويل بنكي", "Pindahan bank"),
 ("Other", "أخرى", "Lain-lain"),
 ("Payment details (optional, you can send them later)", "بيانات الدفع (اختياري، يمكنك إرسالها لاحقاً)", "Butiran pembayaran (pilihan, boleh dihantar kemudian)"),
 ("I agree to the programme rules below.", "أوافق على شروط البرنامج أدناه.", "Saya bersetuju dengan peraturan program di bawah."),
 ("Create my code", "أنشئ رمزي", "Cipta kod saya"),
 ("Please fill in your name and a valid email, and accept the rules.", "يرجى إدخال اسمك وبريد صحيح، والموافقة على الشروط.", "Sila isi nama anda dan e-mel yang sah, dan terima peraturan."),
 ("Sorry, something went wrong. Please try again, or message us on WhatsApp.", "عذراً، حدث خطأ. حاول مرة أخرى، أو راسلنا عبر واتساب.", "Maaf, berlaku ralat. Sila cuba lagi, atau hantar mesej kepada kami di WhatsApp."),
 ("Your code is ready", "رمزك جاهز", "Kod anda sudah sedia"),
 ("Your link", "رابطك", "Pautan anda"),
 ("Copy link", "نسخ الرابط", "Salin pautan"),
 ("Share on WhatsApp", "شارك عبر واتساب", "Kongsi di WhatsApp"),
 ("We've also sent it to your email.", "وأرسلناه أيضاً إلى بريدك.", "Kami juga telah menghantarnya ke e-mel anda."),
 ("You're already registered", "أنت مسجّل بالفعل", "Anda sudah berdaftar"),
 ("We've emailed your code to you again. Check your inbox and spam folder.", "أرسلنا رمزك إلى بريدك مرة أخرى. تحقق من صندوق الوارد ومجلد الرسائل غير المرغوب فيها.", "Kami telah menghantar kod anda ke e-mel anda sekali lagi. Semak peti masuk dan folder spam."),
 ("Already a referrer?", "مسجّل بالفعل؟", "Sudah menjadi perujuk?"),
 ("Check your referrals", "تابع إحالاتك", "Semak rujukan anda"),
 ("Enter your code and the email you signed up with.", "أدخل رمزك والبريد الذي سجّلت به.", "Masukkan kod anda dan e-mel yang anda gunakan untuk mendaftar."),
 ("Your code", "رمزك", "Kod anda"),
 ("Show my referrals", "اعرض إحالاتي", "Tunjukkan rujukan saya"),
 ("We couldn't find that code with this email.", "لم نجد هذا الرمز مع هذا البريد.", "Kami tidak menemui kod itu dengan e-mel ini."),
 ("Enquiries", "الاستفسارات", "Pertanyaan"),
 ("Paid orders", "الطلبات المدفوعة", "Pesanan berbayar"),
 ("Commission", "العمولة", "Komisen"),
 ("Pending", "قيد الانتظار", "Belum selesai"),
 ("Approved", "معتمدة", "Diluluskan"),
 ("No commissions yet.", "لا توجد عمولات بعد.", "Belum ada komisen."),
 ("Programme rules", "شروط البرنامج", "Peraturan program"),
 ("Who can join?", "من يمكنه الانضمام؟", "Siapa boleh menyertai?"),
 ("Anyone aged 18 or over: clients, partners, friends, content creators. It's free.", "أي شخص عمره 18 عاماً فأكثر: العملاء والشركاء والأصدقاء وصنّاع المحتوى. والانضمام مجاني.", "Sesiapa yang berumur 18 tahun ke atas: pelanggan, rakan kongsi, kawan, pencipta kandungan. Ia percuma."),
 ("How is the commission calculated?", "كيف تُحسب العمولة؟", "Bagaimana komisen dikira?"),
 ("10% of the amount your friend actually pays us for our services, after their discount. Government fees we pass on at cost, refunds and cancelled orders don't earn commission.",
  "10% من المبلغ الذي يدفعه صديقك فعلاً مقابل خدماتنا، بعد الخصم. ولا تُحتسب عمولة على الرسوم الحكومية التي ننقلها بالتكلفة، ولا على الطلبات المستردة أو الملغاة.",
  "10% daripada jumlah yang sebenarnya dibayar oleh rakan anda untuk perkhidmatan kami, selepas diskaun. Yuran kerajaan yang kami caj pada kos, bayaran balik dan pesanan yang dibatalkan tidak layak untuk komisen."),
 ("When do I get paid?", "متى أحصل على عمولتي؟", "Bila saya akan dibayar?"),
 ("After your friend's service is completed, we approve the commission and pay it to the account you gave us. You can check the status any time on this page.",
  "بعد إتمام خدمة صديقك، نعتمد العمولة ونحوّلها إلى الحساب الذي زودتنا به. ويمكنك متابعة حالتها في أي وقت من هذه الصفحة.",
  "Selepas perkhidmatan rakan anda selesai, kami meluluskan komisen dan membayarnya ke akaun yang anda berikan. Anda boleh menyemak statusnya bila-bila masa di halaman ini."),
 ("How long does my link work?", "كم يبقى رابطي فعّالاً؟", "Berapa lama pautan saya berfungsi?"),
 ("Once a friend opens your link, we remember your code on their device for 60 days. They can also type your code on our contact form, at checkout, or tell us on WhatsApp.",
  "بعد أن يفتح صديقك رابطك، نحفظ رمزك على جهازه لمدة 60 يوماً. ويمكنه أيضاً كتابة رمزك في نموذج التواصل أو عند الدفع، أو إخبارنا به عبر واتساب.",
  "Sebaik rakan membuka pautan anda, kami mengingati kod anda pada peranti mereka selama 60 hari. Mereka juga boleh menaip kod anda dalam borang hubungan, semasa pembayaran, atau memberitahu kami di WhatsApp."),
 ("Can I use my own code?", "هل يمكنني استخدام رمزي بنفسي؟", "Bolehkah saya menggunakan kod saya sendiri?"),
 ("No. Self-referrals don't earn commission, and the discount is for new clients only, once per client.", "لا. لا تُحتسب عمولة على الإحالة الذاتية، والخصم للعملاء الجدد فقط، مرة واحدة لكل عميل.", "Tidak. Rujukan sendiri tidak layak untuk komisen, dan diskaun hanya untuk pelanggan baharu, sekali bagi setiap pelanggan."),
 ("What can't I say when I share?", "ما الذي لا يجوز قوله عند المشاركة؟", "Apa yang saya tidak boleh katakan semasa berkongsi?"),
 ("Please don't promise bank accounts, Stripe, marketplace approval, visas or residency. Those decisions belong to banks, platforms and governments. No spam, and don't pretend to be Wizz staff.",
  "يرجى عدم الوعد بحسابات بنكية أو Stripe أو قبول على المنصات أو تأشيرات أو إقامة، فهذه قرارات البنوك والمنصات والحكومات. ولا رسائل مزعجة، ولا تنتحل صفة موظفي ويز.",
  "Sila jangan menjanjikan akaun bank, Stripe, kelulusan pasaran, visa atau pemastautin. Keputusan itu milik bank, platform dan kerajaan. Jangan spam, dan jangan menyamar sebagai kakitangan Wizz."),
 ("Can the programme change?", "هل يمكن أن يتغير البرنامج؟", "Bolehkah program berubah?"),
 ("Yes. We can change or end the programme, or close a code that breaks these rules. Commissions already approved are always paid.", "نعم. يمكننا تعديل البرنامج أو إنهاؤه، أو إيقاف أي رمز يخالف هذه الشروط. وتُصرف دائماً العمولات المعتمدة مسبقاً.", "Ya. Kami boleh mengubah atau menamatkan program, atau menutup kod yang melanggar peraturan ini. Komisen yang telah diluluskan sentiasa dibayar."),
 ("Ready to start earning?", "مستعد لتبدأ الربح؟", "Bersedia untuk mula memperoleh?"),
 ("Get your code in a minute and share it with anyone planning a business abroad.", "احصل على رمزك خلال دقيقة وشاركه مع كل من يخطط لنشاط تجاري في الخارج.", "Dapatkan kod anda dalam seminit dan kongsikannya dengan sesiapa yang merancang perniagaan di luar negara."),
 ("Questions about the programme? Message us on WhatsApp.", "لديك أسئلة عن البرنامج؟ راسلنا عبر واتساب.", "Ada soalan tentang program? Hantar mesej kepada kami di WhatsApp."),
]
for en, ar, ms in RTX:
    AR_SRC.setdefault(en, ar)
_msx = json.load(open(_ms_path)); _ch = False
for en, ar, ms in RTX:
    if en not in _msx: _msx[en] = ms; _ch = True
if _ch: json.dump(_msx, open(_ms_path, "w"), ensure_ascii=False, indent=0)

RF_WA = "https://wa.me/601124477685?text=" + urllib.parse.quote("Hi Wizz, I have a question about the referral programme.")
rf_hero = x_hero("RM100", "Refer & earn", "Refer a friend. They save RM 100, you earn 10%.",
    "Know someone who wants a company abroad, a bank account or a marketplace store? Share your Wizz code. Your friend gets RM 100 off, and you earn 10% of what they pay once their service is completed.",
    RF_WA, ("#signup", "Get my code"),
    ["Free to join, open to anyone", "RM 100 off for your friend", "10% for you on every paid client", "Track your referrals online"],
    "Your referral code", "Share it anywhere",
    [("Your friend gets", "RM 100 off", 0), ("You earn", "10% of the sale", 0), ("Paid", "After the service", 1)], price="Free")
rf_steps = [("Sign up", "Fill in the form below. You get your code and link straight away, and by email."),
            ("Share your link", "Send it on WhatsApp, post it, or give friends your code to type in on our contact form or at checkout."),
            ("Earn 10%", "When your friend pays and their service is completed, we approve your 10% and pay you.")]
rf_steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}</li>' for h, p in rf_steps)
rf_ents = ent("What your friend gets", "A welcome discount on their first order.",
              ["RM 100 off orders of RM 1,000 or more", "Applied at checkout, or on their written quote", "For new clients, once per client"]) + \
          ent("What you earn", "A real commission, not points.",
              ["10% of what your friend pays for our services", "Approved once their service is completed", "Paid by bank transfer, Wise or PayPal", "No limit on how many friends you refer"])

def _lbl(id_, en, req=False):
    return f'<label for="{id_}"{tk(en)}>{esc(en)}</label>'
rf_form = f'''<form id="rfForm" class="rf-form" novalidate>
  <p hidden><label>Leave this empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>
  <div>{_lbl("rf_name", "Full name")}<input id="rf_name" name="name" autocomplete="name" required maxlength="120"></div>
  <div>{_lbl("rf_email", "Email")}<input id="rf_email" name="email" type="email" autocomplete="email" required maxlength="200"></div>
  <div>{_lbl("rf_phone", "WhatsApp / phone (optional)")}<input id="rf_phone" name="phone" type="tel" autocomplete="tel" maxlength="60"></div>
  <div>{_lbl("rf_country", "Country of residence")}<input id="rf_country" name="country" autocomplete="country-name" maxlength="80"></div>
  <div>{_lbl("rf_pay", "How should we pay you?")}<select id="rf_pay" name="payout_method">
      <option value="Bank transfer"{tk("Bank transfer")}>Bank transfer</option><option value="Wise">Wise</option><option value="PayPal">PayPal</option><option value="Other"{tk("Other")}>Other</option></select></div>
  <div>{_lbl("rf_pd", "Payment details (optional, you can send them later)")}<input id="rf_pd" name="payout_details" maxlength="300"></div>
  <label class="rf-agree full"><input type="checkbox" id="rf_ok"> <span{tk("I agree to the programme rules below.")}>I agree to the programme rules below.</span> <a href="#rules">↓</a></label>
  <div class="full formfoot"><button class="btn solid" type="submit"><span class="dot"></span>{T("span", "Create my code")}</button></div>
  {T("p", "Please fill in your name and a valid email, and accept the rules.", "err full")}
  {T("p", "Sorry, something went wrong. Please try again, or message us on WhatsApp.", "err full")}
</form>
<div class="rf-out" id="rfOk" hidden role="status" tabindex="-1">
  {T("p", "Your code is ready", "eyebrow")}
  <p class="rf-code ltr" id="rfCode"></p>
  {T("p", "Your link", "rf-lbl")}<p class="rf-link ltr" id="rfLink"></p>
  <div class="rf-act"><button type="button" class="btn ghost" id="rfCopy">{T("span", "Copy link")}</button><a class="btn wa" id="rfShare" target="_blank" rel="noopener">{T("span", "Share on WhatsApp")}</a></div>
  {T("p", "We've also sent it to your email.", "rf-note")}
</div>
<div class="rf-out" id="rfExists" hidden role="status" tabindex="-1">{T("h3", "You're already registered")}{T("p", "We've emailed your code to you again. Check your inbox and spam folder.")}</div>'''

rf_check = f'''<form id="stForm" class="rf-form rf-check" novalidate>
  <div>{_lbl("st_code", "Your code")}<input id="st_code" name="code" class="ref-in" maxlength="16" required autocomplete="off"></div>
  <div>{_lbl("st_email", "Email")}<input id="st_email" name="email" type="email" autocomplete="email" required></div>
  <div class="full formfoot"><button class="btn ghost" type="submit">{T("span", "Show my referrals")}</button></div>
  {T("p", "We couldn't find that code with this email.", "err full")}
</form>
<div class="rf-stats" id="stOut" hidden>
  <div><b id="stEnq">0</b>{T("span", "Enquiries")}</div>
  <div><b id="stOrd">0</b>{T("span", "Paid orders")}</div>
  <div class="rf-com"><span class="rf-com-h">{T("span", "Commission")}</span><ul id="stCom"></ul>{T("p", "No commissions yet.", "rf-none")}</div>
  <span hidden id="stL">{T("span", "Pending")}{T("span", "Approved")}{T("span", "Paid")}</span>
</div>'''

rf_faq_html, rf_ld = x_faq([
 ("Who can join?", "Anyone aged 18 or over: clients, partners, friends, content creators. It's free."),
 ("How is the commission calculated?", "10% of the amount your friend actually pays us for our services, after their discount. Government fees we pass on at cost, refunds and cancelled orders don't earn commission."),
 ("When do I get paid?", "After your friend's service is completed, we approve the commission and pay it to the account you gave us. You can check the status any time on this page."),
 ("How long does my link work?", "Once a friend opens your link, we remember your code on their device for 60 days. They can also type your code on our contact form, at checkout, or tell us on WhatsApp."),
 ("Can I use my own code?", "No. Self-referrals don't earn commission, and the discount is for new clients only, once per client."),
 ("What can't I say when I share?", "Please don't promise bank accounts, Stripe, marketplace approval, visas or residency. Those decisions belong to banks, platforms and governments. No spam, and don't pretend to be Wizz staff."),
 ("Can the programme change?", "Yes. We can change or end the programme, or close a code that breaks these rules. Commissions already approved are always paid.")])

RF_JS = r"""<script>
(function(){
  const $=id=>document.getElementById(id);
  const L=()=>document.documentElement.lang||'en';
  const emailOk=v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  const f=$('rfForm'), errs=f.querySelectorAll('.err');
  const shareText=(c,l)=>L()==='ar'?'استخدم رمزي '+c+' مع ويز للخدمات الذكية واحصل على خصم 100 رينغيت على تأسيس شركتك أو حسابك البنكي أو متجرك: '+l:L()==='ms'?'Guna kod saya '+c+' dengan Wizz Smart Services dan dapatkan RM 100 diskaun untuk syarikat, akaun bank atau kedai dalam talian anda: '+l:'Use my code '+c+' with Wizz Smart Services and get RM 100 off your company setup, bank account or marketplace store: '+l;
  f.addEventListener('submit',async e=>{
    e.preventDefault();errs.forEach(x=>x.hidden=true);
    const d=Object.fromEntries(new FormData(f));d.action='signup';d.lang=L();
    if(!d.name.trim()||!emailOk(d.email.trim())||!$('rf_ok').checked){errs[0].hidden=false;return;}
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{
      const r=await fetch('/.netlify/functions/referral',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||!j.ok)throw new Error(j.error||'x');
      f.hidden=true;
      if(j.code){$('rfCode').textContent=j.code;$('rfLink').textContent=j.link;$('rfShare').href='https://wa.me/?text='+encodeURIComponent(shareText(j.code,j.link));$('rfOk').hidden=false;$('rfOk').focus();}
      else{$('rfExists').hidden=false;$('rfExists').focus();}
      if(window.gtag)gtag('event','sign_up',{method:'referral'});
    }catch(err){errs[1].hidden=false;}finally{b.disabled=false;}
  });
  $('rfCopy').addEventListener('click',()=>{const t=$('rfLink').textContent;if(navigator.clipboard)navigator.clipboard.writeText(t).then(()=>{const s=$('rfCopy').firstChild;const o=s.textContent;s.textContent='✓';setTimeout(()=>s.textContent=o,1500);});});
  const g=$('stForm'), gerr=g.querySelector('.err');
  g.addEventListener('submit',async e=>{
    e.preventDefault();gerr.hidden=true;$('stOut').hidden=true;
    const code=$('st_code').value.trim().toUpperCase(), email=$('st_email').value.trim();
    if(!code||!emailOk(email)){gerr.hidden=false;return;}
    try{
      const r=await fetch('/.netlify/functions/referral',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({action:'stats',code,email})});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||!j.ok)throw 0;
      const s=j.stats, lab=[...$('stL').children].map(x=>x.textContent), idx={pending:0,approved:1,paid:2};
      $('stEnq').textContent=s.enquiries;$('stOrd').textContent=s.orders;
      const list=(s.commissions||[]);
      $('stCom').innerHTML=list.map(c=>'<li><span>'+lab[idx[c.status]]+'</span><b class="ltr">'+c.currency+' '+Number(c.amount).toFixed(2)+'</b></li>').join('');
      $('stOut').querySelector('.rf-none').hidden=list.length>0;
      $('stOut').hidden=false;
    }catch(_){gerr.hidden=false;}
  });
})();
</script>"""

rf_body = rf_hero + f'''
<section class="block">
  <div class="wrap">
    {head("Three steps", "Sign up, share your link, get paid")}
    <ol class="steps us-steps rf-steps">{rf_steps_html}</ol>
  </div>
</section>
<section class="block alt">
  <div class="wrap"><div class="us-ents us-ents-txt">{rf_ents}</div></div>
</section>
<section class="block" id="signup">
  <div class="wrap rf-wrap">
    {head("Join the programme", "Get your referral code", "It takes a minute. We email your code too, so you can find it later.")}
    {rf_form}
  </div>
</section>
<section class="block alt" id="check">
  <div class="wrap rf-wrap">
    {head("Already a referrer?", "Check your referrals", "Enter your code and the email you signed up with.")}
    {rf_check}
  </div>
</section>
<section class="block" id="rules">
  <div class="wrap faq-layout">
    <div>{T("p", "Refer & earn", "eyebrow")}{T("h2", "Programme rules")}{T("p", "Questions about the programme? Message us on WhatsApp.", "rf-q")}</div>
    <div class="faq">{rf_faq_html}</div>
  </div>
</section>
{x_final("Ready to start earning?", "Get your code in a minute and share it with anyone planning a business abroad.", RF_WA)}'''
rf_body = rf_body.replace('class="err full"', 'class="err full" hidden').replace('<p class="rf-none"', '<p class="rf-none" hidden')
page("refer.html", "Refer & Earn: RM 100 Off for Friends, 10% for You | Wizz Smart Services",
     "Join the Wizz referral programme. Your friends get RM 100 off orders of RM 1,000 or more, and you earn 10% of what they pay once their service is completed.",
     rf_body, extra_head=f'<script type="application/ld+json">{rf_ld}</script>', scripts=ar_script() + RF_JS)

US_CSS += """
.rf-steps{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:760px){.rf-steps{grid-template-columns:1fr}}
.rf-wrap{max-width:820px}
.rf-form .err{color:var(--red)}
.rf-agree{display:flex;gap:10px;align-items:center;font-size:14px}
.rf-agree input{width:18px;height:18px;flex:none}
.rf-out{border:1px solid var(--line);border-top:4px solid var(--red);border-radius:var(--r);background:var(--surface);padding:26px;display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.rf-out:focus{outline:none}
.rf-code{font:800 34px var(--mono);letter-spacing:.08em}
.rf-lbl{font-size:13px;color:var(--muted)}
.rf-link{font:600 15px var(--mono);word-break:break-all}
.rf-act{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.rf-note{font-size:13px;color:var(--muted)}
.rf-check{grid-template-columns:1fr 1fr}
.rf-stats{display:grid;grid-template-columns:1fr 1fr 2fr;gap:14px;margin-top:20px}
.rf-stats>div{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:18px;display:flex;flex-direction:column;gap:6px}
.rf-stats>div>b{font:800 30px var(--mono)}
.rf-stats>div>span,.rf-com-h{font-size:13px;color:var(--muted)}
.rf-com ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.rf-com li{display:flex;justify-content:space-between;gap:10px;font-size:15px}
.rf-none{font-size:14px;color:var(--muted)}
.rf-q{margin-top:12px;color:var(--muted)}
@media (max-width:640px){.rf-stats{grid-template-columns:1fr 1fr}.rf-com{grid-column:1/-1}.rf-check{grid-template-columns:1fr}}
"""
