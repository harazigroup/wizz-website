# Careers page (careers.html). Runs inside build_pkgs.py after my_form_page.py (uses x_hero-free hero_t, head, T, tk, CHECK, US_CSS).
# Applications go to netlify/functions/careers.mjs. To add or close a role, edit JOBS below and the strings in JTX.
JTX = [
 ("Careers", "الوظائف", "Kerjaya"),
 ("Build your career beyond borders", "ابنِ مسيرتك المهنية بلا حدود", "Bina kerjaya anda merentasi sempadan"),
 ("We help entrepreneurs from around the world start and grow their companies. Join a small team in Kuala Lumpur and online, and learn international business from the inside.",
  "نساعد رواد الأعمال من حول العالم على تأسيس شركاتهم وتنميتها. انضم إلى فريق صغير في كوالالمبور وعن بُعد، وتعلّم الأعمال الدولية من الداخل.",
  "Kami membantu usahawan dari seluruh dunia memulakan dan mengembangkan syarikat mereka. Sertai pasukan kecil di Kuala Lumpur dan dalam talian, dan pelajari perniagaan antarabangsa dari dalam."),
 ("See open roles", "اطّلع على الوظائف المتاحة", "Lihat jawatan kosong"),
 ("Why work at Wizz", "لماذا تعمل في ويز", "Mengapa bekerja di Wizz"),
 ("Clients from 15 countries", "عملاء من 15 دولة", "Pelanggan dari 15 negara"),
 ("You work with founders from the Gulf, Africa, Asia and Europe, in Arabic, English and Malay.", "تعمل مع مؤسسين من الخليج وأفريقيا وآسيا وأوروبا، بالعربية والإنجليزية والماليزية.", "Anda bekerja dengan pengasas dari Teluk, Afrika, Asia dan Eropah, dalam bahasa Arab, Inggeris dan Melayu."),
 ("Learn the whole business", "تعلّم العمل من كل جوانبه", "Pelajari keseluruhan perniagaan"),
 ("Company formation, banking, marketplaces and logistics: you see how international companies are really built.", "تأسيس الشركات والحسابات البنكية والمنصات والخدمات اللوجستية: ترى كيف تُبنى الشركات الدولية فعلاً.", "Penubuhan syarikat, perbankan, pasaran dalam talian dan logistik: anda melihat bagaimana syarikat antarabangsa sebenarnya dibina."),
 ("Salary plus commission", "راتب مع عمولة", "Gaji serta komisen"),
 ("Every role has a fixed salary, and you earn commission on the clients you help bring in.", "لكل وظيفة راتب ثابت، وتحصل على عمولة عن العملاء الذين تساهم في جلبهم.", "Setiap jawatan ada gaji tetap, dan anda memperoleh komisen atas pelanggan yang anda bantu bawa masuk."),
 ("Remote or Kuala Lumpur", "عن بُعد أو في كوالالمبور", "Jarak jauh atau Kuala Lumpur"),
 ("Work from our office in Publika, Kuala Lumpur, or remotely from anywhere in Malaysia, depending on the role.", "اعمل من مكتبنا في بوبليكا بكوالالمبور أو عن بُعد من أي مكان في ماليزيا، حسب الوظيفة.", "Bekerja dari pejabat kami di Publika, Kuala Lumpur, atau dari jauh dari mana-mana di Malaysia, bergantung pada jawatan."),
 ("Open roles", "الوظائف المتاحة", "Jawatan kosong"),
 ("Join the team", "انضم إلى الفريق", "Sertai pasukan"),
 ("Don't see your role? Send an open application below and we'll keep your CV on file.", "لم تجد وظيفتك؟ أرسل طلباً عاماً أدناه وسنحتفظ بسيرتك الذاتية.", "Tiada jawatan yang sesuai? Hantar permohonan terbuka di bawah dan kami akan menyimpan CV anda."),
 ("Sales Executive (Arabic, English & Malay)", "مسؤول مبيعات (عربي وإنجليزي وملايو)", "Eksekutif Jualan (Arab, Inggeris & Melayu)"),
 ("Customer Support (WhatsApp)", "خدمة العملاء (واتساب)", "Sokongan Pelanggan (WhatsApp)"),
 ("Content Creator (Video)", "صانع محتوى (فيديو)", "Pencipta Kandungan (Video)"),
 ("Open application", "طلب عام", "Permohonan terbuka"),
 ("Remote or KL office", "عن بُعد أو في مكتب كوالالمبور", "Jarak jauh atau pejabat KL"),
 ("Remote, in shifts", "عن بُعد، بنظام المناوبات", "Jarak jauh, mengikut syif"),
 ("KL office or remote", "مكتب كوالالمبور أو عن بُعد", "Pejabat KL atau jarak jauh"),
 ("Full-time", "دوام كامل", "Sepenuh masa"),
 ("Full-time or part-time", "دوام كامل أو جزئي", "Sepenuh masa atau separuh masa"),
 ("Full-time or freelance", "دوام كامل أو عمل حر", "Sepenuh masa atau bebas"),
 ("Salary + commission", "راتب + عمولة", "Gaji + komisen"),
 ("You turn enquiries from WhatsApp, our website and ads into clients. You explain our services clearly, prepare quotes and follow up until the client is ready.",
  "تحوّل الاستفسارات القادمة من واتساب وموقعنا والإعلانات إلى عملاء. تشرح خدماتنا بوضوح، وتجهّز عروض الأسعار، وتتابع حتى يصبح العميل جاهزاً.",
  "Anda menukar pertanyaan dari WhatsApp, laman web dan iklan kami kepada pelanggan. Anda menerangkan perkhidmatan kami dengan jelas, menyediakan sebut harga dan membuat susulan sehingga pelanggan bersedia."),
 ("You are the first reply our clients get. You answer questions, collect documents and keep clients updated while we work on their company.",
  "أنت أول رد يتلقاه عملاؤنا. تجيب عن الأسئلة، وتجمع المستندات، وتطلع العملاء على المستجدات أثناء عملنا على شركاتهم.",
  "Anda balasan pertama yang diterima pelanggan kami. Anda menjawab soalan, mengumpul dokumen dan memaklumkan perkembangan kepada pelanggan semasa kami menguruskan syarikat mereka."),
 ("You make the short videos and posts that explain international business simply, for TikTok, Instagram and Reels, in English.",
  "تصنع الفيديوهات القصيرة والمنشورات التي تشرح الأعمال الدولية ببساطة، على تيك توك وإنستغرام والريلز، باللغة الإنجليزية.",
  "Anda menghasilkan video pendek dan hantaran yang menerangkan perniagaan antarabangsa dengan mudah, untuk TikTok, Instagram dan Reels, dalam bahasa Inggeris."),
 ("What you'll do", "ماذا ستفعل", "Apa yang anda akan lakukan"),
 ("What you bring", "ما نبحث عنه", "Apa yang anda bawa"),
 ("Reply to new leads on WhatsApp and email, quickly and clearly", "الرد على العملاء الجدد عبر واتساب والبريد بسرعة ووضوح", "Membalas petunjuk baharu di WhatsApp dan e-mel dengan cepat dan jelas"),
 ("Understand each client's goals and recommend the right package", "فهم أهداف كل عميل واقتراح الباقة المناسبة", "Memahami matlamat setiap pelanggan dan mencadangkan pakej yang sesuai"),
 ("Prepare quotes in our system and follow up", "تجهيز عروض الأسعار في نظامنا ومتابعتها", "Menyediakan sebut harga dalam sistem kami dan membuat susulan"),
 ("Keep every lead updated in our CRM", "تحديث بيانات كل عميل في نظام إدارة العملاء", "Mengemas kini setiap petunjuk dalam CRM kami"),
 ("Fluent Arabic, English and Malay", "إتقان العربية والإنجليزية والملايو", "Fasih bahasa Arab, Inggeris dan Melayu"),
 ("At least 1 year in sales, ideally services or B2B", "خبرة سنة على الأقل في المبيعات، ويُفضّل في الخدمات أو بين الشركات", "Sekurang-kurangnya 1 tahun dalam jualan, sebaik-baiknya perkhidmatan atau B2B"),
 ("Honest selling: you never promise approvals we can't guarantee", "بيع بأمانة: لا تعد أبداً بموافقات لا يمكننا ضمانها", "Jualan jujur: anda tidak pernah menjanjikan kelulusan yang tidak dapat kami jamin"),
 ("Comfortable working with targets", "الارتياح للعمل وفق أهداف", "Selesa bekerja dengan sasaran"),
 ("Answer client messages on WhatsApp in shifts", "الرد على رسائل العملاء عبر واتساب بنظام المناوبات", "Menjawab mesej pelanggan di WhatsApp mengikut syif"),
 ("Collect and check documents before we file", "جمع المستندات ومراجعتها قبل التقديم", "Mengumpul dan menyemak dokumen sebelum kami memfailkan"),
 ("Send clients clear status updates", "إرسال تحديثات واضحة للعملاء عن سير العمل", "Menghantar kemas kini status yang jelas kepada pelanggan"),
 ("Pass interested leads to the sales team", "تحويل العملاء المهتمين إلى فريق المبيعات", "Menyerahkan petunjuk yang berminat kepada pasukan jualan"),
 ("Arabic, English and Malay", "العربية والإنجليزية والملايو", "Bahasa Arab, Inggeris dan Melayu"),
 ("Organised, patient and quick to reply", "منظّم وصبور وسريع الرد", "Teratur, sabar dan cepat membalas"),
 ("Comfortable with WhatsApp Business and Google Sheets", "تجيد استخدام واتساب للأعمال وجداول Google", "Selesa menggunakan WhatsApp Business dan Google Sheets"),
 ("Available for shifts, including some weekends", "متاح للعمل بالمناوبات، بما فيها بعض عطلات نهاية الأسبوع", "Boleh bekerja mengikut syif, termasuk sesetengah hujung minggu"),
 ("Plan, film and edit short videos with our team", "تخطيط وتصوير ومونتاج الفيديوهات القصيرة مع فريقنا", "Merancang, merakam dan menyunting video pendek bersama pasukan kami"),
 ("Turn client stories and common questions into posts", "تحويل قصص العملاء والأسئلة الشائعة إلى منشورات", "Menukar kisah pelanggan dan soalan lazim kepada hantaran"),
 ("Write captions and track what performs", "كتابة النصوص المرافقة ومتابعة أداء المحتوى", "Menulis kapsyen dan menjejak prestasi kandungan"),
 ("Keep every post accurate and on brand", "الحفاظ على دقة كل منشور وتوافقه مع الهوية", "Memastikan setiap hantaran tepat dan mengikut jenama"),
 ("A portfolio of short-form videos", "نماذج سابقة من الفيديوهات القصيرة", "Portfolio video bentuk pendek"),
 ("Strong English, plus Arabic and Malay", "إنجليزية قوية، مع العربية والملايو", "Bahasa Inggeris yang baik, serta bahasa Arab dan Melayu"),
 ("Editing in CapCut, Premiere or similar", "مونتاج على CapCut أو Premiere أو ما يشابهها", "Menyunting dengan CapCut, Premiere atau seumpamanya"),
 ("Interest in business and e-commerce", "اهتمام بالأعمال والتجارة الإلكترونية", "Minat dalam perniagaan dan e-dagang"),
 ("Apply for this role", "قدّم على هذه الوظيفة", "Mohon jawatan ini"),
 ("How we hire", "كيف نوظّف", "Cara kami mengambil pekerja"),
 ("Four simple steps", "أربع خطوات بسيطة", "Empat langkah mudah"),
 ("Apply", "قدّم", "Mohon"),
 ("Fill in the form and attach your CV. It takes about 5 minutes.", "املأ النموذج وأرفق سيرتك الذاتية. يستغرق نحو 5 دقائق.", "Isi borang dan lampirkan CV anda. Ia mengambil masa kira-kira 5 minit."),
 ("Short call", "مكالمة قصيرة", "Panggilan ringkas"),
 ("A 20-minute video call to get to know you.", "مكالمة فيديو مدتها 20 دقيقة للتعرف عليك.", "Panggilan video 20 minit untuk mengenali anda."),
 ("Task or interview", "مهمة أو مقابلة", "Tugasan atau temu duga"),
 ("A small practical task or a second interview with the team.", "مهمة عملية صغيرة أو مقابلة ثانية مع الفريق.", "Tugasan praktikal kecil atau temu duga kedua bersama pasukan."),
 ("Offer", "العرض الوظيفي", "Tawaran"),
 ("We send you a written offer with your salary and commission.", "نرسل لك عرضاً مكتوباً يتضمن الراتب والعمولة.", "Kami menghantar tawaran bertulis dengan gaji dan komisen anda."),
 ("Apply now", "قدّم الآن", "Mohon sekarang"),
 ("Send your application", "أرسل طلبك", "Hantar permohonan anda"),
 ("We review every application. If your profile fits, we contact you within two weeks.", "نراجع كل الطلبات، وإن كان ملفك مناسباً نتواصل معك خلال أسبوعين.", "Kami menyemak setiap permohonan. Jika profil anda sesuai, kami menghubungi anda dalam masa dua minggu."),
 ("Role", "الوظيفة", "Jawatan"),
 ("Choose…", "اختر…", "Pilih…"),
 ("Full name", "الاسم الكامل", "Nama penuh"),
 ("Email", "البريد الإلكتروني", "E-mel"),
 ("WhatsApp / phone", "واتساب / الهاتف", "WhatsApp / telefon"),
 ("State / city in Malaysia", "الولاية / المدينة في ماليزيا", "Negeri / bandar di Malaysia"),
 ("Malaysian citizens only", "للمواطنين الماليزيين فقط", "Warganegara Malaysia sahaja"),
 ("All roles are open to Malaysian citizens only, and need Arabic, English and Malay.", "جميع الوظائف للمواطنين الماليزيين فقط، وتتطلب العربية والإنجليزية والملايو.", "Semua jawatan terbuka kepada warganegara Malaysia sahaja, dan memerlukan bahasa Arab, Inggeris dan Melayu."),
 ("I confirm I am a Malaysian citizen.", "أؤكد أنني مواطن ماليزي.", "Saya mengesahkan saya warganegara Malaysia."),
 ("Where do you want to work?", "أين تفضّل أن تعمل؟", "Di mana anda mahu bekerja?"),
 ("Remote", "عن بُعد", "Jarak jauh"),
 ("KL office", "مكتب كوالالمبور", "Pejabat KL"),
 ("Either", "أيٌّ منهما", "Mana-mana"),
 ("Languages you speak", "اللغات التي تتحدثها", "Bahasa yang anda tuturkan"),
 ("LinkedIn or portfolio link (optional)", "رابط LinkedIn أو نماذج أعمالك (اختياري)", "Pautan LinkedIn atau portfolio (pilihan)"),
 ("Your CV (PDF or Word, up to 4 MB)", "سيرتك الذاتية (PDF أو Word، حتى 4 ميغابايت)", "CV anda (PDF atau Word, sehingga 4 MB)"),
 ("Why Wizz? (optional)", "لماذا ويز؟ (اختياري)", "Mengapa Wizz? (pilihan)"),
 ("I agree that Wizz keeps my application for up to 12 months for hiring.", "أوافق على أن تحتفظ ويز بطلبي لمدة تصل إلى 12 شهراً لأغراض التوظيف.", "Saya bersetuju Wizz menyimpan permohonan saya sehingga 12 bulan untuk tujuan pengambilan pekerja."),
 ("Send application", "أرسل الطلب", "Hantar permohonan"),
 ("Please fill in the highlighted fields.", "يرجى تعبئة الحقول المحددة.", "Sila isi ruangan yang ditandakan."),
 ("Please attach your CV as a PDF or Word file, up to 4 MB.", "يرجى إرفاق سيرتك الذاتية بصيغة PDF أو Word بحجم لا يتجاوز 4 ميغابايت.", "Sila lampirkan CV anda dalam format PDF atau Word, sehingga 4 MB."),
 ("Sorry, something went wrong. Please try again, or message us on WhatsApp.", "عذراً، حدث خطأ. حاول مرة أخرى، أو راسلنا عبر واتساب.", "Maaf, berlaku ralat. Sila cuba lagi, atau hantar mesej kepada kami di WhatsApp."),
 ("Application received", "استلمنا طلبك", "Permohonan diterima"),
 ("Thank you. We've emailed you a confirmation. If your profile fits, we'll contact you within two weeks to arrange a short call.", "شكراً لك. أرسلنا لك تأكيداً على بريدك. إن كان ملفك مناسباً سنتواصل معك خلال أسبوعين لترتيب مكالمة قصيرة.", "Terima kasih. Kami telah menghantar pengesahan ke e-mel anda. Jika profil anda sesuai, kami akan menghubungi anda dalam masa dua minggu untuk mengatur panggilan ringkas."),
 ("Reference", "المرجع", "Rujukan"),
 ("Sending…", "جارٍ الإرسال…", "Menghantar…"),
]
for en, ar, ms in JTX:
    AR_SRC.setdefault(en, ar)
_msx = json.load(open(_ms_path)); _ch = False
for en, ar, ms in JTX:
    if en not in _msx: _msx[en] = ms; _ch = True
if _ch: json.dump(_msx, open(_ms_path, "w"), ensure_ascii=False, indent=0)

JOBS = [
 dict(id="sales", t="Sales Executive (Arabic, English & Malay)", where="Remote or KL office", type="Full-time",
      p="You turn enquiries from WhatsApp, our website and ads into clients. You explain our services clearly, prepare quotes and follow up until the client is ready.",
      do=["Reply to new leads on WhatsApp and email, quickly and clearly", "Understand each client's goals and recommend the right package", "Prepare quotes in our system and follow up", "Keep every lead updated in our CRM"],
      need=["Fluent Arabic, English and Malay", "At least 1 year in sales, ideally services or B2B", "Honest selling: you never promise approvals we can't guarantee", "Comfortable working with targets"]),
 dict(id="support", t="Customer Support (WhatsApp)", where="Remote, in shifts", type="Full-time or part-time",
      p="You are the first reply our clients get. You answer questions, collect documents and keep clients updated while we work on their company.",
      do=["Answer client messages on WhatsApp in shifts", "Collect and check documents before we file", "Send clients clear status updates", "Pass interested leads to the sales team"],
      need=["Arabic, English and Malay", "Organised, patient and quick to reply", "Comfortable with WhatsApp Business and Google Sheets", "Available for shifts, including some weekends"]),
 dict(id="content", t="Content Creator (Video)", where="KL office or remote", type="Full-time or freelance",
      p="You make the short videos and posts that explain international business simply, for TikTok, Instagram and Reels, in English.",
      do=["Plan, film and edit short videos with our team", "Turn client stories and common questions into posts", "Write captions and track what performs", "Keep every post accurate and on brand"],
      need=["A portfolio of short-form videos", "Strong English, plus Arabic and Malay", "Editing in CapCut, Premiere or similar", "Interest in business and e-commerce"]),
]
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21zM12 12.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></g></svg>'
COIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.4 0-2.5.8-2.5 2s1.1 1.7 2.5 2 2.5.8 2.5 2-1.1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6.5V8M12 16v1.5"/></g></svg>'

def _job(j):
    lis = lambda xs: "".join(f"<li>{CHECK}{T('span', x)}</li>" for x in xs)
    return f'''<article class="jb" id="job-{j["id"]}">
  <div class="jb-h">{T("h3", j["t"])}
    <ul class="jb-tags"><li>{PIN}{T("span", j["where"])}</li><li>{CLOCK}{T("span", j["type"])}</li><li>{COIN}{T("span", "Salary + commission")}</li><li class="jb-my">{T("span", "Malaysian citizens only")}</li></ul></div>
  {T("p", j["p"], "jb-p")}
  <div class="jb-cols"><div>{T("h4", "What you'll do")}<ul class="jb-l">{lis(j["do"])}</ul></div><div>{T("h4", "What you bring")}<ul class="jb-l">{lis(j["need"])}</ul></div></div>
  <a class="btn solid jb-go" href="#apply" data-role="{esc(j["t"])}"><span class="dot"></span>{T("span", "Apply for this role")}</a>
</article>'''

why = [("Clients from 15 countries", "You work with founders from the Gulf, Africa, Asia and Europe, in Arabic, English and Malay."),
       ("Learn the whole business", "Company formation, banking, marketplaces and logistics: you see how international companies are really built."),
       ("Salary plus commission", "Every role has a fixed salary, and you earn commission on the clients you help bring in."),
       ("Remote or Kuala Lumpur", "Work from our office in Publika, Kuala Lumpur, or remotely from anywhere in Malaysia, depending on the role.")]
why_html = "".join(f'<article class="jw">{T("h3", h)}{T("p", p)}</article>' for h, p in why)
steps = [("Apply", "Fill in the form and attach your CV. It takes about 5 minutes."), ("Short call", "A 20-minute video call to get to know you."),
         ("Task or interview", "A small practical task or a second interview with the team."), ("Offer", "We send you a written offer with your salary and commission.")]
steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}</li>' for h, p in steps)

def _jl(id_, en): return f'<label for="{id_}"{tk(en)}>{esc(en)}</label>'
roles = [j["t"] for j in JOBS] + ["Open application"]
form = f'''<form id="jbForm" class="jb-form" novalidate>
  <p hidden><label>Leave this empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>
  <div class="full">{_jl("jb_role", "Role")}<select id="jb_role" name="role" required><option value=""{tk("Choose…")}>Choose…</option>{"".join(f'<option value="{esc(r)}"{tk(r)}>{esc(r)}</option>' for r in roles)}</select></div>
  <div>{_jl("jb_name", "Full name")}<input id="jb_name" name="name" autocomplete="name" maxlength="120" required></div>
  <div>{_jl("jb_email", "Email")}<input id="jb_email" name="email" type="email" dir="ltr" autocomplete="email" maxlength="200" required></div>
  <div>{_jl("jb_phone", "WhatsApp / phone")}<input id="jb_phone" name="phone" type="tel" dir="ltr" autocomplete="tel" maxlength="60" required></div>
  <div>{_jl("jb_country", "State / city in Malaysia")}<input id="jb_country" name="country" autocomplete="address-level1" maxlength="80" required></div>
  <div>{_jl("jb_setup", "Where do you want to work?")}<select id="jb_setup" name="setup">{"".join(f'<option value="{v}"{tk(v)}>{v}</option>' for v in ("Either", "Remote", "KL office"))}</select></div>
  <div>{_jl("jb_lang", "Languages you speak")}<input id="jb_lang" name="languages" maxlength="200"></div>
  <div class="full">{_jl("jb_link", "LinkedIn or portfolio link (optional)")}<input id="jb_link" name="link" type="url" dir="ltr" maxlength="300" placeholder="https://"></div>
  <div class="full">{_jl("jb_cv", "Your CV (PDF or Word, up to 4 MB)")}<input id="jb_cv" type="file" accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document" required></div>
  <div class="full">{_jl("jb_msg", "Why Wizz? (optional)")}<textarea id="jb_msg" name="message" maxlength="3000" rows="4"></textarea></div>
  <label class="rf-agree full jb-agree"><input type="checkbox" id="jb_my"> <span{tk("I confirm I am a Malaysian citizen.")}>I confirm I am a Malaysian citizen.</span></label>
  <label class="rf-agree full jb-agree"><input type="checkbox" id="jb_ok"> <span{tk("I agree that Wizz keeps my application for up to 12 months for hiring.")}>I agree that Wizz keeps my application for up to 12 months for hiring.</span></label>
  <div class="full formfoot"><button class="btn solid" type="submit"><span class="dot"></span>{T("span", "Send application")}</button><span class="jb-sending" hidden>{T("span", "Sending…")}</span></div>
  {T("p", "Please fill in the highlighted fields.", "err full jb-e1")}
  {T("p", "Please attach your CV as a PDF or Word file, up to 4 MB.", "err full jb-e2")}
  {T("p", "Sorry, something went wrong. Please try again, or message us on WhatsApp.", "err full jb-e3")}
</form>
<div class="out" id="jbOut" hidden role="status" tabindex="-1">
  <span class="out-ic">{CHECK}</span>
  {T("h2", "Application received", "out-t")}
  {T("p", "Thank you. We've emailed you a confirmation. If your profile fits, we'll contact you within two weeks to arrange a short call.", "out-p")}
  <p class="out-ref" id="jbRefW" hidden>{T("span", "Reference")}: <bdi id="jbRef"></bdi></p>
</div>'''

JB_JS = r"""<script>
(function(){
  const $=id=>document.getElementById(id), f=$('jbForm');
  const L=()=>document.documentElement.lang||'en';
  const emailOk=v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
  const [e1,e2,e3]=['.jb-e1','.jb-e2','.jb-e3'].map(s=>f.querySelector(s));
  document.querySelectorAll('.jb-go').forEach(a=>a.addEventListener('click',()=>{$('jb_role').value=a.dataset.role;$('jb_role').classList.remove('bad');}));
  const q=new URLSearchParams(location.search).get('role');if(q){const o=[...$('jb_role').options].find(o=>o.value.toLowerCase().startsWith(q.toLowerCase()));if(o)$('jb_role').value=o.value;}
  f.addEventListener('input',e=>e.target.classList&&e.target.classList.remove('bad'));
  f.addEventListener('change',e=>e.target.classList&&e.target.classList.remove('bad'));
  const read=file=>new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(String(r.result).split(',')[1]);r.onerror=rej;r.readAsDataURL(file);});
  f.addEventListener('submit',async e=>{
    e.preventDefault();[e1,e2,e3].forEach(x=>x.hidden=true);f.querySelectorAll('.bad').forEach(x=>x.classList.remove('bad'));
    const bad=[];
    f.querySelectorAll('[required]').forEach(x=>{if(x.type==='file')return;const v=x.value.trim();if(!v||(x.type==='email'&&!emailOk(v)))bad.push(x);});
    if(!$('jb_ok').checked)bad.push($('jb_ok').parentNode);if(!$('jb_my').checked)bad.push($('jb_my').parentNode);
    const file=$('jb_cv').files[0], okFile=file&&/\.(pdf|docx?)$/i.test(file.name)&&file.size<=4*1024*1024;
    if(!okFile)bad.push($('jb_cv'));
    if(bad.length){bad.forEach(x=>x.classList.add('bad'));(okFile||bad.length>1?e1:e2).hidden=false;if(!okFile&&bad.length>1)e2.hidden=false;bad[0].scrollIntoView({behavior:'smooth',block:'center'});return;}
    const b=f.querySelector('button[type=submit]'),s=f.querySelector('.jb-sending');b.disabled=true;s.hidden=false;
    try{
      const d=Object.fromEntries(new FormData(f));d.lang=L();d.citizen=$('jb_my').checked;d.cv={name:file.name,type:file.type,data:await read(file)};
      const r=await fetch('/.netlify/functions/careers',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||!j.ok){if(j.error==='bad_cv'){e2.hidden=false;$('jb_cv').classList.add('bad');return;}throw 0;}
      f.hidden=true;const o=$('jbOut');if(j.ref){$('jbRef').textContent=j.ref;$('jbRefW').hidden=false;}
      o.hidden=false;o.scrollIntoView({behavior:'smooth',block:'start'});o.focus({preventScroll:true});
      if(window.gtag)gtag('event','generate_lead',{form:'careers',role:d.role});
    }catch(_){e3.hidden=false;}finally{b.disabled=false;s.hidden=true;}
  });
})();
</script>"""

jb_body = hero_t("Careers", "Build your career beyond borders",
    "We help entrepreneurs from around the world start and grow their companies. Join a small team in Kuala Lumpur and online, and learn international business from the inside.") + f'''
<section class="block">
  <div class="wrap">
    {head("Careers", "Why work at Wizz")}
    <div class="jw-grid">{why_html}</div>
  </div>
</section>
<section class="block alt" id="roles">
  <div class="wrap">
    {head("Open roles", "Join the team", "Don't see your role? Send an open application below and we'll keep your CV on file.")}
    {T("p", "All roles are open to Malaysian citizens only, and need Arabic, English and Malay.", "jb-note")}
    <div class="jb-list">{"".join(_job(j) for j in JOBS)}</div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("How we hire", "Four simple steps")}
    <ol class="steps us-steps jb-steps">{steps_html}</ol>
  </div>
</section>
<section class="block alt" id="apply">
  <div class="wrap jb-wrap">
    {head("Apply now", "Send your application", "We review every application. If your profile fits, we contact you within two weeks.")}
    {T("p", "All roles are open to Malaysian citizens only, and need Arabic, English and Malay.", "jb-note")}
    {form}
  </div>
</section>'''
for _c in ("err full jb-e1", "err full jb-e2", "err full jb-e3"):
    jb_body = jb_body.replace(f'class="{_c}"', f'class="{_c}" hidden')
page("careers.html", "Careers at Wizz: Sales, Customer Support and Content Jobs | Wizz Smart Services",
     "Join Wizz Smart Services in Kuala Lumpur or remotely in Malaysia. Open roles for Malaysians who speak Arabic, English and Malay: Sales Executive, Customer Support (WhatsApp) and Content Creator. Salary plus commission.",
     jb_body, scripts=ar_script() + JB_JS)

US_CSS += """
.jw-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.jw{border:1px solid var(--line);border-top:4px solid var(--red);border-radius:var(--r);background:var(--surface);padding:20px}
.jw h3{font-size:18px;margin-bottom:8px}.jw p{margin:0;color:var(--muted);font-size:15px}
@media (max-width:980px){.jw-grid{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.jw-grid{grid-template-columns:1fr}}
.jb-list{display:grid;gap:18px}
.jb{border:1px solid var(--line);border-radius:var(--r);background:var(--surface);padding:clamp(20px,3vw,30px);display:flex;flex-direction:column;gap:14px}
.jb-h{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 20px;align-items:flex-start}
.jb-h h3{font-size:clamp(20px,2.2vw,24px)}
.jb-tags{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.jb-tags li{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:5px 11px}
.jb-tags svg{width:15px;height:15px;flex:none}
.jb-p{margin:0;color:var(--muted);max-width:75ch}
.jb-cols{display:grid;grid-template-columns:1fr 1fr;gap:18px 28px}
.jb-cols h4{margin:0 0 8px;font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
[dir="rtl"] .jb-cols h4{letter-spacing:0}
.jb-l{list-style:none;margin:0;padding:0;display:grid;gap:7px}
.jb-l li{display:flex;gap:9px;align-items:flex-start;font-size:15px}
.jb-l svg{width:18px;height:18px;flex:none;color:var(--red);margin-top:3px}
.jb-go{align-self:flex-start}
.jb-tags .jb-my{background:color-mix(in srgb,var(--red) 10%,var(--surface));border-color:color-mix(in srgb,var(--red) 35%,var(--line))}
.jb-note{margin:-6px 0 18px;font-weight:600;border-inline-start:3px solid var(--red);padding-inline-start:12px}
@media (max-width:700px){.jb-cols{grid-template-columns:1fr}}
.jb-steps{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:900px){.jb-steps{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.jb-steps{grid-template-columns:1fr}}
.jb-wrap{max-width:820px}
.jb-form .bad{border-color:var(--red)!important;box-shadow:0 0 0 1px var(--red)}
.jb-agree.bad{box-shadow:none;color:var(--red)}
.jb-form .err{margin:0}
.jb-form input[type=file]{padding:9px;background:var(--bg)}
.jb-sending{color:var(--muted);font-size:14px}
#jbOut{scroll-margin-top:96px}
"""
