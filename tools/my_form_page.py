# Malaysia company registration form (malaysia-company-form.html). Runs inside build_pkgs.py after refer_page.py.
# Sends to netlify/functions/malaysia-form.mjs; activity codes come from netlify/functions/msic.mjs (official DOSM MSIC 2008 list).
MTX = [
 ("Malaysia company registration", "تسجيل شركة في ماليزيا", "Pendaftaran syarikat Malaysia"),
 ("Register your Malaysian company", "سجّل شركتك في ماليزيا", "Daftar syarikat Malaysia anda"),
 ("Fill in this form and we'll check your company names with SSM, confirm your activity codes and send you a quote. It takes about 10 minutes.",
  "املأ هذا النموذج وسنتحقق من توفّر أسماء شركتك لدى هيئة الشركات الماليزية (SSM)، ونؤكد رموز الأنشطة، ونرسل لك عرض السعر. يستغرق نحو 10 دقائق.",
  "Isi borang ini dan kami akan menyemak nama syarikat anda dengan SSM, mengesahkan kod aktiviti anda dan menghantar sebut harga. Ia mengambil masa kira-kira 10 minit."),
 ("What happens next", "ماذا يحدث بعد ذلك", "Apa yang berlaku seterusnya"),
 ("We check your names with SSM", "نتحقق من الأسماء لدى SSM", "Kami menyemak nama anda dengan SSM"),
 ("You get your quote and document list", "يصلك عرض السعر وقائمة المستندات", "Anda menerima sebut harga dan senarai dokumen"),
 ("We register your company", "نسجّل شركتك", "Kami mendaftarkan syarikat anda"),
 ("Your contact details", "بيانات التواصل", "Butiran hubungan anda"),
 ("Full name", "الاسم الكامل", "Nama penuh"),
 ("Email", "البريد الإلكتروني", "E-mel"),
 ("WhatsApp / phone", "واتساب / الهاتف", "WhatsApp / telefon"),
 ("Country of residence", "دولة الإقامة", "Negara kediaman"),
 ("Company name", "اسم الشركة", "Nama syarikat"),
 ("Give us 3 names in order of preference. SSM approves one name per company, so we use the first one that's available. Every name ends with SDN. BHD.",
  "اكتب 3 أسماء حسب الأفضلية. توافق SSM على اسم واحد لكل شركة، لذلك نستخدم أول اسم متاح. ونضيف SDN. BHD. إلى نهاية كل اسم تلقائياً.",
  "Beri kami 3 nama mengikut keutamaan. SSM meluluskan satu nama bagi setiap syarikat, jadi kami menggunakan nama pertama yang tersedia. Setiap nama berakhir dengan SDN. BHD."),
 ("First choice", "الخيار الأول", "Pilihan pertama"),
 ("Second choice", "الخيار الثاني", "Pilihan kedua"),
 ("Third choice", "الخيار الثالث", "Pilihan ketiga"),
 ("Business activities", "أنشطة الشركة", "Aktiviti perniagaan"),
 ("In Malaysia a company can register up to 3 activities, each with an MSIC code. Search by keyword in English or Malay, or by code.",
  "في ماليزيا يمكن للشركة تسجيل 3 أنشطة كحد أقصى، لكل نشاط رمز MSIC. ابحث بكلمة بالإنجليزية أو الماليزية، أو بالرمز.",
  "Di Malaysia, syarikat boleh mendaftar sehingga 3 aktiviti, setiap satu dengan kod MSIC. Cari mengikut kata kunci dalam bahasa Inggeris atau Melayu, atau mengikut kod."),
 ("Search activity codes", "ابحث عن رمز النشاط", "Cari kod aktiviti"),
 ("e.g. online retail, software, 47912", "مثال: online retail أو software أو 47912", "cth. runcit dalam talian, perisian, 47912"),
 ("Your activities", "أنشطتك", "Aktiviti anda"),
 ("Remove", "إزالة", "Buang"),
 ("You've chosen 3 activities, the maximum.", "اخترت 3 أنشطة، وهو الحد الأقصى.", "Anda telah memilih 3 aktiviti, iaitu maksimum."),
 ("No matching codes. Try another word, or describe your business below.", "لا توجد رموز مطابقة. جرّب كلمة أخرى، أو صف نشاطك أدناه.", "Tiada kod sepadan. Cuba perkataan lain, atau terangkan perniagaan anda di bawah."),
 ("Loading the code list…", "جارٍ تحميل قائمة الرموز…", "Memuatkan senarai kod…"),
 ("The code list didn't load. Describe your business below and we'll choose the codes with you.", "لم تُحمَّل قائمة الرموز. صف نشاطك أدناه وسنختار الرموز معك.", "Senarai kod tidak dapat dimuatkan. Terangkan perniagaan anda di bawah dan kami akan memilih kod bersama anda."),
 ("Describe your business in a few words", "صف نشاطك التجاري بكلمات قليلة", "Terangkan perniagaan anda dalam beberapa perkataan"),
 ("Not sure which codes fit? Pick the closest ones and we'll confirm them with you before we file.", "لست متأكداً من الرموز المناسبة؟ اختر الأقرب وسنؤكدها معك قبل التسجيل.", "Tidak pasti kod yang sesuai? Pilih yang paling hampir dan kami akan mengesahkannya dengan anda sebelum pemfailan."),
 ("Budget and capital", "الميزانية ورأس المال", "Bajet dan modal"),
 ("Planned paid-up capital", "رأس المال المدفوع المخطط", "Modal berbayar yang dirancang"),
 ("Choose…", "اختر…", "Pilih…"),
 ("Under RM 10,000", "أقل من 10,000 رينغيت", "Bawah RM 10,000"),
 ("RM 10,000 to 99,999", "من 10,000 إلى 99,999 رينغيت", "RM 10,000 hingga 99,999"),
 ("RM 100,000 to 499,999", "من 100,000 إلى 499,999 رينغيت", "RM 100,000 hingga 499,999"),
 ("RM 500,000 or more", "500,000 رينغيت أو أكثر", "RM 500,000 atau lebih"),
 ("Not sure yet", "لم أحدد بعد", "Belum pasti"),
 ("Your budget for the setup (optional)", "ميزانيتك للتأسيس (اختياري)", "Bajet anda untuk penubuhan (pilihan)"),
 ("Paid-up capital is the money the shareholders put into the company. Some licences and work visas need a minimum amount, and we'll tell you if yours does.",
  "رأس المال المدفوع هو المبلغ الذي يضعه المساهمون في الشركة. بعض التراخيص وتأشيرات العمل تشترط حداً أدنى، وسنخبرك إن كان ذلك ينطبق عليك.",
  "Modal berbayar ialah wang yang dimasukkan oleh pemegang saham ke dalam syarikat. Sesetengah lesen dan visa kerja memerlukan jumlah minimum, dan kami akan memberitahu anda jika ia berkaitan."),
 ("Shareholders", "الشركاء", "Pemegang saham"),
 ("Number of shareholders", "عدد الشركاء", "Bilangan pemegang saham"),
 ("Fill in each person's details exactly as in their passport.", "اكتب بيانات كل شريك كما هي في جواز السفر تماماً.", "Isi butiran setiap orang tepat seperti dalam pasport mereka."),
 ("More than 6 shareholders? Tell us in the notes.", "أكثر من 6 شركاء؟ أخبرنا في الملاحظات.", "Lebih daripada 6 pemegang saham? Beritahu kami dalam nota."),
 ("Shareholder", "الشريك", "Pemegang saham"),
 ("Full name as in passport", "الاسم الكامل كما في الجواز", "Nama penuh seperti dalam pasport"),
 ("Nationality", "الجنسية", "Kewarganegaraan"),
 ("Passport number", "رقم الجواز", "Nombor pasport"),
 ("Date of birth", "تاريخ الميلاد", "Tarikh lahir"),
 ("Share (%)", "نسبة الملكية (%)", "Saham (%)"),
 ("Full residential address", "عنوان السكن الكامل", "Alamat kediaman penuh"),
 ("Malaysian residency", "الإقامة في ماليزيا", "Pemastautin di Malaysia"),
 ("Needs a residence visa", "يحتاج إلى إقامة (تأشيرة)", "Perlu visa pemastautin"),
 ("Already lives in Malaysia with a valid pass", "مقيم في ماليزيا بإقامة سارية", "Sudah tinggal di Malaysia dengan pas yang sah"),
 ("No residency needed", "لا يحتاج إلى إقامة", "Tidak perlu pemastautin"),
 ("A company in Malaysia needs at least one director who lives in Malaysia. If none of the shareholders does, we can quote a resident director service.",
  "تحتاج الشركة في ماليزيا إلى مدير واحد على الأقل مقيم في ماليزيا. إن لم يكن أي من الشركاء مقيماً فيها، يمكننا تقديم عرض لخدمة المدير المقيم.",
  "Syarikat di Malaysia memerlukan sekurang-kurangnya seorang pengarah yang tinggal di Malaysia. Jika tiada pemegang saham yang tinggal di sini, kami boleh menyebut harga perkhidmatan pengarah pemastautin."),
 ("Registering a company doesn't give a visa by itself. Residence and work visas are a separate application, decided by the Malaysian Immigration Department, and quoted separately.",
  "تسجيل الشركة لا يمنح تأشيرة بحد ذاته. الإقامة وتأشيرات العمل طلب منفصل تقرره دائرة الهجرة الماليزية، ويُسعَّر بشكل منفصل.",
  "Pendaftaran syarikat tidak memberikan visa dengan sendirinya. Visa pemastautin dan kerja ialah permohonan berasingan yang diputuskan oleh Jabatan Imigresen Malaysia, dan disebut harga secara berasingan."),
 ("Anything else", "أي تفاصيل أخرى", "Apa-apa lagi"),
 ("Notes (optional)", "ملاحظات (اختياري)", "Nota (pilihan)"),
 ("Referral code (optional)", "رمز الإحالة (اختياري)", "Kod rujukan (pilihan)"),
 ("I confirm these details are correct and agree that Wizz uses them to prepare my company registration.", "أؤكد صحة هذه البيانات وأوافق على أن تستخدمها ويز لتجهيز تسجيل شركتي.", "Saya mengesahkan butiran ini betul dan bersetuju Wizz menggunakannya untuk menyediakan pendaftaran syarikat saya."),
 ("Your passport details go only to our team and are used only for your registration.", "تُرسل بيانات جوازك إلى فريقنا فقط وتُستخدم لتسجيل شركتك فقط.", "Butiran pasport anda dihantar kepada pasukan kami sahaja dan digunakan untuk pendaftaran anda sahaja."),
 ("Send my details", "أرسل بياناتي", "Hantar butiran saya"),
 ("Please fill in the highlighted fields.", "يرجى تعبئة الحقول المحددة.", "Sila isi ruangan yang ditandakan."),
 ("The shares should add up to 100%.", "يجب أن يكون مجموع نسب الملكية 100%.", "Jumlah saham hendaklah 100%."),
 ("Sorry, something went wrong. Please try again, or message us on WhatsApp.", "عذراً، حدث خطأ. حاول مرة أخرى، أو راسلنا عبر واتساب.", "Maaf, berlaku ralat. Sila cuba lagi, atau hantar mesej kepada kami di WhatsApp."),
 ("We've received your details", "استلمنا بياناتك", "Kami telah menerima butiran anda"),
 ("Our team will check your names with SSM and reply with your quote and the documents we need, usually within one business day. We've sent a copy to your email.",
  "سيتحقق فريقنا من الأسماء لدى SSM ويرد عليك بعرض السعر والمستندات المطلوبة، عادةً خلال يوم عمل واحد. وأرسلنا نسخة إلى بريدك.",
  "Pasukan kami akan menyemak nama anda dengan SSM dan membalas dengan sebut harga serta dokumen yang diperlukan, biasanya dalam satu hari bekerja. Kami telah menghantar salinan ke e-mel anda."),
 ("Reference", "المرجع", "Rujukan"),
 ("Chat on WhatsApp", "تواصل عبر واتساب", "Sembang di WhatsApp"),
]
for en, ar, ms in MTX:
    AR_SRC.setdefault(en, ar)
_msx = json.load(open(_ms_path)); _ch = False
for en, ar, ms in MTX:
    if en not in _msx: _msx[en] = ms; _ch = True
if _ch: json.dump(_msx, open(_ms_path, "w"), ensure_ascii=False, indent=0)

def _ml(id_, en):
    return f'<label for="{id_}"{tk(en)}>{esc(en)}</label>'
def _opts(items):
    return "".join(f'<option value="{esc(v)}"{tk(v)}>{esc(v)}</option>' for v in items)
MF_RES = ["Needs a residence visa", "Already lives in Malaysia with a valid pass", "No residency needed"]
MF_CAP = ["Under RM 10,000", "RM 10,000 to 99,999", "RM 100,000 to 499,999", "RM 500,000 or more", "Not sure yet"]
CHOOSE = f'<option value=""{tk("Choose…")}>Choose…</option>'

def _partner(i):
    p = f"p{i}_"
    return f'''<fieldset class="mf-p" data-p="{i}"{"" if i == 1 else " hidden"}>
  <h3 class="mf-ph">{T("span", "Shareholder")} <span class="ltr">{i}</span></h3>
  <div class="mf-g">
    <div class="full">{_ml(p+"name", "Full name as in passport")}<input id="{p}name" data-k="name" dir="ltr" maxlength="150" required autocomplete="off"></div>
    <div>{_ml(p+"nat", "Nationality")}<input id="{p}nat" data-k="nat" maxlength="80" required></div>
    <div>{_ml(p+"passport", "Passport number")}<input id="{p}passport" data-k="passport" dir="ltr" maxlength="40" required autocomplete="off" class="mf-up"></div>
    <div>{_ml(p+"dob", "Date of birth")}<input id="{p}dob" data-k="dob" type="date" min="1920-01-01" required></div>
    <div>{_ml(p+"share", "Share (%)")}<input id="{p}share" data-k="share" type="number" min="1" max="100" step="any" inputmode="decimal" required{' value="100"' if i == 1 else ""}></div>
    <div class="full">{_ml(p+"address", "Full residential address")}<input id="{p}address" data-k="address" maxlength="400" required></div>
    <div class="full">{_ml(p+"res", "Malaysian residency")}<select id="{p}res" data-k="residency" required>{CHOOSE}{_opts(MF_RES)}</select></div>
  </div>
</fieldset>'''

def _leg(n, en):
    return f'<legend class="mf-leg"><span class="mf-n ltr">{n}</span>{T("span", en)}</legend>'

mf_form = f'''<form id="mfForm" class="mf-form" novalidate>
  <p hidden><label>Leave this empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>
  <fieldset class="mf-sec">{_leg(1, "Your contact details")}
    <div class="mf-g">
      <div>{_ml("mf_name", "Full name")}<input id="mf_name" name="name" autocomplete="name" maxlength="120" required></div>
      <div>{_ml("mf_email", "Email")}<input id="mf_email" name="email" type="email" dir="ltr" autocomplete="email" maxlength="200" required></div>
      <div>{_ml("mf_phone", "WhatsApp / phone")}<input id="mf_phone" name="phone" type="tel" dir="ltr" autocomplete="tel" maxlength="60" required></div>
      <div>{_ml("mf_country", "Country of residence")}<input id="mf_country" name="country" autocomplete="country-name" maxlength="80" required></div>
    </div>
  </fieldset>
  <fieldset class="mf-sec">{_leg(2, "Company name")}
    {T("p", "Give us 3 names in order of preference. SSM approves one name per company, so we use the first one that's available. Every name ends with SDN. BHD.", "mf-hint")}
    <div class="mf-names">
      {"".join(f'<div>{_ml(f"mf_n{i}", lab)}<div class="mf-name"><input id="mf_n{i}" class="mf-up" dir="ltr" maxlength="100" autocomplete="off"{" required" if i == 1 else ""}><span class="mf-suf ltr">SDN. BHD.</span></div></div>' for i, lab in ((1, "First choice"), (2, "Second choice"), (3, "Third choice")))}
    </div>
  </fieldset>
  <fieldset class="mf-sec">{_leg(3, "Business activities")}
    {T("p", "In Malaysia a company can register up to 3 activities, each with an MSIC code. Search by keyword in English or Malay, or by code.", "mf-hint")}
    <div class="mf-msic">
      {_ml("mf_q", "Search activity codes")}
      <input id="mf_q" type="search" autocomplete="off" placeholder="e.g. online retail, software, 47912"{kph("e.g. online retail, software, 47912")} aria-controls="mfRes">
      {T("p", "Loading the code list…", "mf-msg")}
      {T("p", "No matching codes. Try another word, or describe your business below.", "mf-msg")}
      {T("p", "The code list didn't load. Describe your business below and we'll choose the codes with you.", "mf-msg")}
      {T("p", "You've chosen 3 activities, the maximum.", "mf-msg")}
      <ul id="mfRes" class="mf-res" role="listbox" hidden></ul>
      <div class="mf-selw" id="mfSelW" hidden>{T("p", "Your activities", "mf-lbl")}<ol id="mfSel" class="mf-sel"></ol></div>
      <span hidden id="mfRm">{T("span", "Remove")}</span>
    </div>
    <div class="mf-g">
      <div class="full">{_ml("mf_bus", "Describe your business in a few words")}<textarea id="mf_bus" name="business" maxlength="1000" rows="3"></textarea>
        {T("p", "Not sure which codes fit? Pick the closest ones and we'll confirm them with you before we file.", "mf-hint")}</div>
    </div>
  </fieldset>
  <fieldset class="mf-sec">{_leg(4, "Budget and capital")}
    <div class="mf-g">
      <div>{_ml("mf_cap", "Planned paid-up capital")}<select id="mf_cap" name="capital" required>{CHOOSE}{_opts(MF_CAP)}</select></div>
      <div>{_ml("mf_budget", "Your budget for the setup (optional)")}<input id="mf_budget" name="budget" maxlength="120"></div>
    </div>
    {T("p", "Paid-up capital is the money the shareholders put into the company. Some licences and work visas need a minimum amount, and we'll tell you if yours does.", "mf-hint")}
  </fieldset>
  <fieldset class="mf-sec">{_leg(5, "Shareholders")}
    <div class="mf-g">
      <div>{_ml("mf_count", "Number of shareholders")}<select id="mf_count">{"".join(f'<option value="{i}">{i}</option>' for i in range(1, 7))}</select></div>
      <div class="mf-cnote">{T("p", "Fill in each person's details exactly as in their passport.", "mf-hint")}{T("p", "More than 6 shareholders? Tell us in the notes.", "mf-hint")}</div>
    </div>
    {"".join(_partner(i) for i in range(1, 7))}
    {T("p", "The shares should add up to 100%.", "err mf-sharerr")}
    <div class="mf-notes">
      {T("p", "A company in Malaysia needs at least one director who lives in Malaysia. If none of the shareholders does, we can quote a resident director service.")}
      {T("p", "Registering a company doesn't give a visa by itself. Residence and work visas are a separate application, decided by the Malaysian Immigration Department, and quoted separately.")}
    </div>
  </fieldset>
  <fieldset class="mf-sec">{_leg(6, "Anything else")}
    <div class="mf-g">
      <div class="full">{_ml("mf_notes", "Notes (optional)")}<textarea id="mf_notes" name="notes" maxlength="3000" rows="3"></textarea></div>
      <div>{_ml("mf_ref", "Referral code (optional)")}<input id="mf_ref" name="ref" class="ref-in" dir="ltr" maxlength="16" autocomplete="off"></div>
    </div>
    <label class="rf-agree mf-agree"><input type="checkbox" id="mf_ok"> <span{tk("I confirm these details are correct and agree that Wizz uses them to prepare my company registration.")}>I confirm these details are correct and agree that Wizz uses them to prepare my company registration.</span></label>
  </fieldset>
  <div class="formfoot mf-foot"><button class="btn solid" type="submit"><span class="dot"></span>{T("span", "Send my details")}</button>{T("small", "Your passport details go only to our team and are used only for your registration.")}</div>
  {T("p", "Please fill in the highlighted fields.", "err mf-e1")}
  {T("p", "Sorry, something went wrong. Please try again, or message us on WhatsApp.", "err mf-e2")}
</form>
<div class="out mf-out" id="mfOut" hidden role="status" tabindex="-1">
  <span class="out-ic">{CHECK}</span>
  {T("h2", "We've received your details", "out-t")}
  {T("p", "Our team will check your names with SSM and reply with your quote and the documents we need, usually within one business day. We've sent a copy to your email.", "out-p")}
  <p class="out-ref" id="mfRefW" hidden>{T("span", "Reference")}: <bdi id="mfRef"></bdi></p>
  <div class="out-act"><a class="btn wa" id="mfWa" target="_blank" rel="noopener">{T("span", "Chat on WhatsApp")}</a></div>
</div>'''

MF_JS = r"""<script>
(function(){
  const $=id=>document.getElementById(id), f=$('mfForm');
  const L=()=>document.documentElement.lang||'en';
  const emailOk=v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  const msgs=f.querySelectorAll('.mf-msg'), [mLoad,mNone,mFail,mMax]=msgs;
  const show=m=>msgs.forEach(x=>x.hidden=x!==m);
  // referral code remembered from a ?ref= link
  try{const r=JSON.parse(localStorage.getItem('wizz-ref')||'null');if(r&&r.c&&!$('mf_ref').value)$('mf_ref').value=r.c;}catch(_){}
  // company names: capitals, no suffix typed twice
  f.querySelectorAll('.mf-up').forEach(i=>i.addEventListener('input',()=>{const p=i.selectionStart;i.value=i.value.toUpperCase();try{i.setSelectionRange(p,p)}catch(_){}}));
  const clean=n=>n.toUpperCase().replace(/\s*\b(SDN\.?\s*BHD\.?|SENDIRIAN\s+BERHAD)\s*$/i,'').trim();
  // shareholders
  const cards=[...f.querySelectorAll('.mf-p')];
  function setCount(){const n=+$('mf_count').value;cards.forEach((c,i)=>{c.hidden=i>=n;c.querySelectorAll('input,select').forEach(x=>x.disabled=i>=n);});
    if(n===1)$('p1_share').value=100;}
  $('mf_count').addEventListener('change',setCount);setCount();
  // MSIC search
  let codes=null,loading=null;const sel=[];
  const desc=it=>L()==='ms'&&it[2]?it[2]:it[1];
  function load(){if(codes||loading)return loading;show(mLoad);
    loading=fetch('/.netlify/functions/msic').then(r=>r.json()).then(j=>{if(!j.ok)throw 0;codes=j.items.map(x=>[x[0],x[1],x[2],(x[1]+' '+x[2]).toLowerCase()]);show(null);search();})
      .catch(()=>{show(mFail);$('mf_q').disabled=true;});return loading;}
  const q=$('mf_q'),res=$('mfRes');
  function search(){
    if(!codes)return;const v=q.value.trim().toLowerCase();res.innerHTML='';
    if(sel.length>=3){res.hidden=true;show(v?mMax:null);return;}
    if(v.length<2&&!/^\d/.test(v)){res.hidden=true;show(null);return;}
    let hits;
    if(/^\d+$/.test(v))hits=codes.filter(c=>c[0].startsWith(v));
    else{const w=v.split(/\s+/).filter(Boolean);hits=codes.filter(c=>w.every(x=>c[3].includes(x)));}
    hits=hits.filter(c=>!sel.some(s=>s[0]===c[0])).slice(0,40);
    if(!hits.length){res.hidden=true;show(mNone);return;}
    show(null);
    res.innerHTML=hits.map(c=>'<li role="option"><button type="button" data-c="'+c[0]+'"><b class="ltr">'+c[0]+'</b><span>'+desc(c).replace(/[&<>]/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[s]))+'</span></button></li>').join('');
    res.hidden=false;
  }
  let t;q.addEventListener('focus',load);q.addEventListener('input',()=>{load();clearTimeout(t);t=setTimeout(search,120);});
  res.addEventListener('click',e=>{const b=e.target.closest('[data-c]');if(!b||sel.length>=3)return;
    sel.push(codes.find(c=>c[0]===b.dataset.c));drawSel();q.value='';res.hidden=true;show(sel.length>=3?mMax:null);if(sel.length<3)q.focus();});
  function drawSel(){
    const rm=$('mfRm').textContent.trim();
    $('mfSel').innerHTML=sel.map((c,i)=>'<li><b class="ltr">'+c[0]+'</b><span>'+desc(c).replace(/[&<>]/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[s]))+'</span><button type="button" class="mf-x" data-i="'+i+'" aria-label="'+rm+'">×</button></li>').join('');
    $('mfSelW').hidden=!sel.length;q.disabled=sel.length>=3;
  }
  $('mfSel').addEventListener('click',e=>{const b=e.target.closest('[data-i]');if(!b)return;sel.splice(+b.dataset.i,1);drawSel();show(null);q.disabled=false;q.focus();});
  // submit
  const e1=f.querySelector('.mf-e1'),e2=f.querySelector('.mf-e2'),eS=f.querySelector('.mf-sharerr');
  f.addEventListener('input',e=>{if(e.target.classList)e.target.classList.remove('bad');});
  f.addEventListener('change',e=>{if(e.target.classList)e.target.classList.remove('bad');});
  f.addEventListener('submit',async e=>{
    e.preventDefault();[e1,e2,eS].forEach(x=>x.hidden=true);
    const bad=[];
    f.querySelectorAll('[required]').forEach(x=>{if(x.disabled)return;const v=x.value.trim();if(!v||(x.type==='email'&&!emailOk(v)))bad.push(x);});
    const bus=$('mf_bus');if(!sel.length&&!bus.value.trim())bad.push(bus);
    const ok=$('mf_ok');if(!ok.checked)bad.push(ok.parentNode);
    f.querySelectorAll('.bad').forEach(x=>x.classList.remove('bad'));bad.forEach(x=>x.classList.add('bad'));
    if(bad.length){e1.hidden=false;bad[0].scrollIntoView({behavior:'smooth',block:'center'});if(bad[0].focus)bad[0].focus({preventScroll:true});return;}
    const n=+$('mf_count').value, ps=cards.slice(0,n).map(c=>{const o={};c.querySelectorAll('[data-k]').forEach(x=>o[x.dataset.k]=x.value.trim());return o;});
    const tot=ps.reduce((t,p)=>t+(parseFloat(p.share)||0),0);
    if(Math.abs(tot-100)>0.01){eS.hidden=false;cards.slice(0,n).forEach(c=>c.querySelector('[data-k=share]').classList.add('bad'));eS.scrollIntoView({behavior:'smooth',block:'center'});return;}
    const d={name:$('mf_name').value,email:$('mf_email').value,phone:$('mf_phone').value,country:$('mf_country').value,
      names:[1,2,3].map(i=>clean($('mf_n'+i).value)).filter(Boolean),activities:sel.map(c=>({code:c[0],desc:c[1]})),
      business:bus.value,capital:$('mf_cap').value,budget:$('mf_budget').value,partners:ps,notes:$('mf_notes').value,
      ref:$('mf_ref').value,lang:L(),company_website:f.company_website.value};
    const b=f.querySelector('button[type=submit]');b.disabled=true;
    try{
      const r=await fetch('/.netlify/functions/malaysia-form',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)});
      const j=await r.json().catch(()=>({}));if(!r.ok||!j.ok)throw 0;
      f.hidden=true;const o=$('mfOut');
      if(j.ref){$('mfRef').textContent=j.ref;$('mfRefW').hidden=false;}
      $('mfWa').href='https://wa.me/601124477685?text='+encodeURIComponent((L()==='ar'?'مرحباً ويز، أرسلت نموذج تسجيل شركتي في ماليزيا. ':L()==='ms'?'Hai Wizz, saya telah menghantar borang syarikat Malaysia saya. ':"Hi Wizz, I've sent my Malaysia company form. ")+(j.ref?'Ref: '+j.ref:d.names[0]+' SDN. BHD.'));
      o.hidden=false;o.scrollIntoView({behavior:'smooth',block:'start'});o.focus({preventScroll:true});
      if(window.gtag)gtag('event','generate_lead',{form:'malaysia_company'});
    }catch(_){e2.hidden=false;}finally{b.disabled=false;}
  });
})();
</script>"""

mf_steps = "".join(f'<li>{T("span", s)}</li>' for s in ("We check your names with SSM", "You get your quote and document list", "We register your company"))
mf_body = hero_t("Malaysia company registration", "Register your Malaysian company",
    "Fill in this form and we'll check your company names with SSM, confirm your activity codes and send you a quote. It takes about 10 minutes.") + f'''
<section class="block">
  <div class="wrap mf-wrap">
    <div class="mf-next">{T("p", "What happens next", "eyebrow")}<ol class="out-steps mf-steps">{mf_steps}</ol></div>
    {mf_form}
  </div>
</section>
<p class="us-disc wrap"><span{tk(DISC)}>{esc(DISC)}</span></p>'''
for _c in ("err mf-sharerr", "err mf-e1", "err mf-e2"):
    mf_body = mf_body.replace(f'class="{_c}"', f'class="{_c}" hidden')
mf_body = mf_body.replace('<p class="mf-msg"', '<p class="mf-msg" hidden')
page("malaysia-company-form.html", "Malaysia Company Registration Form (Sdn. Bhd.) | Wizz Smart Services",
     "Send us your details for a Malaysian Sdn. Bhd.: three proposed names, up to 3 MSIC activity codes, capital and shareholders. We check the names with SSM and send your quote.",
     mf_body, scripts=ar_script() + MF_JS)

US_CSS += """
.mf-wrap{max-width:860px}
.mf-out,.mf-form .err{scroll-margin-top:96px}
.mf-next{margin-bottom:26px}
.mf-steps{border-top:0;padding-top:4px;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 18px}
@media (max-width:700px){.mf-steps{grid-template-columns:1fr}}
.mf-form{display:flex;flex-direction:column;gap:18px}
.mf-sec{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:22px clamp(16px,3vw,26px) 24px;display:flex;flex-direction:column;gap:14px;min-width:0}
.mf-leg{float:left;width:100%;display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;padding:0;margin:0 0 4px}
[dir="rtl"] .mf-leg{float:right}
.mf-leg+*{clear:both}
.mf-n{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--ink);color:var(--surface);font:700 13px var(--body);flex:none}
.mf-g{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px}
.mf-g .full{grid-column:1/-1}
.mf-hint{font-size:13.5px;color:var(--muted);margin:0}
.mf-g .mf-hint{margin-top:6px}
.mf-names{display:grid;gap:12px}
.mf-name{display:flex;align-items:stretch;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);overflow:hidden}
.mf-name:focus-within{border-color:var(--ink)}
.mf-name input{border:0;border-radius:0;min-width:0;flex:1}
.mf-suf{display:flex;align-items:center;padding:0 12px;background:var(--bg);border-inline-start:1px solid var(--line);font:700 13px var(--mono);white-space:nowrap;color:var(--muted)}
[dir="rtl"] .mf-name{flex-direction:row-reverse}
[dir="rtl"] .mf-suf{border-inline-start:0;border-inline-end:1px solid var(--line)}
.mf-up{text-transform:uppercase}
.mf-up::placeholder{text-transform:none}
.mf-msic{position:relative;display:flex;flex-direction:column;gap:8px}
.mf-msic label{margin:0}
.mf-msg{font-size:13.5px;color:var(--muted);margin:0}
.mf-res{list-style:none;margin:0;padding:4px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);max-height:300px;overflow:auto;box-shadow:0 12px 28px -18px rgba(0,0,0,.35)}
.mf-res button{all:unset;box-sizing:border-box;width:100%;display:flex;gap:12px;align-items:baseline;padding:9px 10px;border-radius:3px;cursor:pointer;font-size:14.5px;line-height:1.35}
.mf-res button:hover,.mf-res button:focus-visible{background:var(--bg)}
.mf-res b,.mf-sel b{font:700 13.5px var(--mono);flex:none}
.mf-lbl{font-size:13.5px;font-weight:600;margin:4px 0 0}
.mf-sel{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.mf-sel li{display:flex;gap:12px;align-items:baseline;border:1px solid var(--line);border-inline-start:4px solid var(--red);border-radius:var(--r);padding:10px 12px;background:var(--bg);font-size:14.5px}
.mf-sel span{flex:1}
.mf-x{all:unset;cursor:pointer;font-size:20px;line-height:1;padding:0 4px;color:var(--muted)}
.mf-x:hover{color:var(--red)}
.mf-cnote{display:flex;flex-direction:column;justify-content:flex-end;gap:4px}
.mf-p{border-top:1px dashed var(--line);padding-top:16px;margin-top:4px;min-width:0}
.mf-ph{font-size:16px;margin:0 0 12px;display:flex;gap:6px}
.mf-notes{display:grid;gap:8px;font-size:13.5px;color:var(--muted);border-inline-start:3px solid var(--line);padding-inline-start:12px}
.mf-notes p{margin:0}
.mf-agree{margin:4px 0 0;font-weight:500;align-items:flex-start}
.mf-agree input{margin-top:2px}
.mf-foot{margin-top:4px}
.mf-form .bad{border-color:var(--red)!important;box-shadow:0 0 0 1px var(--red)}
.mf-name:has(.bad){border-color:var(--red);box-shadow:0 0 0 1px var(--red)}
.mf-name .bad{box-shadow:none}
.mf-agree.bad{box-shadow:none;color:var(--red)}
.mf-form .err{margin:0}
input[type=date]{min-height:45px}
@media (max-width:560px){.mf-g{grid-template-columns:1fr}.mf-sel li,.mf-res button{font-size:14px}}
"""
