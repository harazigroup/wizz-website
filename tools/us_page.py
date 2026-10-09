# US landing page (usa.html). Run inside build_pkgs.py (exec), so page(), tk(), tier_html(), PK_JS, money_text() exist.
# Prices come from catalog.py (the US entry), so changing a US price there updates this page too.

US = next(c for c in COUNTRIES if c["c"] == "US")

# Real client stories only, with the client's written permission to show their name and photo.
# Example: dict(name="Full Name", role="Founder, Brand (Amazon US)", country="Oman", photo="img/clients/name.webp",
#               quote="What they said, in their words.", quote_ar="Arabic version")
TESTIMONIALS = []

USAR = {
 "United States": "الولايات المتحدة",
 "Start your US company from anywhere in the world": "أسّس شركتك الأمريكية من أي مكان في العالم",
 "We form your LLC, apply for your EIN and set up the address and paperwork you need to sell to US customers. Fully remote, with a team you can reach on WhatsApp.":
   "نؤسس شركتك ذات المسؤولية المحدودة (LLC)، ونقدّم طلب الرقم الضريبي EIN، ونجهّز العنوان والمستندات التي تحتاجها للبيع للعملاء في أمريكا. كل ذلك عن بُعد، مع فريق تتواصل معه عبر واتساب.",
 "See US packages": "عرض باقات أمريكا",
 "Free consultation": "استشارة مجانية",
 "No US visit needed": "لا حاجة لزيارة أمريكا",
 "100% foreign ownership": "ملكية أجنبية 100%",
 "State fee included": "رسوم الولاية مشمولة",
 "EIN for non-residents": "رقم EIN لغير المقيمين",
 "Your US company kit": "حزمة شركتك الأمريكية",
 "Wyoming LLC": "شركة LLC في وايومنغ",
 "Articles of organization": "عقد التأسيس (Articles of Organization)",
 "Operating agreement": "اتفاقية التشغيل (Operating Agreement)",
 "EIN confirmation letter": "خطاب تأكيد الرقم الضريبي EIN",
 "Registered agent": "الوكيل المسجّل",
 "US business address": "عنوان تجاري في أمريكا",
 "Bank & payment applications": "طلبات الحسابات البنكية وحسابات الدفع",
 "Filed": "تم التقديم",
 "Issued": "صدر",
 "Active": "مفعّل",
 "Ready": "جاهز",
 "In review": "قيد المراجعة",
 "from": "من",
 "Wizz Smart Services is a private company. We are not a government agency or a law firm.":
   "ويز للخدمات الذكية شركة خاصة، ولسنا جهة حكومية ولا مكتب محاماة.",
 "What you get": "ما تحصل عليه",
 "Start right. Stay compliant.": "ابدأ بشكل صحيح، وابقَ ملتزماً.",
 "Everything a non-US founder needs to open and run a US company, in one place.":
   "كل ما يحتاجه المؤسس من خارج أمريكا لفتح شركة أمريكية وإدارتها، في مكان واحد.",
 "LLC formation": "تأسيس شركة LLC",
 "We file your LLC with the state and prepare your articles of organization and operating agreement.":
   "نسجّل شركتك لدى الولاية ونجهّز عقد التأسيس واتفاقية التشغيل.",
 "EIN (US tax ID)": "الرقم الضريبي الأمريكي (EIN)",
 "We apply to the IRS for your Employer Identification Number. You don't need an SSN or ITIN.":
   "نقدّم طلب رقم التعريف الضريبي لدى مصلحة الضرائب الأمريكية (IRS). لا تحتاج إلى رقم ضمان اجتماعي (SSN) أو ITIN.",
 "A registered agent in your state receives official mail and legal notices for your company.":
   "يستلم الوكيل المسجّل في ولايتك البريد الرسمي والإشعارات القانونية الخاصة بشركتك.",
 "A US mailing address for your company, with scans of the letters you receive.":
   "عنوان بريدي أمريكي لشركتك، مع نسخ ممسوحة ضوئياً من الرسائل التي تصلك.",
 "We prepare and submit applications to providers such as Wise, Payoneer and Stripe. Each provider makes its own decision.":
   "نجهّز ونقدّم الطلبات لدى مزوّدين مثل Wise وPayoneer وStripe. ولكل مزوّد قراره الخاص.",
 "Yearly compliance": "الالتزامات السنوية",
 "Form 5472 and pro-forma 1120, the state annual report and reminders, so your company stays in good standing.":
   "نموذج 5472 ونموذج 1120 الشكلي، والتقرير السنوي للولاية مع التذكيرات، لتبقى شركتك في وضع قانوني سليم.",
 "How it works": "كيف تتم العملية",
 "From first message to a working US company": "من أول رسالة إلى شركة أمريكية جاهزة للعمل",
 "Times are typical. Government offices and providers set their own pace.":
   "المدد تقريبية، فالجهات الحكومية والمزوّدون يحددون سرعتهم بأنفسهم.",
 "Tell us about your business": "أخبرنا عن نشاطك",
 "Choose a package and send your passport and details through your client account.":
   "اختر باقة وأرسل جواز سفرك وبياناتك عبر حسابك لدينا.",
 "About 15 minutes": "حوالي 15 دقيقة",
 "We verify and file": "نتحقق ونقدّم الطلب",
 "We check your identity, then file your LLC with the state.": "نتحقق من هويتك، ثم نسجّل شركتك لدى الولاية.",
 "1 to 3 business days after checks": "من يوم إلى 3 أيام عمل بعد التحقق",
 "We get your EIN": "نستخرج رقم EIN",
 "We apply to the IRS for your company's tax ID.": "نقدّم طلب الرقم الضريبي لشركتك لدى مصلحة الضرائب الأمريكية.",
 "Usually 2 to 6 weeks for non-residents": "عادةً من أسبوعين إلى 6 أسابيع لغير المقيمين",
 "Address, bank and payments": "العنوان والبنك والمدفوعات",
 "Your US address goes live and we prepare your bank and payment applications.":
   "يتم تفعيل عنوانك الأمريكي ونجهّز طلبات الحسابات البنكية وحسابات الدفع.",
 "Depends on each provider": "حسب كل مزوّد",
 "Launch and grow": "انطلق وتوسّع",
 "Start selling, and we remind you of every yearly filing.": "ابدأ البيع، ونذكّرك بكل التزام سنوي.",
 "Ongoing": "مستمر",
 "Which structure and state?": "أي هيكل وأي ولاية؟",
 "Most non-US founders choose an LLC": "معظم المؤسسين من خارج أمريكا يختارون شركة LLC",
 "We help you pick in your free consultation. For tax questions specific to your country, we refer you to a qualified tax professional.":
   "نساعدك في الاختيار خلال الاستشارة المجانية. وللأسئلة الضريبية الخاصة ببلدك، نحيلك إلى مختص ضرائب مؤهل.",
 "LLC": "LLC",
 "C-Corp": "C-Corp",
 "Simple to run and the usual choice for e-commerce sellers, agencies and online services.":
   "سهلة الإدارة وهي الخيار المعتاد لبائعي التجارة الإلكترونية والوكالات والخدمات الرقمية.",
 "Can be 100% owned by non-residents, alone or with partners": "يمكن أن تكون مملوكة 100% لغير المقيمين، بشكل فردي أو مع شركاء",
 "Protects your personal assets from business debts": "تحمي أصولك الشخصية من ديون الشركة",
 "Light yearly paperwork": "التزامات ورقية سنوية بسيطة",
 "Doesn't issue shares to investors": "لا تُصدر أسهماً للمستثمرين",
 "For startups that plan to raise money from investors.": "للشركات الناشئة التي تخطط لجمع تمويل من المستثمرين.",
 "Issues shares and stock options": "تُصدر أسهماً وخيارات أسهم",
 "Preferred by most venture investors, usually in Delaware": "يفضّلها معظم المستثمرين، وغالباً في ولاية ديلاوير",
 "More formal rules and yearly filings": "قواعد أكثر رسمية والتزامات سنوية أكبر",
 "Available on request, with a written quote": "متاحة عند الطلب، بعرض سعر مكتوب",
 "Wyoming": "وايومنغ",
 "Our default. Low yearly costs and strong privacy for owners.": "خيارنا الافتراضي. تكاليف سنوية منخفضة وخصوصية قوية للملّاك.",
 "New Mexico": "نيو مكسيكو",
 "No annual report, so the lowest running cost.": "لا يتطلب تقريراً سنوياً، لذا فهو الأقل تكلفة في التشغيل.",
 "Delaware": "ديلاوير",
 "Best known with investors. Higher yearly state tax.": "الأشهر لدى المستثمرين، مع ضريبة سنوية أعلى للولاية.",
 "Pricing": "الأسعار",
 "US packages": "باقات أمريكا",
 "One price, with the state filing fee included. Pay in your own currency.": "سعر واحد يشمل رسوم التسجيل في الولاية، وادفع بعملتك المحلية.",
 "Compare packages": "قارن بين الباقات",
 "Feature": "الميزة",
 "Included": "مشمول",
 "Not included": "غير مشمول",
 "Who we help": "من نساعد",
 "Built for founders selling to the US": "مصمّمة للمؤسسين الذين يبيعون للسوق الأمريكي",
 "Amazon and e-commerce sellers": "بائعو أمازون والتجارة الإلكترونية",
 "Sell on Amazon.com, Walmart or TikTok Shop US with a US company and EIN. We also help with seller account applications.":
   "بِع على Amazon.com أو Walmart أو TikTok Shop الأمريكي بشركة أمريكية ورقم EIN. ونساعدك أيضاً في طلبات حسابات البائعين.",
 "Shopify and private-label brands": "متاجر شوبيفاي والعلامات التجارية الخاصة",
 "Build your own brand with a US entity, address and payment applications behind it.":
   "ابنِ علامتك التجارية الخاصة بكيان أمريكي وعنوان وطلبات حسابات دفع تدعمها.",
 "Agencies, SaaS and freelancers": "الوكالات وشركات البرمجيات والمستقلون",
 "Invoice US clients from a US company and apply for USD payment accounts.":
   "أصدر فواتيرك للعملاء الأمريكيين من شركة أمريكية، وقدّم طلب حسابات دفع بالدولار.",
 "Traders and importers": "التجار والمستوردون",
 "Trade with US suppliers and buyers, with logistics support from our network.":
   "تعامل مع الموردين والمشترين في أمريكا، مع دعم لوجستي من شبكتنا.",
 "Client stories": "قصص عملائنا",
 "Founders who started with Wizz": "مؤسسون بدأوا مع ويز",
 "Questions": "أسئلة",
 "US company questions": "أسئلة عن الشركة الأمريكية",
 "Do I need to be a US citizen or live in the US?": "هل يجب أن أكون مواطناً أمريكياً أو مقيماً في أمريكا؟",
 "No. Non-residents can own 100% of a US LLC. You don't need to travel to the US, and you don't need an SSN or ITIN to get an EIN.":
   "لا. يمكن لغير المقيمين امتلاك 100% من شركة LLC أمريكية. لا تحتاج للسفر إلى أمريكا، ولا تحتاج إلى SSN أو ITIN للحصول على رقم EIN.",
 "What do you need from me?": "ما المطلوب مني؟",
 "A copy of your passport, your full residential address, your national ID number, a few company name choices and a short description of your business.":
   "نسخة من جواز السفر، وعنوان سكنك الكامل، ورقم الهوية الوطنية، وعدة خيارات لاسم الشركة، ووصف مختصر لنشاطك.",
 "How long does it take?": "كم تستغرق العملية؟",
 "The LLC is usually filed within 1 to 3 business days after our checks. The EIN usually takes 2 to 6 weeks for non-residents. Bank and payment accounts depend on each provider.":
   "يتم تسجيل الشركة عادةً خلال يوم إلى 3 أيام عمل بعد التحقق. ويستغرق رقم EIN عادةً من أسبوعين إلى 6 أسابيع لغير المقيمين. أما الحسابات البنكية وحسابات الدفع فتعتمد على كل مزوّد.",
 "Will I get a US bank account and Stripe?": "هل سأحصل على حساب بنكي أمريكي وعلى Stripe؟",
 "We prepare and submit complete applications to suitable providers such as Wise, Payoneer and Stripe. Approval is always the provider's decision, based on their own checks, so no one can guarantee it.":
   "نجهّز ونقدّم طلبات كاملة لدى مزوّدين مناسبين مثل Wise وPayoneer وStripe. والموافقة دائماً قرار المزوّد بناءً على فحوصاته الخاصة، لذلك لا يمكن لأحد أن يضمنها.",
 "Does a US company give me a visa or residency?": "هل تمنحني الشركة الأمريكية تأشيرة أو إقامة؟",
 "No. Forming a company does not give you a visa, residency or the right to work in the US. Immigration is a separate process.":
   "لا. تأسيس شركة لا يمنحك تأشيرة أو إقامة أو حق العمل في أمريكا. الهجرة إجراء منفصل تماماً.",
 "What taxes will I pay?": "ما الضرائب التي سأدفعها؟",
 "It depends on your activity, where you live and where your customers are. Every foreign-owned LLC must file Form 5472 each year, which our Complete package covers. For tax advice we refer you to a qualified tax professional.":
   "يعتمد ذلك على نشاطك ومكان إقامتك ومكان عملائك. وعلى كل شركة LLC مملوكة لأجنبي تقديم نموذج 5472 سنوياً، وهو مشمول في باقة Complete. وللاستشارات الضريبية نحيلك إلى مختص ضرائب مؤهل.",
 "What happens after the first year?": "ماذا يحدث بعد السنة الأولى؟",
 "You renew the registered agent and file the state's annual report, and the federal filings continue each year. We send reminders and can handle the renewal for you.":
   "تجدد خدمة الوكيل المسجّل وتقدّم التقرير السنوي للولاية، وتستمر الالتزامات الفيدرالية كل عام. نرسل لك التذكيرات ويمكننا تولّي التجديد عنك.",
 "Ready to start your US company?": "جاهز لتأسيس شركتك الأمريكية؟",
 "Pick a package today, or talk to us first. We reply on WhatsApp and email.":
   "اختر باقتك اليوم، أو تحدث معنا أولاً. نرد عبر واتساب والبريد الإلكتروني.",
 "Start my US company": "ابدأ شركتي الأمريكية",
 "Chat on WhatsApp": "تواصل عبر واتساب",
 "US company formation guide": "دليل تأسيس شركة أمريكية",
 "Everything about forming a US company": "كل شيء عن تأسيس شركة أمريكية",
}
AR_SRC.update({k: v for k, v in USAR.items() if k not in AR_SRC})

def T(tag, en, cls="", render=None):
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c}{tk(en, render)}>{(render or esc)(en)}</{tag}>"

CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3L15 6.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICONS = {
 "llc": '<path d="M7 3h7l5 5v13H7z M14 3v5h5 M10 13h6 M10 17h6"/>',
 "ein": '<path d="M4 6h16v12H4z M8 10h3 M8 14h8 M15 9.5h2"/>',
 "agent": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z M9 12l2 2 4-4"/>',
 "addr": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z M12 12.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>',
 "bank": '<path d="M3 10l9-6 9 6 M5 10v8 M9.5 10v8 M14.5 10v8 M19 10v8 M3 21h18"/>',
 "cal": '<path d="M4 6h16v15H4z M4 10h16 M8 3v5 M16 3v5 M8 14h3 M8 17h6"/>',
 "cart": '<path d="M3 4h2l2.5 11h11L21 7H7 M9 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm9 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>',
 "brand": '<path d="M4 7l8-4 8 4v10l-8 4-8-4z M4 7l8 4 8-4 M12 11v10"/>',
 "code": '<path d="M8 8l-4 4 4 4 M16 8l4 4-4 4 M13.5 5l-3 14"/>',
 "ship": '<path d="M3 15l2 5h14l2-5z M5 15V9h14v6 M12 9V4 M9 6h6"/>',
}
def icon(k):
    return f'<svg class="us-ic" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</g></svg>'

starter = US["tiers"][0]["p"]
kit_rows = [("Articles of organization", "Filed"), ("Operating agreement", "Ready"), ("EIN confirmation letter", "Issued"),
            ("Registered agent", "Active"), ("US business address", "Active"), ("Bank & payment applications", "In review")]
kit = "".join(f'<li><span class="us-kit-ck">{CHECK}</span>{T("span", a)}{T("em", b, "pend" if b == "In review" else "")}</li>' for a, b in kit_rows)

hero = f'''<section class="page-hero night us-hero">
  <div class="wrap">
    <div>
      <p class="eyebrow"><span class="ltr">US</span> · {T("span", "United States")}</p>
      {T("h1", "Start your US company from anywhere in the world")}
      {T("p", "We form your LLC, apply for your EIN and set up the address and paperwork you need to sell to US customers. Fully remote, with a team you can reach on WhatsApp.", "lede")}
      <div class="us-cta">
        <a class="btn solid us-red" href="#pricing"><span class="dot"></span>{T("span", "See US packages")}</a>
        <a class="btn ghost us-ghost" href="contact.html">{T("span", "Free consultation")}</a>
      </div>
      <ul class="us-trust">
        <li>{CHECK}{T("span", "No US visit needed")}</li>
        <li>{CHECK}{T("span", "100% foreign ownership")}</li>
        <li>{CHECK}{T("span", "State fee included")}</li>
        <li>{CHECK}{T("span", "EIN for non-residents")}</li>
      </ul>
    </div>
    <div class="us-kit" aria-hidden="true">
      <div class="us-kit-top"><span class="us-kit-flag ltr">US<i>.</i></span><div>{T("b", "Your US company kit")}{T("small", "Wyoming LLC")}</div>
        <span class="us-kit-price">{T("span", "from")} {money(starter)}</span></div>
      <ul>{kit}</ul>
    </div>
  </div>
</section>
<p class="us-disc wrap"><span{tk("Wizz Smart Services is a private company. We are not a government agency or a law firm.")}>Wizz Smart Services is a private company. We are not a government agency or a law firm.</span></p>'''

feats = [("llc", "LLC formation", "We file your LLC with the state and prepare your articles of organization and operating agreement."),
         ("ein", "EIN (US tax ID)", "We apply to the IRS for your Employer Identification Number. You don't need an SSN or ITIN."),
         ("agent", "Registered agent", "A registered agent in your state receives official mail and legal notices for your company."),
         ("addr", "US business address", "A US mailing address for your company, with scans of the letters you receive."),
         ("bank", "Bank & payment applications", "We prepare and submit applications to providers such as Wise, Payoneer and Stripe. Each provider makes its own decision."),
         ("cal", "Yearly compliance", "Form 5472 and pro-forma 1120, the state annual report and reminders, so your company stays in good standing.")]
feat_html = "".join(f'<article class="us-feat">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in feats)

def head(eyebrow, h2, p=None, id_=None):
    return f'<div class="sec-head"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div>{T("p", eyebrow, "eyebrow")}{T("h2", h2)}</div>{T("p", p) if p else "<span></span>"}</div>'

steps = [("Tell us about your business", "Choose a package and send your passport and details through your client account.", "About 15 minutes"),
         ("We verify and file", "We check your identity, then file your LLC with the state.", "1 to 3 business days after checks"),
         ("We get your EIN", "We apply to the IRS for your company's tax ID.", "Usually 2 to 6 weeks for non-residents"),
         ("Address, bank and payments", "Your US address goes live and we prepare your bank and payment applications.", "Depends on each provider"),
         ("Launch and grow", "Start selling, and we remind you of every yearly filing.", "Ongoing")]
steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}<span class="us-time">{T("span", t)}</span></li>' for h, p, t in steps)

def ent(name, lede, pts, note=None):
    lis = "".join(f"<li>{CHECK}{T('span', x)}</li>" for x in pts)
    return f'<article class="us-ent">{T("h3", name)}{T("p", lede)}<ul>{lis}</ul>{T("p", note, "us-ent-note") if note else ""}</article>'
ents = ent("LLC", "Simple to run and the usual choice for e-commerce sellers, agencies and online services.",
           ["Can be 100% owned by non-residents, alone or with partners", "Protects your personal assets from business debts", "Light yearly paperwork", "Doesn't issue shares to investors"]) + \
       ent("C-Corp", "For startups that plan to raise money from investors.",
           ["Issues shares and stock options", "Preferred by most venture investors, usually in Delaware", "More formal rules and yearly filings"], "Available on request, with a written quote")
states = "".join(f'<div class="us-state">{T("b", s)}{T("p", d)}</div>' for s, d in [
    ("Wyoming", "Our default. Low yearly costs and strong privacy for owners."),
    ("New Mexico", "No annual report, so the lowest running cost."),
    ("Delaware", "Best known with investors. Higher yearly state tax.")])

# comparison table built from the catalog: each tier adds to the one before
rows, owner = [], []
for i, t in enumerate(US["tiers"]):
    for item in t["i"]:
        rows.append((item, i))
def cell(have):
    return f'<td class="{"y" if have else "n"}">' + (f'{CHECK}<span class="sr"{tk("Included")}>Included</span>' if have else f'<span aria-hidden="true">–</span><span class="sr"{tk("Not included")}>Not included</span>') + "</td>"
thead = "".join(f'<th scope="col">{T("span", t["n"])}<small>{money(t["p"])}</small></th>' for t in US["tiers"])
tbody = "".join(f'<tr><th scope="row"{tk(item)}>{esc(item)}</th>' + "".join(cell(j >= i) for j in range(len(US["tiers"]))) + "</tr>" for item, i in rows)
notes = "".join(f'<p class="pk-note"{tk(n, money_text)}>{money_text(n)}</p>' for n in US["notes"])

who = [("cart", "Amazon and e-commerce sellers", "Sell on Amazon.com, Walmart or TikTok Shop US with a US company and EIN. We also help with seller account applications."),
       ("brand", "Shopify and private-label brands", "Build your own brand with a US entity, address and payment applications behind it."),
       ("code", "Agencies, SaaS and freelancers", "Invoice US clients from a US company and apply for USD payment accounts."),
       ("ship", "Traders and importers", "Trade with US suppliers and buyers, with logistics support from our network.")]
who_html = "".join(f'<article class="us-who">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in who)

stories = ""
if TESTIMONIALS:
    cards = ""
    for s in TESTIMONIALS:
        if s.get("quote_ar"): AR_SRC.setdefault(s["quote"], s["quote_ar"])
        q = T("blockquote", s["quote"]) if s["quote"] in AR_SRC else f"<blockquote>{esc(s['quote'])}</blockquote>"
        cards += f'<figure class="us-story"><img src="{esc(s["photo"])}" alt="{esc(s["name"])}" width="64" height="64" loading="lazy">{q}<figcaption><b>{esc(s["name"])}</b><span>{esc(s["role"])}</span></figcaption></figure>'
    stories = f'<section class="block alt"><div class="wrap">{head("Client stories", "Founders who started with Wizz")}<div class="us-stories">{cards}</div></div></section>'

faqs = [("Do I need to be a US citizen or live in the US?", "No. Non-residents can own 100% of a US LLC. You don't need to travel to the US, and you don't need an SSN or ITIN to get an EIN."),
        ("What do you need from me?", "A copy of your passport, your full residential address, your national ID number, a few company name choices and a short description of your business."),
        ("How long does it take?", "The LLC is usually filed within 1 to 3 business days after our checks. The EIN usually takes 2 to 6 weeks for non-residents. Bank and payment accounts depend on each provider."),
        ("Will I get a US bank account and Stripe?", "We prepare and submit complete applications to suitable providers such as Wise, Payoneer and Stripe. Approval is always the provider's decision, based on their own checks, so no one can guarantee it."),
        ("Does a US company give me a visa or residency?", "No. Forming a company does not give you a visa, residency or the right to work in the US. Immigration is a separate process."),
        ("What taxes will I pay?", "It depends on your activity, where you live and where your customers are. Every foreign-owned LLC must file Form 5472 each year, which our Complete package covers. For tax advice we refer you to a qualified tax professional."),
        ("What happens after the first year?", "You renew the registered agent and file the state's annual report, and the federal filings continue each year. We send reminders and can handle the renewal for you.")]
faq_html = "".join(f"<details><summary{tk(q)}>{esc(q)}</summary>{T('p', a)}</details>" for q, a in faqs)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False)

us_body = hero + f'''
<section class="block">
  <div class="wrap">
    {head("What you get", "Start right. Stay compliant.", "Everything a non-US founder needs to open and run a US company, in one place.")}
    <div class="us-feats">{feat_html}</div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("How it works", "From first message to a working US company", "Times are typical. Government offices and providers set their own pace.")}
    <ol class="steps us-steps">{steps_html}</ol>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("Which structure and state?", "Most non-US founders choose an LLC", "We help you pick in your free consultation. For tax questions specific to your country, we refer you to a qualified tax professional.")}
    <div class="us-ents">{ents}</div>
    <div class="us-states">{states}</div>
  </div>
</section>
<section class="block alt" id="pricing">
  <div class="wrap">
    {head("Pricing", "US packages", "One price, with the state filing fee included. Pay in your own currency.")}
    <div class="pk-curbar"><label for="pkCur"{tk("Prices in")}>Prices in</label><select id="pkCur"><option value="USD">USD · US dollar</option></select><span class="pk-curnote" id="pkCurNote">Set in US dollars. Change the currency if you prefer.</span></div>
    <div class="pk-grid">{"".join(tier_html(US, t) for t in US["tiers"])}</div>
    {notes}
    <div class="pk-msg" id="pkMsg" role="status" hidden></div>
    {T("h3", "Compare packages", "us-cmp-h")}
    <div class="us-cmp-wrap"><table class="us-cmp"><thead><tr><th scope="col"{tk("Feature")}>Feature</th>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("Who we help", "Built for founders selling to the US")}
    <div class="us-whos">{who_html}</div>
  </div>
</section>
{stories}
<section class="block alt" id="faq">
  <div class="wrap faq-layout">
    <div>{T("p", "Questions", "eyebrow")}{T("h2", "US company questions")}</div>
    <div class="faq">{faq_html}</div>
  </div>
</section>
<section class="us-final night">
  <div class="wrap">
    {T("h2", "Ready to start your US company?")}
    {T("p", "Pick a package today, or talk to us first. We reply on WhatsApp and email.")}
    <div class="us-cta">
      <a class="btn solid us-red" href="#pricing"><span class="dot"></span>{T("span", "Start my US company")}</a>
      <a class="btn ghost us-ghost" href="https://wa.me/601124477685?text=Hi%20Wizz%2C%20I%27d%20like%20to%20start%20a%20US%20company." target="_blank" rel="noopener">{T("span", "Chat on WhatsApp")}</a>
    </div>
  </div>
</section>'''

page("usa.html", "US Company Formation for Non-Residents | LLC + EIN | Wizz Smart Services",
     f"Form a US LLC from anywhere: state fee, EIN for non-residents and registered agent included, from ${starter}. Fully remote, with WhatsApp support.",
     us_body, extra_head=f'<script type="application/ld+json">{faq_ld}</script>', scripts=ar_script() + PK_JS)

US_CSS = r'''
/* ----- US landing page */
.us-hero .wrap{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr)}
.us-hero .eyebrow .ltr{font-family:var(--mono)}
.us-cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.us-red{background:var(--red)!important;border-color:var(--red)!important;color:#fff!important}
.us-red .dot{background:#fff}
.night .us-ghost{color:var(--night-fg);border-color:var(--night-line)}
.night .us-ghost:hover{border-color:var(--night-fg)}
.us-trust{list-style:none;padding:0;margin:26px 0 0;display:grid;grid-template-columns:repeat(2,minmax(0,max-content));gap:10px 26px;color:var(--night-fg);font-size:14.5px}
.us-trust li{display:flex;gap:8px;align-items:center}
.us-trust svg,.us-ent li svg{width:18px;height:18px;flex:none;color:var(--red)}
.us-kit{background:var(--surface);color:var(--ink);border-radius:16px;padding:22px;box-shadow:0 30px 60px -30px rgba(0,0,0,.55);border:1px solid var(--line)}
.us-kit-top{display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:1px solid var(--line)}
.us-kit-top b{display:block;font-size:15px}.us-kit-top small{color:var(--muted);font-size:12.5px}
.us-kit-flag{font:800 20px var(--mono);background:var(--ink);color:var(--on-ink);border-radius:10px;padding:8px 10px}
.us-kit-flag i{color:var(--red);font-style:normal}
.us-kit-price{margin-inline-start:auto;font-size:12.5px;color:var(--muted);text-align:end}
.us-kit-price .m{display:block;font:800 20px var(--body);color:var(--ink)}
.us-kit ul{list-style:none;margin:0;padding:6px 0 0}
.us-kit li{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px dashed var(--line);font-size:14px}
.us-kit li:last-child{border-bottom:0}
.us-kit li em{margin-inline-start:auto;font:600 11.5px var(--mono);font-style:normal;text-transform:uppercase;letter-spacing:.04em;color:#178a4c;background:rgba(23,138,76,.1);padding:3px 8px;border-radius:99px;white-space:nowrap}
.us-kit li em.pend{color:#a86a00;background:rgba(214,140,0,.13)}
.us-kit-ck{width:22px;height:22px;border-radius:50%;background:var(--ink);color:var(--on-ink);display:grid;place-items:center;flex:none}
.us-kit-ck svg{width:14px;height:14px}
.us-disc{font-size:12.5px;color:var(--muted);padding-block:14px;margin-block:0}
.us-feats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.us-feat,.us-who,.us-ent{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:26px 24px}
.us-feat h3,.us-who h3{font-size:18px;margin:16px 0 8px}
.us-feat p,.us-who p{color:var(--muted);font-size:15px;margin:0}
.us-ic{width:42px;height:42px;padding:9px;border-radius:12px;background:var(--bg);border:1px solid var(--line);color:var(--ink)}
.us-steps{grid-template-columns:repeat(5,minmax(0,1fr))}
.us-steps p{color:var(--muted);font-size:14.5px}
.us-time{display:inline-block;margin-top:10px;font:600 12px var(--mono);color:var(--red);text-transform:uppercase;letter-spacing:.03em}
.us-ents{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.us-ent h3{font:800 26px var(--mono);margin:0 0 8px}
.us-ent>p{color:var(--muted);margin:0 0 14px}
.us-ents-txt .us-ent h3{font:800 21px var(--body)}
.us-ent ul{list-style:none;padding:0;margin:0;display:grid;gap:9px;font-size:15px}
.us-ent li{display:flex;gap:9px;align-items:flex-start}.us-ent li svg{margin-top:3px}
.us-ent-note{margin:16px 0 0!important;font-size:13px;font-weight:600;color:var(--ink)!important}
.us-states{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;margin-top:18px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface)}
.us-state{padding:18px 22px;border-inline-start:1px solid var(--line)}
.us-state:first-child{border-inline-start:0}
.us-state b{font-size:16px}.us-state p{margin:4px 0 0;color:var(--muted);font-size:14px}
.us-cmp-h{font-size:22px;margin:56px 0 16px}
.us-cmp-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--surface)}
.us-cmp{width:100%;border-collapse:collapse;font-size:14.5px;min-width:560px}
.us-cmp th,.us-cmp td{padding:13px 16px;border-bottom:1px solid var(--line);text-align:center}
.us-cmp tbody tr:last-child>*{border-bottom:0}
.us-cmp th[scope=row],.us-cmp thead th:first-child{text-align:start;font-weight:500}
.us-cmp thead th{font-weight:700;vertical-align:bottom}
.us-cmp thead small{display:block;font-weight:500;color:var(--muted);font-size:13px}
.us-cmp td.y svg{width:20px;height:20px;color:#178a4c;vertical-align:middle}
.us-cmp td.n{color:var(--muted)}
.us-cmp td,.us-cmp th{position:relative}
.us-cmp .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.us-whos{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
.us-stories{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.us-story{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:24px;display:flex;flex-direction:column;gap:14px}
.us-story img{width:64px;height:64px;border-radius:50%;object-fit:cover}
.us-story blockquote{margin:0;font-size:15.5px}
.us-story figcaption span{display:block;color:var(--muted);font-size:13.5px}
.us-final{padding-block:clamp(56px,8vw,96px);text-align:center;background:var(--night);color:var(--night-fg)}
.us-final h2{font-size:clamp(28px,4vw,46px);font-weight:850;margin:0 0 12px;color:var(--night-fg)}
.us-final p{color:var(--night-muted);margin:0}
.us-final .us-cta{justify-content:center}
.ccard .clinks{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:auto;padding-top:16px}
.ccard .clink{display:inline-flex;gap:6px;margin-top:0;font-weight:600;color:var(--ink);text-decoration:none;border-bottom:1.5px solid var(--red)}
.pk-guide{display:inline-flex;gap:6px;margin:6px 0 18px;font-weight:600;color:var(--ink);text-decoration:none;border-bottom:1.5px solid var(--red)}
@media (max-width:1000px){.us-steps{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:34px}.us-whos{grid-template-columns:repeat(2,minmax(0,1fr))}.us-feats,.us-stories{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:860px){.us-hero .wrap{grid-template-columns:1fr}.us-kit{max-width:460px}}
@media (max-width:640px){.us-kit{padding:18px}.us-kit-top{flex-wrap:wrap}.us-kit-price{flex-basis:100%;text-align:start;margin-inline-start:0;display:flex;gap:8px;align-items:baseline}.us-kit-price .m{display:inline}.us-feats,.us-whos,.us-ents,.us-stories,.us-states,.us-steps{grid-template-columns:1fr}.us-state{border-inline-start:0;border-top:1px solid var(--line)}.us-state:first-child{border-top:0}.us-trust{grid-template-columns:1fr}.us-cmp{min-width:0;font-size:13px}.us-cmp th,.us-cmp td{padding:10px 6px}.us-cmp th[scope=row]{padding-inline-start:12px}.us-cmp thead small{font-size:11px}}
'''
