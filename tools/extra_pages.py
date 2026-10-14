# MM2H page (mm2h.html) and Amazon brand services page (amazon-brand.html). Quote-only, no checkout.
# Runs inside build_pkgs.py after saudi_page.py, reusing T, tk, icon, CHECK, head, ent, page, ar_script and the US_CSS styles.
# MM2H: applications go through a licensed MM2H agent partner (not named). Figures checked October 2026 (MOTAC rules); re-check before changing.
# Every string: (English, Arabic, Malay). Malay is written into tools/ms_strings.json for build_ar.py.

XTX = [
 # shared
 ("By quote", "حسب عرض السعر", "Ikut sebut harga"),
 ("Written quote before you pay", "عرض سعر مكتوب قبل الدفع", "Sebut harga bertulis sebelum anda membayar"),
 # ---- MM2H
 ("Malaysia My Second Home", "برنامج ماليزيا وطني الثاني", "Malaysia Rumah Keduaku"),
 ("Live in Malaysia long term with MM2H", "عِش في ماليزيا لفترة طويلة مع برنامج MM2H", "Tinggal di Malaysia untuk jangka panjang dengan MM2H"),
 ("Malaysia My Second Home (MM2H) is a long-stay visa programme run by Malaysia's Ministry of Tourism. We guide you from the first eligibility check to your pass, and our licensed MM2H agent partner submits your application.",
  "برنامج ماليزيا وطني الثاني (MM2H) برنامج تأشيرة إقامة طويلة تديره وزارة السياحة الماليزية. نرافقك من أول تقييم للأهلية حتى حصولك على التصريح، ويتولى وكيل MM2H مرخّص من شركائنا تقديم طلبك.",
  "Malaysia Rumah Keduaku (MM2H) ialah program visa tinggal jangka panjang yang dikendalikan oleh Kementerian Pelancongan Malaysia. Kami membimbing anda dari semakan kelayakan pertama hingga pas anda, dan rakan ejen MM2H berlesen kami menghantar permohonan anda."),
 ("See the tiers", "عرض الفئات", "Lihat peringkat"),
 ("Eligibility check before you pay", "تقييم الأهلية قبل الدفع", "Semakan kelayakan sebelum anda membayar"),
 ("Application through a licensed MM2H agent", "تقديم الطلب عبر وكيل MM2H مرخّص", "Permohonan melalui ejen MM2H berlesen"),
 ("Help with the deposit, bank and property steps", "مساعدة في خطوات الوديعة والبنك والعقار", "Bantuan untuk langkah deposit, bank dan hartanah"),
 ("Your MM2H file", "ملف MM2H الخاص بك", "Fail MM2H anda"),
 ("Silver, Gold or Platinum", "الفضية أو الذهبية أو البلاتينية", "Silver, Gold atau Platinum"),
 ("Eligibility check", "تقييم الأهلية", "Semakan kelayakan"),
 ("Document checklist", "قائمة المستندات", "Senarai semak dokumen"),
 ("Application", "الطلب", "Permohonan"),
 ("Fixed deposit", "الوديعة الثابتة", "Deposit tetap"),
 ("MM2H pass", "تصريح MM2H", "Pas MM2H"),
 ("Done", "تم", "Selesai"),
 ("Ready", "جاهز", "Sedia"),
 ("Submitted", "قُدّم", "Dihantar"),
 ("Placed", "أودعت", "Diletakkan"),
 ("Ministry decides", "الوزارة تقرر", "Kementerian memutuskan"),
 ("MM2H is a visa programme run by the Malaysian government. Forming a company does not give you a visa.",
  "MM2H برنامج تأشيرة تديره الحكومة الماليزية. وتأسيس شركة لا يمنحك تأشيرة بحد ذاته.",
  "MM2H ialah program visa yang dikendalikan oleh kerajaan Malaysia. Menubuhkan syarikat tidak memberi anda visa."),
 ("The tiers", "الفئات", "Peringkat"),
 ("Silver, Gold and Platinum", "الفضية والذهبية والبلاتينية", "Silver, Gold dan Platinum"),
 ("Set by the Ministry of Tourism, Arts and Culture (MOTAC), as of October 2026. The rules can change, so we confirm them with you before you apply.",
  "تحددها وزارة السياحة والفنون والثقافة (MOTAC)، كما في أكتوبر 2026. قد تتغير الشروط، لذا نتأكد منها معك قبل التقديم.",
  "Ditetapkan oleh Kementerian Pelancongan, Seni dan Budaya (MOTAC), setakat Oktober 2026. Peraturan boleh berubah, jadi kami mengesahkannya bersama anda sebelum anda memohon."),
 ("Requirement", "الشرط", "Syarat"),
 ("Silver", "الفضية", "Silver"), ("Gold", "الذهبية", "Gold"), ("Platinum", "البلاتينية", "Platinum"),
 ("Minimum age", "الحد الأدنى للعمر", "Umur minimum"),
 ("Fixed deposit in a Malaysian bank", "وديعة ثابتة في بنك ماليزي", "Deposit tetap di bank Malaysia"),
 ("Property to buy (minimum)", "العقار المطلوب شراؤه (حد أدنى)", "Hartanah untuk dibeli (minimum)"),
 ("Pass length", "مدة التصريح", "Tempoh pas"),
 ("Minimum stay", "الحد الأدنى للإقامة", "Tempoh tinggal minimum"),
 ("Work or run a business", "العمل أو إدارة نشاط تجاري", "Bekerja atau menjalankan perniagaan"),
 ("5 years", "5 سنوات", "5 tahun"), ("15 years", "15 سنة", "15 tahun"), ("20 years", "20 سنة", "20 tahun"),
 ("90 days a year", "90 يوماً في السنة", "90 hari setahun"),
 ("No", "لا", "Tidak"), ("Yes, with approval", "نعم، بموافقة", "Ya, dengan kelulusan"),
 ("Up to 50% of the deposit can be withdrawn after approval for approved purposes, such as buying a home, education or healthcare. The property is bought within 12 months of the pass and is usually held for at least 10 years. A Special Economic Zone (SEZ) route with lower amounts also exists; ask us whether it fits you.",
  "يمكن سحب ما يصل إلى 50% من الوديعة بعد الموافقة لأغراض معتمدة، مثل شراء منزل أو التعليم أو العلاج. ويُشترى العقار خلال 12 شهراً من صدور التصريح، ويُحتفظ به عادةً 10 سنوات على الأقل. ويوجد أيضاً مسار المناطق الاقتصادية الخاصة (SEZ) بمبالغ أقل؛ اسألنا إن كان يناسبك.",
  "Sehingga 50% daripada deposit boleh dikeluarkan selepas kelulusan untuk tujuan yang diluluskan, seperti membeli rumah, pendidikan atau penjagaan kesihatan. Hartanah dibeli dalam tempoh 12 bulan selepas pas dan biasanya dipegang sekurang-kurangnya 10 tahun. Laluan Zon Ekonomi Khas (SEZ) dengan jumlah lebih rendah juga wujud; tanya kami sama ada ia sesuai untuk anda."),
 ("How it works", "كيف تتم العملية", "Cara ia berfungsi"),
 ("From first question to your MM2H pass", "من أول سؤال حتى تصريح MM2H", "Dari soalan pertama hingga pas MM2H anda"),
 ("Each application is decided by MOTAC and the Immigration Department. We keep you updated at every step.",
  "تقرر وزارة السياحة ودائرة الهجرة في كل طلب. ونطلعك على كل خطوة.",
  "Setiap permohonan diputuskan oleh MOTAC dan Jabatan Imigresen. Kami memaklumkan anda pada setiap langkah."),
 ("Tell us your age, nationality, family and budget. We check which tier fits, and whether MM2H is right for you.",
  "أخبرنا بعمرك وجنسيتك وعائلتك وميزانيتك. نحدد الفئة المناسبة، وما إذا كان البرنامج مناسباً لك أصلاً.",
  "Beritahu kami umur, kewarganegaraan, keluarga dan bajet anda. Kami menyemak peringkat yang sesuai, dan sama ada MM2H sesuai untuk anda."),
 ("Free consultation", "استشارة مجانية", "Rundingan percuma"),
 ("Documents", "المستندات", "Dokumen"),
 ("We give you the checklist and review your passport, family documents and financial statements before anything is submitted.",
  "نعطيك قائمة المستندات ونراجع جواز سفرك ومستندات عائلتك وكشوفك المالية قبل تقديم أي شيء.",
  "Kami memberi senarai semak dan menyemak pasport, dokumen keluarga dan penyata kewangan anda sebelum apa-apa dihantar."),
 ("Application through a licensed agent", "تقديم الطلب عبر وكيل مرخّص", "Permohonan melalui ejen berlesen"),
 ("Our licensed MM2H agent partner submits your application to MOTAC and follows it until a decision is made.",
  "يقدّم وكيل MM2H المرخّص من شركائنا طلبك إلى وزارة السياحة ويتابعه حتى صدور القرار.",
  "Rakan ejen MM2H berlesen kami menghantar permohonan anda kepada MOTAC dan menjejakinya sehingga keputusan dibuat."),
 ("Deposit and medical check", "الوديعة والفحص الطبي", "Deposit dan pemeriksaan perubatan"),
 ("After approval, you place the fixed deposit with a Malaysian bank and complete the medical check.",
  "بعد الموافقة، تودع الوديعة الثابتة في بنك ماليزي وتُجري الفحص الطبي.",
  "Selepas kelulusan, anda meletakkan deposit tetap di bank Malaysia dan melengkapkan pemeriksaan perubatan."),
 ("Pass and property", "التصريح والعقار", "Pas dan hartanah"),
 ("Your pass is endorsed in your passport, and you buy your property within the required time.",
  "يُختم التصريح في جواز سفرك، وتشتري العقار خلال المدة المطلوبة.",
  "Pas anda diendorskan dalam pasport, dan anda membeli hartanah dalam tempoh yang ditetapkan."),
 ("What MM2H gives you", "ما يمنحك إياه البرنامج", "Apa yang MM2H berikan"),
 ("A legal, renewable way to live in Malaysia with your family.", "طريقة نظامية وقابلة للتجديد للعيش في ماليزيا مع عائلتك.", "Cara sah dan boleh diperbaharui untuk tinggal di Malaysia bersama keluarga anda."),
 ("A long-stay pass of 5, 15 or 20 years, by tier", "تصريح إقامة طويلة لمدة 5 أو 15 أو 20 سنة حسب الفئة", "Pas tinggal jangka panjang 5, 15 atau 20 tahun, mengikut peringkat"),
 ("Renewable when you meet the conditions", "قابل للتجديد عند استيفاء الشروط", "Boleh diperbaharui jika anda memenuhi syarat"),
 ("Spouse, children and parents can usually be included as dependants", "يمكن عادةً إضافة الزوج والأبناء والوالدين كمرافقين", "Pasangan, anak dan ibu bapa biasanya boleh dimasukkan sebagai tanggungan"),
 ("Platinum holders can work or run a business, with approval", "يمكن لحاملي الفئة البلاتينية العمل أو إدارة نشاط تجاري بموافقة", "Pemegang Platinum boleh bekerja atau menjalankan perniagaan, dengan kelulusan"),
 ("What it doesn't do", "ما لا يفعله", "Apa yang ia tidak lakukan"),
 ("Be clear on this before you start.", "من المهم أن يكون هذا واضحاً قبل أن تبدأ.", "Pastikan perkara ini jelas sebelum anda bermula."),
 ("It isn't citizenship or permanent residency", "ليس جنسية ولا إقامة دائمة", "Ia bukan kewarganegaraan atau pemastautin tetap"),
 ("Silver and Gold holders can't work in Malaysia", "لا يحق لحاملي الفئتين الفضية والذهبية العمل في ماليزيا", "Pemegang Silver dan Gold tidak boleh bekerja di Malaysia"),
 ("No one can guarantee approval: MOTAC and Immigration decide every application", "لا أحد يستطيع ضمان الموافقة: وزارة السياحة ودائرة الهجرة تقرران في كل طلب", "Tiada siapa boleh menjamin kelulusan: MOTAC dan Imigresen memutuskan setiap permohonan"),
 ("Amounts and rules can change; we confirm them before you apply", "قد تتغير المبالغ والشروط؛ ونتأكد منها قبل التقديم", "Jumlah dan peraturan boleh berubah; kami mengesahkannya sebelum anda memohon"),
 ("Who we help", "من نساعد", "Siapa yang kami bantu"),
 ("Built for families and investors moving to Malaysia", "مصمم للعائلات والمستثمرين الذين ينتقلون إلى ماليزيا", "Dibina untuk keluarga dan pelabur yang berpindah ke Malaysia"),
 ("Families relocating", "العائلات المنتقلة", "Keluarga yang berpindah"),
 ("Parents who want a stable, long-term base in Malaysia for the whole family.", "آباء وأمهات يريدون قاعدة مستقرة وطويلة الأمد في ماليزيا للعائلة كلها.", "Ibu bapa yang mahukan pangkalan jangka panjang yang stabil di Malaysia untuk seluruh keluarga."),
 ("Retirees", "المتقاعدون", "Pesara"),
 ("People planning to spend part of each year in Malaysia after they stop working.", "من يخططون لقضاء جزء من كل سنة في ماليزيا بعد التقاعد.", "Mereka yang merancang untuk menghabiskan sebahagian setiap tahun di Malaysia selepas bersara."),
 ("Investors", "المستثمرون", "Pelabur"),
 ("Platinum applicants who want to work or run a business in Malaysia, with approval.", "المتقدمون للفئة البلاتينية الذين يريدون العمل أو إدارة نشاط تجاري في ماليزيا بموافقة.", "Pemohon Platinum yang mahu bekerja atau menjalankan perniagaan di Malaysia, dengan kelulusan."),
 ("Business owners", "أصحاب الأعمال", "Pemilik perniagaan"),
 ("Founders with a Malaysian company who want long-stay status for their family. The company and the visa are separate applications.",
  "مؤسسون لديهم شركة ماليزية ويريدون إقامة طويلة لعائلاتهم. الشركة والتأشيرة طلبان منفصلان.",
  "Pengasas yang mempunyai syarikat Malaysia dan mahukan status tinggal jangka panjang untuk keluarga mereka. Syarikat dan visa ialah permohonan berasingan."),
 ("Questions", "أسئلة", "Soalan"),
 ("MM2H questions", "أسئلة عن برنامج MM2H", "Soalan MM2H"),
 ("Can I apply for MM2H myself?", "هل يمكنني التقديم على البرنامج بنفسي؟", "Bolehkah saya memohon MM2H sendiri?"),
 ("No. Applications must go through a licensed MM2H agent. We work with a licensed agent partner and manage the process with you.",
  "لا. يجب تقديم الطلبات عبر وكيل MM2H مرخّص. نعمل مع وكيل مرخّص من شركائنا وندير العملية معك.",
  "Tidak. Permohonan mesti melalui ejen MM2H berlesen. Kami bekerjasama dengan rakan ejen berlesen dan menguruskan proses bersama anda."),
 ("Do I have to buy property?", "هل يجب أن أشتري عقاراً؟", "Adakah saya perlu membeli hartanah?"),
 ("Yes. Each tier sets a minimum property value: RM 600,000 for Silver, RM 1,000,000 for Gold and RM 2,000,000 for Platinum. The purchase is usually due within 12 months of your pass.",
  "نعم. لكل فئة حد أدنى لقيمة العقار: 600,000 رينغيت للفضية، و1,000,000 رينغيت للذهبية، و2,000,000 رينغيت للبلاتينية. ويكون الشراء عادةً خلال 12 شهراً من صدور التصريح.",
  "Ya. Setiap peringkat menetapkan nilai hartanah minimum: RM 600,000 untuk Silver, RM 1,000,000 untuk Gold dan RM 2,000,000 untuk Platinum. Pembelian biasanya perlu dibuat dalam tempoh 12 bulan selepas pas anda."),
 ("Can I work in Malaysia with MM2H?", "هل يمكنني العمل في ماليزيا بهذا التصريح؟", "Bolehkah saya bekerja di Malaysia dengan MM2H?"),
 ("Only the Platinum tier allows work or running a business, with approval. Silver and Gold holders can't work.",
  "الفئة البلاتينية وحدها تسمح بالعمل أو إدارة نشاط تجاري، بموافقة. ولا يحق لحاملي الفئتين الفضية والذهبية العمل.",
  "Hanya peringkat Platinum membenarkan kerja atau menjalankan perniagaan, dengan kelulusan. Pemegang Silver dan Gold tidak boleh bekerja."),
 ("Can my family come with me?", "هل يمكن لعائلتي مرافقتي؟", "Bolehkah keluarga saya ikut serta?"),
 ("Usually yes. Your spouse, children and parents can be included as dependants. We check the rules for your family before you apply.",
  "عادةً نعم. يمكن إضافة الزوج والأبناء والوالدين كمرافقين. ونتحقق من الشروط الخاصة بعائلتك قبل التقديم.",
  "Biasanya ya. Pasangan, anak dan ibu bapa anda boleh dimasukkan sebagai tanggungan. Kami menyemak peraturan untuk keluarga anda sebelum anda memohon."),
 ("Is MM2H permanent residency?", "هل البرنامج إقامة دائمة؟", "Adakah MM2H pemastautin tetap?"),
 ("No. It's a renewable long-stay pass. It doesn't give citizenship or permanent residency.", "لا. هو تصريح إقامة طويلة قابل للتجديد، ولا يمنح الجنسية أو الإقامة الدائمة.", "Tidak. Ia pas tinggal jangka panjang yang boleh diperbaharui. Ia tidak memberi kewarganegaraan atau pemastautin tetap."),
 ("How much do you charge?", "كم تبلغ رسومكم؟", "Berapakah caj anda?"),
 ("It depends on the tier and your family. After a free consultation we send a written quote, so you know every cost before you start.",
  "تعتمد على الفئة وعلى عائلتك. بعد استشارة مجانية نرسل لك عرض سعر مكتوباً، لتعرف كل التكاليف قبل أن تبدأ.",
  "Ia bergantung pada peringkat dan keluarga anda. Selepas rundingan percuma kami menghantar sebut harga bertulis, supaya anda tahu setiap kos sebelum bermula."),
 ("Thinking about MM2H?", "تفكر في برنامج MM2H؟", "Sedang mempertimbangkan MM2H?"),
 ("Tell us your age, nationality and family, and we'll tell you which tier fits and what it costs.", "أخبرنا بعمرك وجنسيتك وعائلتك، وسنخبرك بالفئة المناسبة وتكلفتها.", "Beritahu kami umur, kewarganegaraan dan keluarga anda, dan kami akan memberitahu peringkat yang sesuai dan kosnya."),
 ("Talk to us on WhatsApp", "تحدث معنا عبر واتساب", "Hubungi kami di WhatsApp"),
 ("Chat on WhatsApp", "تواصل عبر واتساب", "Bual di WhatsApp"),
 # ---- Amazon
 ("Amazon brand services", "خدمات العلامات التجارية على أمازون", "Perkhidmatan jenama Amazon"),
 ("Protect and grow your brand on Amazon", "احمِ علامتك التجارية ونمِّها على أمازون", "Lindungi dan kembangkan jenama anda di Amazon"),
 ("We file your trademark, enrol your brand in Amazon Brand Registry and prepare you for Amazon Vendor Central, so your listings are protected and ready to grow.",
  "نسجّل علامتك التجارية، ونُدرج علامتك في برنامج Amazon Brand Registry، ونجهّزك لمنصة Amazon Vendor Central، لتكون منتجاتك محمية وجاهزة للنمو.",
  "Kami memfailkan tanda dagangan anda, mendaftarkan jenama anda dalam Amazon Brand Registry dan menyediakan anda untuk Amazon Vendor Central, supaya senarai produk anda dilindungi dan sedia untuk berkembang."),
 ("See our services", "عرض خدماتنا", "Lihat perkhidmatan kami"),
 ("Trademark filing for your brand", "تسجيل العلامة التجارية لعلامتك", "Pemfailan tanda dagangan untuk jenama anda"),
 ("Brand Registry enrolment", "التسجيل في Brand Registry", "Pendaftaran Brand Registry"),
 ("Vendor Central readiness", "الجاهزية لمنصة Vendor Central", "Persediaan Vendor Central"),
 ("Your Amazon brand file", "ملف علامتك على أمازون", "Fail jenama Amazon anda"),
 ("Own private brand", "علامة خاصة بك", "Jenama persendirian sendiri"),
 ("Trademark application", "طلب العلامة التجارية", "Permohonan tanda dagangan"),
 ("Filed", "قُدّم", "Difailkan"),
 ("Brand Registry application", "طلب Brand Registry", "Permohonan Brand Registry"),
 ("Product and packaging photos", "صور المنتج والتغليف", "Gambar produk dan pembungkusan"),
 ("Checked", "تمت المراجعة", "Disemak"),
 ("Vendor Central", "Vendor Central", "Vendor Central"),
 ("By Amazon's invitation", "بدعوة من أمازون", "Melalui jemputan Amazon"),
 ("Wizz Smart Services is a private company. We are not a government agency or a law firm.", "ويز للخدمات الذكية شركة خاصة، ولسنا جهة حكومية أو مكتب محاماة.", "Wizz Smart Services ialah syarikat swasta. Kami bukan agensi kerajaan atau firma guaman."),
 ("What we do", "ما نقدمه", "Apa yang kami lakukan"),
 ("Three services, one brand file", "ثلاث خدمات، وملف واحد لعلامتك", "Tiga perkhidmatan, satu fail jenama"),
 ("Trademark filing", "تسجيل العلامة التجارية", "Pemfailan tanda dagangan"),
 ("We file your trademark with the right office, for example the USPTO in the US or the UKIPO in the UK. Amazon accepts a pending application, so you don't have to wait for registration to apply.",
  "نقدّم طلب علامتك لدى الجهة المناسبة، مثل USPTO في أمريكا أو UKIPO في بريطانيا. وتقبل أمازون الطلب قيد التسجيل، فلا تحتاج إلى انتظار التسجيل النهائي للتقديم.",
  "Kami memfailkan tanda dagangan anda di pejabat yang betul, contohnya USPTO di AS atau UKIPO di UK. Amazon menerima permohonan yang belum selesai, jadi anda tidak perlu menunggu pendaftaran untuk memohon."),
 ("Amazon Brand Registry", "Amazon Brand Registry", "Amazon Brand Registry"),
 ("We prepare and submit your enrolment: the brand name exactly as on the trademark, your logo, product categories and photos of the brand on your product or packaging.",
  "نجهّز طلب التسجيل ونقدّمه: اسم العلامة كما في سجل العلامة التجارية تماماً، والشعار، وفئات المنتجات، وصور العلامة على المنتج أو التغليف.",
  "Kami menyediakan dan menghantar pendaftaran anda: nama jenama tepat seperti pada tanda dagangan, logo, kategori produk dan gambar jenama pada produk atau pembungkusan anda."),
 ("Amazon Vendor Central", "Amazon Vendor Central", "Amazon Vendor Central"),
 ("Vendor Central is by Amazon's invitation. We help you build the brand, listings and sales record Amazon looks for, and support your onboarding if you're invited.",
  "منصة Vendor Central بدعوة من أمازون. نساعدك في بناء العلامة وصفحات المنتجات وسجل المبيعات الذي تبحث عنه أمازون، وندعمك في الانضمام إذا تلقيت دعوة.",
  "Vendor Central adalah melalui jemputan Amazon. Kami membantu anda membina jenama, senarai produk dan rekod jualan yang Amazon cari, dan menyokong proses penyertaan jika anda dijemput."),
 ("Seller Central or Vendor Central", "Seller Central أم Vendor Central", "Seller Central atau Vendor Central"),
 ("Two ways to sell on Amazon", "طريقتان للبيع على أمازون", "Dua cara menjual di Amazon"),
 ("Seller Central", "Seller Central", "Seller Central"),
 ("You sell to customers as a third-party seller.", "تبيع للعملاء مباشرة كبائع طرف ثالث.", "Anda menjual kepada pelanggan sebagai penjual pihak ketiga."),
 ("You set your own prices", "تحدد أسعارك بنفسك", "Anda menetapkan harga sendiri"),
 ("You keep control of your listings and stock", "تحتفظ بالتحكم في صفحاتك ومخزونك", "Anda mengawal senarai produk dan stok anda"),
 ("Open to any brand that registers", "متاحة لأي علامة تسجّل", "Terbuka kepada mana-mana jenama yang mendaftar"),
 ("Amazon buys your stock wholesale and sells it to customers.", "تشتري أمازون مخزونك بالجملة وتبيعه للعملاء.", "Amazon membeli stok anda secara borong dan menjualnya kepada pelanggan."),
 ("Amazon sets the retail price", "تحدد أمازون سعر البيع", "Amazon menetapkan harga runcit"),
 ("Payment on Amazon's terms, often 30 to 90 days", "الدفع وفق شروط أمازون، غالباً بين 30 و90 يوماً", "Bayaran mengikut terma Amazon, selalunya 30 hingga 90 hari"),
 ("By Amazon's invitation only", "بدعوة من أمازون فقط", "Melalui jemputan Amazon sahaja"),
 ("What you need for Brand Registry", "ما تحتاجه للتسجيل في Brand Registry", "Apa yang anda perlukan untuk Brand Registry"),
 ("Amazon checks these against your trademark record.", "تطابق أمازون هذه البيانات مع سجل علامتك التجارية.", "Amazon menyemak perkara ini dengan rekod tanda dagangan anda."),
 ("A registered or pending trademark (a word mark, or a logo with words)", "علامة تجارية مسجلة أو قيد التسجيل (علامة نصية أو شعار يحتوي على كلمات)", "Tanda dagangan berdaftar atau belum selesai (tanda perkataan, atau logo dengan perkataan)"),
 ("Your brand name exactly as on the trademark", "اسم علامتك كما في سجل العلامة تماماً", "Nama jenama anda tepat seperti pada tanda dagangan"),
 ("Photos of the brand permanently on your product or packaging, not stickers", "صور تُظهر العلامة مطبوعة بشكل دائم على المنتج أو التغليف، وليس ملصقات", "Gambar jenama yang kekal pada produk atau pembungkusan, bukan pelekat"),
 ("Your product categories", "فئات منتجاتك", "Kategori produk anda"),
 ("What we can't promise", "ما لا يمكننا ضمانه", "Apa yang kami tidak boleh janjikan"),
 ("Trademark offices decide every registration", "مكاتب العلامات التجارية تقرر في كل تسجيل", "Pejabat tanda dagangan memutuskan setiap pendaftaran"),
 ("Amazon decides Brand Registry and Vendor Central access", "أمازون تقرر القبول في Brand Registry وVendor Central", "Amazon memutuskan akses Brand Registry dan Vendor Central"),
 ("An invitation to Vendor Central isn't guaranteed", "الدعوة إلى Vendor Central ليست مضمونة", "Jemputan ke Vendor Central tidak dijamin"),
 ("Sales depend on your product and market", "المبيعات تعتمد على منتجك وسوقك", "Jualan bergantung pada produk dan pasaran anda"),
 ("From brand name to protected listings", "من اسم العلامة إلى منتجات محمية", "Dari nama jenama hingga senarai produk yang dilindungi"),
 ("Trademark office and Amazon review times vary. We keep you updated.", "تختلف مدد مراجعة مكاتب العلامات التجارية وأمازون، ونطلعك على كل جديد.", "Tempoh semakan pejabat tanda dagangan dan Amazon berbeza. Kami sentiasa memaklumkan anda."),
 ("Brand check", "مراجعة العلامة", "Semakan jenama"),
 ("Tell us your brand name, products and markets. We check the name and recommend which office to file with.", "أخبرنا باسم علامتك ومنتجاتك وأسواقك. نراجع الاسم ونوصي بالجهة المناسبة للتسجيل.", "Beritahu kami nama jenama, produk dan pasaran anda. Kami menyemak nama itu dan mencadangkan pejabat untuk pemfailan."),
 ("We file your application and send you the filing receipt and number.", "نقدّم طلبك ونرسل لك إيصال التقديم ورقمه.", "Kami memfailkan permohonan anda dan menghantar resit serta nombor pemfailan."),
 ("Brand Registry", "Brand Registry", "Brand Registry"),
 ("With your trademark filed, we submit your Brand Registry enrolment and follow Amazon's verification.", "بعد تقديم علامتك، نقدّم طلب التسجيل في Brand Registry ونتابع تحقق أمازون.", "Selepas tanda dagangan difailkan, kami menghantar pendaftaran Brand Registry dan menjejaki pengesahan Amazon."),
 ("Grow and Vendor Central", "النمو وVendor Central", "Berkembang dan Vendor Central"),
 ("We help you use the brand tools, and get ready in case Amazon invites you to Vendor Central.", "نساعدك في استخدام أدوات العلامة، ونجهّزك في حال دعتك أمازون إلى Vendor Central.", "Kami membantu anda menggunakan alat jenama, dan bersedia sekiranya Amazon menjemput anda ke Vendor Central."),
 ("Built for brand owners selling on Amazon", "مصمم لأصحاب العلامات الذين يبيعون على أمازون", "Dibina untuk pemilik jenama yang menjual di Amazon"),
 ("Private-label brands", "العلامات الخاصة", "Jenama label persendirian"),
 ("Brands that make products under their own name and want them protected.", "علامات تصنع منتجات باسمها وتريد حمايتها.", "Jenama yang menghasilkan produk atas nama sendiri dan mahu ia dilindungi."),
 ("Amazon sellers", "البائعون على أمازون", "Penjual Amazon"),
 ("Sellers who want more control over their product listings.", "بائعون يريدون تحكماً أكبر في صفحات منتجاتهم.", "Penjual yang mahukan lebih kawalan ke atas senarai produk mereka."),
 ("Manufacturers", "المصنّعون", "Pengilang"),
 ("Factories and producers launching their own brand on Amazon.", "مصانع ومنتجون يطلقون علامتهم الخاصة على أمازون.", "Kilang dan pengeluar yang melancarkan jenama sendiri di Amazon."),
 ("Wholesale suppliers", "موردو الجملة", "Pembekal borong"),
 ("Brands aiming to sell wholesale to Amazon through Vendor Central.", "علامات تسعى للبيع بالجملة لأمازون عبر Vendor Central.", "Jenama yang ingin menjual secara borong kepada Amazon melalui Vendor Central."),
 ("Amazon brand questions", "أسئلة عن خدمات العلامات على أمازون", "Soalan jenama Amazon"),
 ("Do I need a registered trademark first?", "هل أحتاج إلى علامة تجارية مسجلة أولاً؟", "Adakah saya perlukan tanda dagangan berdaftar dahulu?"),
 ("No. Amazon accepts a pending trademark application from an approved trademark office, so you can apply once it's filed.", "لا. تقبل أمازون طلب علامة قيد التسجيل من مكتب علامات تجارية معتمد، فيمكنك التقديم بمجرد تقديم الطلب.", "Tidak. Amazon menerima permohonan tanda dagangan yang belum selesai daripada pejabat tanda dagangan yang diluluskan, jadi anda boleh memohon sebaik ia difailkan."),
 ("Can I enrol a brand I resell?", "هل يمكنني تسجيل علامة أعيد بيعها؟", "Bolehkah saya mendaftarkan jenama yang saya jual semula?"),
 ("No. Only the trademark owner can enrol a brand. If you resell other brands, Brand Registry isn't for you, but we can help you set up as a seller.", "لا. مالك العلامة التجارية وحده يمكنه تسجيلها. إن كنت تعيد بيع علامات أخرى فهذا البرنامج ليس لك، لكن يمكننا مساعدتك في التسجيل كبائع.", "Tidak. Hanya pemilik tanda dagangan boleh mendaftarkan jenama. Jika anda menjual semula jenama lain, Brand Registry bukan untuk anda, tetapi kami boleh membantu anda mendaftar sebagai penjual."),
 ("Can you get me into Vendor Central?", "هل يمكنكم إدخالي إلى Vendor Central؟", "Bolehkah anda memasukkan saya ke Vendor Central?"),
 ("Vendor Central is by Amazon's invitation, so no one can guarantee access. We help you build the sales record and brand presence Amazon looks for.", "منصة Vendor Central بدعوة من أمازون، لذا لا أحد يستطيع ضمان الدخول إليها. نساعدك في بناء سجل المبيعات والحضور الذي تبحث عنه أمازون.", "Vendor Central adalah melalui jemputan Amazon, jadi tiada siapa boleh menjamin akses. Kami membantu anda membina rekod jualan dan kehadiran jenama yang Amazon cari."),
 ("Does Amazon charge for Brand Registry?", "هل تفرض أمازون رسوماً على Brand Registry؟", "Adakah Amazon mengenakan bayaran untuk Brand Registry?"),
 ("No. Amazon doesn't charge to enrol. Our fee and the trademark office fees are in your written quote.", "لا، لا تفرض أمازون رسوماً على التسجيل. وتشمل رسومنا ورسوم مكتب العلامات في عرض السعر المكتوب.", "Tidak. Amazon tidak mengenakan bayaran untuk mendaftar. Yuran kami dan yuran pejabat tanda dagangan dinyatakan dalam sebut harga bertulis anda."),
 ("Which country should I file my trademark in?", "في أي دولة أسجّل علامتي التجارية؟", "Di negara mana saya patut memfailkan tanda dagangan?"),
 ("Usually where you sell first. Most of our clients start with the US or the UK. Tell us your markets and we'll recommend the office.", "عادةً في السوق الذي تبدأ البيع فيه. يبدأ معظم عملائنا بأمريكا أو بريطانيا. أخبرنا بأسواقك وسنوصي بالجهة المناسبة.", "Biasanya di pasaran tempat anda mula menjual. Kebanyakan pelanggan kami bermula dengan AS atau UK. Beritahu kami pasaran anda dan kami akan mencadangkan pejabatnya."),
 ("Ready to protect your brand on Amazon?", "مستعد لحماية علامتك على أمازون؟", "Bersedia untuk melindungi jenama anda di Amazon?"),
 ("Tell us your brand, products and markets, and we'll send a written quote.", "أخبرنا بعلامتك ومنتجاتك وأسواقك، وسنرسل لك عرض سعر مكتوباً.", "Beritahu kami jenama, produk dan pasaran anda, dan kami akan menghantar sebut harga bertulis."),
]
for en, ar, ms in XTX:
    AR_SRC.setdefault(en, ar)
_ms_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ms_strings.json")
_msx = json.load(open(_ms_path)); _changed = False
for en, ar, ms in XTX:
    if en not in _msx: _msx[en] = ms; _changed = True
if _changed: json.dump(_msx, open(_ms_path, "w"), ensure_ascii=False, indent=0)

XMARK2 = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M6 6l8 8M14 6l-8 8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
DISC = "Wizz Smart Services is a private company. We are not a government agency or a law firm."

def x_hero(code, eyebrow, h1, lede, wa, second, trust, kit_title, kit_small, rows):
    kit = "".join(f'<li><span class="us-kit-ck">{CHECK}</span>{T("span", a)}{T("em", b, "pend" if p else "")}</li>' for a, b, p in rows)
    tr = "".join(f"<li>{CHECK}{T('span', x)}</li>" for x in trust)
    return f'''<section class="page-hero night us-hero">
  <div class="wrap">
    <div>
      <p class="eyebrow"><span class="ltr">{code}</span> · {T("span", eyebrow)}</p>
      {T("h1", h1)}
      {T("p", lede, "lede")}
      <div class="us-cta">
        <a class="btn solid us-red" href="{wa}" target="_blank" rel="noopener"><span class="dot"></span>{T("span", "Talk to us on WhatsApp")}</a>
        <a class="btn ghost us-ghost" href="{second[0]}">{T("span", second[1])}</a>
      </div>
      <ul class="us-trust">{tr}</ul>
    </div>
    <div class="us-kit" aria-hidden="true">
      <div class="us-kit-top"><span class="us-kit-flag ltr">{code}<i>.</i></span><div>{T("b", kit_title)}{T("small", kit_small)}</div>
        <span class="us-kit-price">{T("span", "By quote")}</span></div>
      <ul>{kit}</ul>
    </div>
  </div>
</section>'''

def x_faq(faqs):
    html_ = "".join(f"<details><summary{tk(q)}>{esc(q)}</summary>{T('p', a)}</details>" for q, a in faqs)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False)
    return html_, ld

def x_final(h, p, wa):
    return f'''<section class="us-final night">
  <div class="wrap">
    {T("h2", h)}
    {T("p", p)}
    <div class="us-cta">
      <a class="btn solid us-red" href="{wa}" target="_blank" rel="noopener"><span class="dot"></span>{T("span", "Chat on WhatsApp")}</a>
      <a class="btn ghost us-ghost" href="contact.html">{T("span", "Free consultation")}</a>
    </div>
  </div>
</section>'''

# ---------------- MM2H ----------------
MM_WA = "https://wa.me/601124477685?text=" + urllib.parse.quote("Hi Wizz, I'd like to know more about MM2H.")
mm_hero = x_hero("MY", "Malaysia My Second Home", "Live in Malaysia long term with MM2H",
    "Malaysia My Second Home (MM2H) is a long-stay visa programme run by Malaysia's Ministry of Tourism. We guide you from the first eligibility check to your pass, and our licensed MM2H agent partner submits your application.",
    MM_WA, ("#tiers", "See the tiers"),
    ["Eligibility check before you pay", "Application through a licensed MM2H agent", "Help with the deposit, bank and property steps", "Written quote before you pay"],
    "Your MM2H file", "Silver, Gold or Platinum",
    [("Eligibility check", "Done", 0), ("Document checklist", "Ready", 0), ("Application", "Submitted", 0), ("Fixed deposit", "Placed", 0), ("MM2H pass", "Ministry decides", 1)])
mm_hero += f'\n<p class="us-disc wrap">{T("span", DISC)} {T("span", "MM2H is a visa programme run by the Malaysian government. Forming a company does not give you a visa.")}</p>'

def _row(label, vals, translate=True):
    cells = "".join(T("td", v) if translate else f"<td>{esc(v)}</td>" for v in vals)
    return f'<tr><th scope="row"{tk(label)}>{esc(label)}</th>{cells}</tr>'
mm_table = ('<div class="us-cmp-wrap"><table class="us-cmp mm-tbl"><thead><tr>' + T("th", "Requirement") + T("th", "Silver") + T("th", "Gold") + T("th", "Platinum") + "</tr></thead><tbody>"
    + f'<tr><th scope="row"{tk("Minimum age")}>Minimum age</th><td>25+</td><td>25+</td><td>25+</td></tr>'
    + _row("Fixed deposit in a Malaysian bank", ["USD 150,000", "USD 500,000", "USD 1,000,000"], False)
    + _row("Property to buy (minimum)", ["RM 600,000", "RM 1,000,000", "RM 2,000,000"], False)
    + _row("Pass length", ["5 years", "15 years", "20 years"])
    + _row("Minimum stay", ["90 days a year", "90 days a year", "90 days a year"])
    + _row("Work or run a business", ["No", "No", "Yes, with approval"])
    + "</tbody></table></div>")
mm_steps = [("Eligibility check", "Tell us your age, nationality, family and budget. We check which tier fits, and whether MM2H is right for you.", "Free consultation"),
            ("Documents", "We give you the checklist and review your passport, family documents and financial statements before anything is submitted.", None),
            ("Application through a licensed agent", "Our licensed MM2H agent partner submits your application to MOTAC and follows it until a decision is made.", "Ministry decides"),
            ("Deposit and medical check", "After approval, you place the fixed deposit with a Malaysian bank and complete the medical check.", None),
            ("Pass and property", "Your pass is endorsed in your passport, and you buy your property within the required time.", None)]
mm_steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}' + (f'<span class="us-time">{T("span", t)}</span>' if t else "") + "</li>" for h, p, t in mm_steps)
mm_ents = ent("What MM2H gives you", "A legal, renewable way to live in Malaysia with your family.",
              ["A long-stay pass of 5, 15 or 20 years, by tier", "Renewable when you meet the conditions", "Spouse, children and parents can usually be included as dependants", "Platinum holders can work or run a business, with approval"]) + \
          ent("What it doesn't do", "Be clear on this before you start.",
              ["It isn't citizenship or permanent residency", "Silver and Gold holders can't work in Malaysia", "No one can guarantee approval: MOTAC and Immigration decide every application", "Amounts and rules can change; we confirm them before you apply"]).replace(CHECK, XMARK2)
mm_who = [("addr", "Families relocating", "Parents who want a stable, long-term base in Malaysia for the whole family."),
          ("cal", "Retirees", "People planning to spend part of each year in Malaysia after they stop working."),
          ("bank", "Investors", "Platinum applicants who want to work or run a business in Malaysia, with approval."),
          ("llc", "Business owners", "Founders with a Malaysian company who want long-stay status for their family. The company and the visa are separate applications.")]
mm_who_html = "".join(f'<article class="us-who">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in mm_who)
mm_faq_html, mm_ld = x_faq([
    ("Can I apply for MM2H myself?", "No. Applications must go through a licensed MM2H agent. We work with a licensed agent partner and manage the process with you."),
    ("Do I have to buy property?", "Yes. Each tier sets a minimum property value: RM 600,000 for Silver, RM 1,000,000 for Gold and RM 2,000,000 for Platinum. The purchase is usually due within 12 months of your pass."),
    ("Can I work in Malaysia with MM2H?", "Only the Platinum tier allows work or running a business, with approval. Silver and Gold holders can't work."),
    ("Can my family come with me?", "Usually yes. Your spouse, children and parents can be included as dependants. We check the rules for your family before you apply."),
    ("Is MM2H permanent residency?", "No. It's a renewable long-stay pass. It doesn't give citizenship or permanent residency."),
    ("How much do you charge?", "It depends on the tier and your family. After a free consultation we send a written quote, so you know every cost before you start.")])
mm_body = mm_hero + f'''
<section class="block" id="tiers">
  <div class="wrap">
    {head("The tiers", "Silver, Gold and Platinum", "Set by the Ministry of Tourism, Arts and Culture (MOTAC), as of October 2026. The rules can change, so we confirm them with you before you apply.")}
    {mm_table}
    {T("p", "Up to 50% of the deposit can be withdrawn after approval for approved purposes, such as buying a home, education or healthcare. The property is bought within 12 months of the pass and is usually held for at least 10 years. A Special Economic Zone (SEZ) route with lower amounts also exists; ask us whether it fits you.", "sa-note")}
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("How it works", "From first question to your MM2H pass", "Each application is decided by MOTAC and the Immigration Department. We keep you updated at every step.")}
    <ol class="steps us-steps">{mm_steps_html}</ol>
  </div>
</section>
<section class="block">
  <div class="wrap"><div class="us-ents us-ents-txt">{mm_ents}</div></div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("Who we help", "Built for families and investors moving to Malaysia")}
    <div class="us-whos">{mm_who_html}</div>
  </div>
</section>
<section class="block" id="faq">
  <div class="wrap faq-layout">
    <div>{T("p", "Questions", "eyebrow")}{T("h2", "MM2H questions")}</div>
    <div class="faq">{mm_faq_html}</div>
  </div>
</section>
{x_final("Thinking about MM2H?", "Tell us your age, nationality and family, and we'll tell you which tier fits and what it costs.", MM_WA)}'''
page("mm2h.html", "MM2H Malaysia My Second Home: Tiers, Requirements and Application | Wizz Smart Services",
     "Live in Malaysia long term with MM2H. Silver, Gold and Platinum tiers explained, with eligibility checks and applications through a licensed MM2H agent. Written quote before you pay.",
     mm_body, extra_head=f'<script type="application/ld+json">{mm_ld}</script>', scripts=ar_script())

# ---------------- Amazon brand ----------------
AZ_WA = "https://wa.me/601124477685?text=" + urllib.parse.quote("Hi Wizz, I'd like help with my brand on Amazon (trademark / Brand Registry / Vendor Central).")
az_hero = x_hero("AMZ", "Amazon brand services", "Protect and grow your brand on Amazon",
    "We file your trademark, enrol your brand in Amazon Brand Registry and prepare you for Amazon Vendor Central, so your listings are protected and ready to grow.",
    AZ_WA, ("#services", "See our services"),
    ["Trademark filing for your brand", "Brand Registry enrolment", "Vendor Central readiness", "Written quote before you pay"],
    "Your Amazon brand file", "Own private brand",
    [("Trademark application", "Filed", 0), ("Product and packaging photos", "Checked", 0), ("Brand Registry application", "Submitted", 0), ("Vendor Central", "By Amazon's invitation", 1)])
az_hero += f'\n<p class="us-disc wrap">{T("span", DISC)}</p>'
az_feats = [("llc", "Trademark filing", "We file your trademark with the right office, for example the USPTO in the US or the UKIPO in the UK. Amazon accepts a pending application, so you don't have to wait for registration to apply."),
            ("agent", "Amazon Brand Registry", "We prepare and submit your enrolment: the brand name exactly as on the trademark, your logo, product categories and photos of the brand on your product or packaging."),
            ("ship", "Amazon Vendor Central", "Vendor Central is by Amazon's invitation. We help you build the brand, listings and sales record Amazon looks for, and support your onboarding if you're invited.")]
az_feat_html = "".join(f'<article class="us-feat">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in az_feats)
az_cmp = ent("Seller Central", "You sell to customers as a third-party seller.",
             ["You set your own prices", "You keep control of your listings and stock", "Open to any brand that registers"]) + \
         ent("Vendor Central", "Amazon buys your stock wholesale and sells it to customers.",
             ["Amazon sets the retail price", "Payment on Amazon's terms, often 30 to 90 days", "By Amazon's invitation only"])
az_req = ent("What you need for Brand Registry", "Amazon checks these against your trademark record.",
             ["A registered or pending trademark (a word mark, or a logo with words)", "Your brand name exactly as on the trademark", "Photos of the brand permanently on your product or packaging, not stickers", "Your product categories"]) + \
         ent("What we can't promise", "Be clear on this before you start.",
             ["Trademark offices decide every registration", "Amazon decides Brand Registry and Vendor Central access", "An invitation to Vendor Central isn't guaranteed", "Sales depend on your product and market"]).replace(CHECK, XMARK2)
az_steps = [("Brand check", "Tell us your brand name, products and markets. We check the name and recommend which office to file with.", "Free consultation"),
            ("Trademark filing", "We file your application and send you the filing receipt and number.", None),
            ("Brand Registry", "With your trademark filed, we submit your Brand Registry enrolment and follow Amazon's verification.", None),
            ("Grow and Vendor Central", "We help you use the brand tools, and get ready in case Amazon invites you to Vendor Central.", None)]
az_steps_html = "".join(f'<li>{T("h3", h)}{T("p", p)}' + (f'<span class="us-time">{T("span", t)}</span>' if t else "") + "</li>" for h, p, t in az_steps)
az_who = [("brand", "Private-label brands", "Brands that make products under their own name and want them protected."),
          ("cart", "Amazon sellers", "Sellers who want more control over their product listings."),
          ("ship", "Manufacturers", "Factories and producers launching their own brand on Amazon."),
          ("bank", "Wholesale suppliers", "Brands aiming to sell wholesale to Amazon through Vendor Central.")]
az_who_html = "".join(f'<article class="us-who">{icon(k)}{T("h3", h)}{T("p", p)}</article>' for k, h, p in az_who)
az_faq_html, az_ld = x_faq([
    ("Do I need a registered trademark first?", "No. Amazon accepts a pending trademark application from an approved trademark office, so you can apply once it's filed."),
    ("Can I enrol a brand I resell?", "No. Only the trademark owner can enrol a brand. If you resell other brands, Brand Registry isn't for you, but we can help you set up as a seller."),
    ("Can you get me into Vendor Central?", "Vendor Central is by Amazon's invitation, so no one can guarantee access. We help you build the sales record and brand presence Amazon looks for."),
    ("Does Amazon charge for Brand Registry?", "No. Amazon doesn't charge to enrol. Our fee and the trademark office fees are in your written quote."),
    ("Which country should I file my trademark in?", "Usually where you sell first. Most of our clients start with the US or the UK. Tell us your markets and we'll recommend the office.")])
az_body = az_hero + f'''
<section class="block" id="services">
  <div class="wrap">
    {head("What we do", "Three services, one brand file")}
    <div class="us-feats">{az_feat_html}</div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("Seller Central or Vendor Central", "Two ways to sell on Amazon")}
    <div class="us-ents us-ents-txt">{az_cmp}</div>
  </div>
</section>
<section class="block">
  <div class="wrap">
    {head("How it works", "From brand name to protected listings", "Trademark office and Amazon review times vary. We keep you updated.")}
    <ol class="steps us-steps az-steps">{az_steps_html}</ol>
    <div class="us-ents us-ents-txt sa-req">{az_req}</div>
  </div>
</section>
<section class="block alt">
  <div class="wrap">
    {head("Who we help", "Built for brand owners selling on Amazon")}
    <div class="us-whos">{az_who_html}</div>
  </div>
</section>
<section class="block" id="faq">
  <div class="wrap faq-layout">
    <div>{T("p", "Questions", "eyebrow")}{T("h2", "Amazon brand questions")}</div>
    <div class="faq">{az_faq_html}</div>
  </div>
</section>
{x_final("Ready to protect your brand on Amazon?", "Tell us your brand, products and markets, and we'll send a written quote.", AZ_WA)}'''
page("amazon-brand.html", "Amazon Brand Registry, Trademark Filing and Vendor Central | Wizz Smart Services",
     "Trademark filing, Amazon Brand Registry enrolment and Vendor Central readiness for brand owners. Written quote before you pay.",
     az_body, extra_head=f'<script type="application/ld+json">{az_ld}</script>', scripts=ar_script())

US_CSS += """
.mm-tbl{min-width:560px}.mm-tbl td{text-align:center;font-weight:600}
.az-steps{grid-template-columns:repeat(4,minmax(0,1fr))}
@media (max-width:1000px){.az-steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.az-steps{grid-template-columns:1fr}}
"""
