# UK landing page (uk.html). Runs inside build_pkgs.py after us_page.py, reusing its helpers (T, icon, CHECK, head, US_CSS styles).
# Prices come from catalog.py (the UK entry). Facts checked October 2026: Companies House £100 incorporation, £50 confirmation
# statement (from 1 Feb 2026); director identity verification compulsory since 18 Nov 2025.

UK = next(c for c in COUNTRIES if c["c"] == "UK")
UK_MAIN = [t for t in UK["tiers"] if not t.get("grp")]
UK_ADDR = [t for t in UK["tiers"] if t.get("grp") == "uk-addr"]

UKAR = {
 "United Kingdom": "المملكة المتحدة",
 "Start your UK company from anywhere in the world": "أسّس شركتك البريطانية من أي مكان في العالم",
 "We register your private limited company at Companies House, handle director ID checks, give you a London address and set up your HMRC registrations. Fully remote, with a team you can reach on WhatsApp.":
   "نسجّل شركتك الخاصة المحدودة (Ltd) لدى Companies House، ونتولى التحقق من هوية المدير، ونوفر لك عنواناً في لندن، ونجهّز تسجيلاتك لدى مصلحة الضرائب HMRC. كل ذلك عن بُعد، مع فريق تتواصل معه عبر واتساب.",
 "See UK packages": "عرض باقات بريطانيا",
 "No UK residence needed": "لا حاجة للإقامة في بريطانيا",
 "Companies House fee included": "رسوم Companies House مشمولة",
 "London address options": "خيارات عنوان في لندن",
 "Your UK company kit": "حزمة شركتك البريطانية",
 "Private limited company (Ltd)": "شركة خاصة محدودة (Ltd)",
 "Certificate of incorporation": "شهادة التأسيس",
 "Articles of association": "النظام الأساسي (Articles of Association)",
 "Share certificates": "شهادات الأسهم",
 "Director ID verification": "التحقق من هوية المدير",
 "Registered office in London": "مكتب مسجّل في لندن",
 "Corporation Tax UTR": "الرقم الضريبي للشركة (UTR)",
 "Verified": "تم التحقق",
 "Start right. Stay compliant.": "ابدأ بشكل صحيح، وابقَ ملتزماً.",
 "Everything a non-UK founder needs to open and run a UK company, in one place.":
   "كل ما يحتاجه المؤسس من خارج بريطانيا لفتح شركة بريطانية وإدارتها، في مكان واحد.",
 "Ltd company formation": "تأسيس شركة Ltd",
 "We file your company at Companies House with the articles of association, share structure and officer details.":
   "نسجّل شركتك لدى Companies House مع النظام الأساسي وهيكل الأسهم وبيانات المسؤولين.",
 "Every director and person with significant control must verify their identity. We guide you through it before we file.":
   "يجب على كل مدير وكل شخص ذي سيطرة جوهرية التحقق من هويته، ونرشدك في ذلك قبل التقديم.",
 "Your company must have a UK registered office. Ours is in London, and you can add a director's address, a business address and call answering.":
   "يجب أن يكون لشركتك مكتب مسجّل في بريطانيا. مكتبنا في لندن، ويمكنك إضافة عنوان للمدير وعنوان تجاري وخدمة الرد على المكالمات.",
 "HMRC registrations": "التسجيل لدى HMRC",
 "We register your company for Corporation Tax and get your UTR, and handle VAT registration when your business needs it.":
   "نسجّل شركتك في ضريبة الشركات ونستخرج رقم UTR، ونتولى التسجيل في ضريبة القيمة المضافة (VAT) عندما يحتاجها نشاطك.",
 "We prepare and submit applications to providers such as Wise, Payoneer and Airwallex. Each provider makes its own decision.":
   "نجهّز ونقدّم الطلبات لدى مزوّدين مثل Wise وPayoneer وAirwallex. ولكل مزوّد قراره الخاص.",
 "The yearly confirmation statement, and first-year accounts through our accountant partner, so your company stays in good standing.":
   "تقديم بيان التأكيد السنوي، والحسابات السنوية الأولى عبر شريكنا المحاسب، لتبقى شركتك في وضع قانوني سليم.",
 "From first message to a working UK company": "من أول رسالة إلى شركة بريطانية جاهزة للعمل",
 "Verify your identity": "تحقق من هويتك",
 "Each director confirms their identity with Companies House online, using a passport. We tell you exactly what to do.":
   "يؤكد كل مدير هويته لدى Companies House عبر الإنترنت باستخدام جواز السفر، ونخبرك بالخطوات بالتفصيل.",
 "Usually 1 to 3 days": "عادةً من يوم إلى 3 أيام",
 "We file at Companies House": "نقدّم الطلب لدى Companies House",
 "We submit your company and you receive the certificate of incorporation.": "نقدّم طلب تأسيس شركتك وتستلم شهادة التأسيس.",
 "Usually within 24 hours": "عادةً خلال 24 ساعة",
 "HMRC and VAT": "HMRC وضريبة القيمة المضافة",
 "We register you for Corporation Tax, and for VAT if needed.": "نسجّلك في ضريبة الشركات، وفي ضريبة القيمة المضافة إذا لزم.",
 "UTR usually arrives in 2 to 4 weeks": "يصل رقم UTR عادةً خلال 2 إلى 4 أسابيع",
 "Bank, payments and launch": "البنك والمدفوعات والانطلاق",
 "We prepare your bank and payment applications, and you start trading.": "نجهّز طلبات الحسابات البنكية وحسابات الدفع، وتبدأ نشاطك التجاري.",
 "Why a UK company": "لماذا شركة بريطانية",
 "A trusted company you can run from abroad": "شركة موثوقة يمكنك إدارتها من الخارج",
 "A UK Ltd gives you": "ما تمنحك إياه شركة Ltd بريطانية",
 "A respected structure that customers, suppliers and marketplaces recognise worldwide.":
   "هيكل قانوني محترم يعرفه العملاء والموردون والمنصات حول العالم.",
 "Any nationality can be a director and shareholder": "يمكن لأي جنسية أن تكون مديراً ومساهماً",
 "Limited liability: your personal assets are protected": "مسؤولية محدودة: أصولك الشخصية محمية",
 "Access to Amazon UK, TikTok Shop UK and European marketplaces": "الوصول إلى أمازون بريطانيا وتيك توك شوب بريطانيا والمنصات الأوروبية",
 "One of the fastest company registers in the world": "من أسرع سجلات الشركات في العالم",
 "What you keep up each year": "ما يجب الالتزام به سنوياً",
 "UK companies have a few fixed yearly duties. We remind you of each one.": "على الشركات البريطانية التزامات سنوية محددة، ونذكّرك بكل منها.",
 "Confirmation statement at Companies House (£50 fee)": "بيان التأكيد لدى Companies House (رسوم 50 جنيهاً)",
 "Annual accounts, due 9 months after your year end": "الحسابات السنوية، خلال 9 أشهر من نهاية السنة المالية",
 "Company Tax Return to HMRC": "الإقرار الضريبي للشركة لدى HMRC",
 "A UK registered office address at all times": "عنوان مكتب مسجّل في بريطانيا في جميع الأوقات",
 "UK packages": "باقات بريطانيا",
 "One price, with the Companies House fee included. Pay in your own currency.": "سعر واحد يشمل رسوم Companies House، وادفع بعملتك المحلية.",
 "Built for founders selling in the UK and Europe": "مصمّمة للمؤسسين الذين يبيعون في بريطانيا وأوروبا",
 "Amazon UK and EU sellers": "بائعو أمازون بريطانيا وأوروبا",
 "Sell on Amazon.co.uk and expand to Amazon Europe with a UK company behind your account.":
   "بِع على Amazon.co.uk وتوسّع إلى أمازون أوروبا بشركة بريطانية خلف حسابك.",
 "Brands on Shopify and TikTok Shop UK": "العلامات التجارية على شوبيفاي وتيك توك شوب بريطانيا",
 "Build a UK-facing brand with a London address and UK company details customers trust.":
   "ابنِ علامة تجارية موجّهة للسوق البريطاني بعنوان في لندن وبيانات شركة بريطانية يثق بها العملاء.",
 "Consultants and agencies": "المستشارون والوكالات",
 "Invoice UK and European clients from a UK company and apply for GBP and EUR payment accounts.":
   "أصدر فواتيرك للعملاء في بريطانيا وأوروبا من شركة بريطانية، وقدّم طلب حسابات دفع بالجنيه واليورو.",
 "Import, export and trade with UK buyers and suppliers, with logistics support from our network.":
   "استورد وصدّر وتعامل مع المشترين والموردين في بريطانيا، مع دعم لوجستي من شبكتنا.",
 "UK company questions": "أسئلة عن الشركة البريطانية",
 "Do I need to live in the UK or have a UK director?": "هل يجب أن أعيش في بريطانيا أو أن يكون لدي مدير بريطاني؟",
 "No. Directors and shareholders can be any nationality and live anywhere. You need a UK registered office address, which we provide.":
   "لا. يمكن أن يكون المديرون والمساهمون من أي جنسية ويقيمون في أي مكان. تحتاج فقط إلى عنوان مكتب مسجّل في بريطانيا، ونحن نوفره.",
 "What is director identity verification?": "ما هو التحقق من هوية المدير؟",
 "Since November 2025, every new director and person with significant control must verify their identity with Companies House before the company is filed. It's done online with a passport, and we guide you through it.":
   "منذ نوفمبر 2025، يجب على كل مدير جديد وكل شخص ذي سيطرة جوهرية التحقق من هويته لدى Companies House قبل تسجيل الشركة. يتم ذلك عبر الإنترنت باستخدام جواز السفر، ونرشدك في كل خطوة.",
 "A copy of your passport, your full residential address, your national ID number, a few company name choices, the share split between owners and a short description of your business.":
   "نسخة من جواز السفر، وعنوان سكنك الكامل، ورقم الهوية الوطنية، وعدة خيارات لاسم الشركة، وتوزيع الأسهم بين الملّاك، ووصف مختصر لنشاطك.",
 "Once identity checks are done, Companies House usually registers the company within 24 hours. Your Corporation Tax UTR usually arrives in 2 to 4 weeks. Bank and payment accounts depend on each provider.":
   "بعد إتمام التحقق من الهوية، تسجّل Companies House الشركة عادةً خلال 24 ساعة. ويصل رقم UTR عادةً خلال 2 إلى 4 أسابيع. أما الحسابات البنكية وحسابات الدفع فتعتمد على كل مزوّد.",
 "Will I get a UK bank account?": "هل سأحصل على حساب بنكي بريطاني؟",
 "We prepare and submit complete applications to suitable providers such as Wise, Payoneer and Airwallex. Approval is always the provider's decision, based on their own checks, so no one can guarantee it.":
   "نجهّز ونقدّم طلبات كاملة لدى مزوّدين مناسبين مثل Wise وPayoneer وAirwallex. والموافقة دائماً قرار المزوّد بناءً على فحوصاته الخاصة، لذلك لا يمكن لأحد أن يضمنها.",
 "Does a UK company give me a visa or the right to live in the UK?": "هل تمنحني الشركة البريطانية تأشيرة أو حق الإقامة في بريطانيا؟",
 "No. Owning a UK company does not give you a visa, residence or the right to work in the UK. Immigration is a separate process.":
   "لا. امتلاك شركة بريطانية لا يمنحك تأشيرة أو إقامة أو حق العمل في بريطانيا. الهجرة إجراء منفصل تماماً.",
 "UK companies pay Corporation Tax on their profits, currently between 19% and 25%, and may need to register for VAT. What you owe also depends on where you live and where the work is done, so we refer you to a qualified tax professional for advice.":
   "تدفع الشركات البريطانية ضريبة الشركات على أرباحها، وتتراوح حالياً بين 19% و25%، وقد تحتاج إلى التسجيل في ضريبة القيمة المضافة. ويعتمد ما عليك أيضاً على مكان إقامتك ومكان أداء العمل، لذلك نحيلك إلى مختص ضرائب مؤهل للاستشارة.",
 "Can I use my own address as the registered office?": "هل يمكنني استخدام عنواني كمكتب مسجّل؟",
 "Only if it's in the UK. The registered office must be a UK address where official letters can be delivered, and it is shown publicly. Our London address plans cover this and keep your home address private.":
   "فقط إذا كان في بريطانيا. يجب أن يكون المكتب المسجّل عنواناً بريطانياً تُسلَّم إليه الرسائل الرسمية، ويظهر للعموم. وباقات عناويننا في لندن تغطي ذلك وتحافظ على خصوصية عنوان منزلك.",
 "You file a confirmation statement and annual accounts each year, plus a Company Tax Return. We send reminders, and the Complete package covers the first year with our accountant partner.":
   "تقدّم بيان التأكيد والحسابات السنوية كل عام، إضافة إلى الإقرار الضريبي للشركة. نرسل لك التذكيرات، وتغطي باقة Complete السنة الأولى مع شريكنا المحاسب.",
 "Ready to start your UK company?": "جاهز لتأسيس شركتك البريطانية؟",
 "Start my UK company": "ابدأ شركتي البريطانية",
 "UK Ltd formation for non-residents, from Companies House filing and director ID checks to a London address, HMRC registration and yearly compliance.":
   "تأسيس شركة Ltd بريطانية لغير المقيمين، من التسجيل لدى Companies House والتحقق من هوية المدير إلى عنوان في لندن والتسجيل لدى HMRC والالتزامات السنوية.",
 "Everything about forming a UK company": "كل شيء عن تأسيس شركة بريطانية",
}
AR_SRC.update({k: v for k, v in UKAR.items() if k not in AR_SRC})

uk_start = UK_MAIN[0]
uk_kit_rows = [("Certificate of incorporation", "Issued"), ("Articles of association", "Ready"), ("Share certificates", "Ready"),
               ("Director ID verification", "Verified"), ("Registered office in London", "Active"), ("Corporation Tax UTR", "Issued"),
               ("Bank & payment applications", "In review")]
uk_kit = "".join(f'<li><span class="us-kit-ck">{CHECK}</span>{T("span", a)}{T("em", b, "pend" if b == "In review" else "")}</li>' for a, b in uk_kit_rows)

uk_hero = f'''<section class="page-hero night us-hero">
  <div class="wrap">
    <div>
      <p class="eyebrow"><span class="ltr">UK</span> · {T("span", "United Kingdom")}</p>
      {T("h1", "Start your UK company from anywhere in the world")}
      {T("p", "We register your private limited company at Companies House, handle director ID checks, give you a London address and set up your HMRC registrations. Fully remote, with a team you can reach on WhatsApp.", "lede")}
      <div class="us-cta">
        <a class="btn solid us-red" href="#pricing"><span class="dot"></span>{T("span", "See UK packages")}</a>
        <a class="btn ghost us-ghost" href="contact.html">{T("span", "Free consultation")}</a>
      </div>
      <ul class="us-trust">
        <li>{CHECK}{T("span", "No UK residence needed")}</li>
        <li>{CHECK}{T("span", "100% foreign ownership")}</li>
        <li>{CHECK}{T("span", "Companies House fee included")}</li>
        <li>{CHECK}{T("span", "London address options")}</li>
      </ul>
    </div>
    <div class="us-kit" aria-hidden="true">
      <div class="us-kit-top"><span class="us-kit-flag ltr">UK<i>.</i></span><div>{T("b", "Your UK company kit")}{T("small", "Private limited company (Ltd)")}</div>
        <span class="us-kit-price">{T("span", "from")} {money(uk_start["p"], uk_start.get("fix"))}</span></div>
      <ul>{uk_kit}</ul>
    </div>
  </div>
</section>
<p class="us-disc wrap"><span{tk("Wizz Smart Services is a private company. We are not a government agency or a law firm.")}>Wizz Smart Services is a private company. We are not a government agency or a law firm.</span></p>'''

uk_feats = [("llc", "Ltd company formation", "We file your company at Companies House with the articles of association, share structure and officer details."),
            ("agent", "Director ID verification", "Every director and person with significant control must verify their identity. We guide you through it before we file."),
            ("addr", "Registered office in London", "Your company must have a UK registered office. Ours is in London, and you can add a director's address, a business address and call answering."),
            ("ein", "HMRC registrations", "We register your company for Corporation Tax and get your UTR, and handle VAT registration when your business needs it."),
            ("bank", "Bank & payment applications", "We prepare and submit applications to providers such as Wise, Payoneer and Airwallex. Each provider makes its own decision."),
            ("cal", "Yearly compliance", "The yearly confirmation statement, and first-year accounts through our accountant partner, so your company stays in good standing.")]
uk_feat_html = "".join(f'<article class="us-feat">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in uk_feats)

uk_steps = [("Tell us about your business", "Choose a package and send your passport and details through your client account.", "About 15 minutes"),
            ("Verify your identity", "Each director confirms their identity with Companies House online, using a passport. We tell you exactly what to do.", "Usually 1 to 3 days"),
            ("We file at Companies House", "We submit your company and you receive the certificate of incorporation.", "Usually within 24 hours"),
            ("HMRC and VAT", "We register you for Corporation Tax, and for VAT if needed.", "UTR usually arrives in 2 to 4 weeks"),
            ("Bank, payments and launch", "We prepare your bank and payment applications, and you start trading.", "Depends on each provider")]
uk_steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}<span class="us-time">{T("span", t)}</span></li>' for h, p, t in uk_steps)

uk_ents = ent("A UK Ltd gives you", "A respected structure that customers, suppliers and marketplaces recognise worldwide.",
              ["Any nationality can be a director and shareholder", "Limited liability: your personal assets are protected",
               "Access to Amazon UK, TikTok Shop UK and European marketplaces", "One of the fastest company registers in the world"]) + \
          ent("What you keep up each year", "UK companies have a few fixed yearly duties. We remind you of each one.",
              ["Confirmation statement at Companies House (£50 fee)", "Annual accounts, due 9 months after your year end",
               "Company Tax Return to HMRC", "A UK registered office address at all times"])

uk_rows = [(item, i) for i, t in enumerate(UK_MAIN) for item in t["i"]]
uk_thead = "".join(f'<th scope="col">{T("span", t["n"])}<small>{money(t["p"], t.get("fix"))}</small></th>' for t in UK_MAIN)
uk_tbody = "".join(f'<tr><th scope="row"{tk(item)}>{esc(item)}</th>' + "".join(cell(j >= i) for j in range(len(UK_MAIN))) + "</tr>" for item, i in uk_rows)
uk_notes = "".join(f'<p class="pk-note"{tk(n, money_text)}>{money_text(n)}</p>' for n in UK["notes"])
uk_addr_title, uk_addr_lede = UK["groups"]["uk-addr"]

uk_who = [("cart", "Amazon UK and EU sellers", "Sell on Amazon.co.uk and expand to Amazon Europe with a UK company behind your account."),
          ("brand", "Brands on Shopify and TikTok Shop UK", "Build a UK-facing brand with a London address and UK company details customers trust."),
          ("code", "Consultants and agencies", "Invoice UK and European clients from a UK company and apply for GBP and EUR payment accounts."),
          ("ship", "Traders and importers", "Import, export and trade with UK buyers and suppliers, with logistics support from our network.")]
uk_who_html = "".join(f'<article class="us-who">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in uk_who)

uk_faqs = [("Do I need to live in the UK or have a UK director?", "No. Directors and shareholders can be any nationality and live anywhere. You need a UK registered office address, which we provide."),
           ("What is director identity verification?", "Since November 2025, every new director and person with significant control must verify their identity with Companies House before the company is filed. It's done online with a passport, and we guide you through it."),
           ("What do you need from me?", "A copy of your passport, your full residential address, your national ID number, a few company name choices, the share split between owners and a short description of your business."),
           ("How long does it take?", "Once identity checks are done, Companies House usually registers the company within 24 hours. Your Corporation Tax UTR usually arrives in 2 to 4 weeks. Bank and payment accounts depend on each provider."),
           ("Will I get a UK bank account?", "We prepare and submit complete applications to suitable providers such as Wise, Payoneer and Airwallex. Approval is always the provider's decision, based on their own checks, so no one can guarantee it."),
           ("Does a UK company give me a visa or the right to live in the UK?", "No. Owning a UK company does not give you a visa, residence or the right to work in the UK. Immigration is a separate process."),
           ("What taxes will I pay?", "UK companies pay Corporation Tax on their profits, currently between 19% and 25%, and may need to register for VAT. What you owe also depends on where you live and where the work is done, so we refer you to a qualified tax professional for advice."),
           ("Can I use my own address as the registered office?", "Only if it's in the UK. The registered office must be a UK address where official letters can be delivered, and it is shown publicly. Our London address plans cover this and keep your home address private."),
           ("What happens after the first year?", "You file a confirmation statement and annual accounts each year, plus a Company Tax Return. We send reminders, and the Complete package covers the first year with our accountant partner.")]
uk_faq_html = "".join(f"<details><summary{tk(q)}>{esc(q)}</summary>{T('p', a)}</details>" for q, a in uk_faqs)
uk_faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in uk_faqs]}, ensure_ascii=False)

uk_body = uk_hero + f'''
<section class="block">
  <div class="wrap">
    {head("What you get", "Start right. Stay compliant.", "Everything a non-UK founder needs to open and run a UK company, in one place.")}
    <div class="us-feats">{uk_feat_html}</div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("How it works", "From first message to a working UK company", "Times are typical. Government offices and providers set their own pace.")}
    <ol class="steps us-steps">{uk_steps_html}</ol>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("Why a UK company", "A trusted company you can run from abroad")}
    <div class="us-ents us-ents-txt">{uk_ents}</div>
  </div>
</section>
<section class="block alt" id="pricing">
  <div class="wrap">
    {head("Pricing", "UK packages", "One price, with the Companies House fee included. Pay in your own currency.")}
    <div class="pk-curbar"><label for="pkCur"{tk("Prices in")}>Prices in</label><select id="pkCur"><option value="USD">USD · US dollar</option></select><span class="pk-curnote" id="pkCurNote">Set in US dollars. Change the currency if you prefer.</span></div>
    <div class="pk-grid">{"".join(tier_html(UK, t) for t in UK_MAIN)}</div>
    <div class="pk-sub"><h3{tk(uk_addr_title)}>{esc(uk_addr_title)}</h3><p{tk(uk_addr_lede)}>{esc(uk_addr_lede)}</p></div>
    <div class="pk-grid pk-grid-sm">{"".join(tier_html(UK, t) for t in UK_ADDR)}</div>
    {uk_notes}
    <div class="pk-msg" id="pkMsg" role="status" hidden></div>
    {T("h3", "Compare packages", "us-cmp-h")}
    <div class="us-cmp-wrap"><table class="us-cmp"><thead><tr><th scope="col"{tk("Feature")}>Feature</th>{uk_thead}</tr></thead><tbody>{uk_tbody}</tbody></table></div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("Who we help", "Built for founders selling in the UK and Europe")}
    <div class="us-whos">{uk_who_html}</div>
  </div>
</section>
<section class="block alt" id="faq">
  <div class="wrap faq-layout">
    <div>{T("p", "Questions", "eyebrow")}{T("h2", "UK company questions")}</div>
    <div class="faq">{uk_faq_html}</div>
  </div>
</section>
<section class="us-final night">
  <div class="wrap">
    {T("h2", "Ready to start your UK company?")}
    {T("p", "Pick a package today, or talk to us first. We reply on WhatsApp and email.")}
    <div class="us-cta">
      <a class="btn solid us-red" href="#pricing"><span class="dot"></span>{T("span", "Start my UK company")}</a>
      <a class="btn ghost us-ghost" href="https://wa.me/601124477685?text=Hi%20Wizz%2C%20I%27d%20like%20to%20start%20a%20UK%20company." target="_blank" rel="noopener">{T("span", "Chat on WhatsApp")}</a>
    </div>
  </div>
</section>'''

page("uk.html", "UK Company Formation for Non-Residents | Ltd + London Address | Wizz Smart Services",
     f"Form a UK private limited company from anywhere: Companies House fee, director ID checks and London registered office, from ${uk_start['p']}. Fully remote, with WhatsApp support.",
     uk_body, extra_head=f'<script type="application/ld+json">{uk_faq_ld}</script>', scripts=ar_script() + PK_JS)
