#!/usr/bin/env python3
"""Builds the translated sites: Arabic under /ar/ and Malay under /ms/. Each public page gets a pre-translated copy
with its own URL (wizz.com.my/ar/..., wizz.com.my/ms/...), translated text in the HTML for search engines, and
hreflang links between the versions. Run after build_pkgs.py (it calls this at the end). Assets resolve through
the /ar/* and /ms/* rewrites in netlify.toml.

Arabic comes from the data-i18n keys (site.js AR dict + each page's window.WIZZ_AR).
Malay comes from tools/ms_strings.json (English text -> Malay) and tools/posts_ms.json (blog posts)."""
import glob, html, json, os, re, subprocess
from bs4 import BeautifulSoup

D = "/home/claude/wizz-dist"
T = os.path.dirname(os.path.abspath(__file__))
SITE = "https://wizz.com.my"
SKIP = {"admin.html", "quote.html", "invoice.html"}
LANGS = ("ar", "ms")

site_js = open(f"{D}/site.js").read()
AR = json.loads(re.match(r"const AR = (\{.*?\});\n", site_js).group(1))
MS = json.load(open(f"{T}/ms_strings.json"))
# runtime strings in the JS source carry \' escapes; the browser sees plain apostrophes
MS.update({k.replace("\\'", "'"): v.replace("\\'", "'") for k, v in list(MS.items()) if "\\'" in k})
MS_POSTS = json.load(open(f"{T}/posts_ms.json"))

# blog posts live in site.js as a JS array; let node turn them into JSON
NODE = r"""
const s=require('fs').readFileSync(process.argv[1],'utf8');
const P=s.slice(s.indexOf('const POSTS = ['),s.indexOf('const POST_SLUGS'));
const S=s.slice(s.indexOf('const POST_SLUGS'),s.indexOf(';',s.indexOf('const POST_SLUGS'))+1);
eval(P.replace('const POSTS','globalThis.POSTS')+S.replace('const POST_SLUGS','globalThis.POST_SLUGS'));
console.log(JSON.stringify({posts:POSTS,slugs:POST_SLUGS}));
"""
blog = json.loads(subprocess.run(["node", "-e", NODE, f"{D}/site.js"], capture_output=True, text=True, check=True).stdout)
POSTS, SLUGS = blog["posts"], blog["slugs"]
for p in POSTS:
    p["ms"] = MS_POSTS.get(p["id"])
    if not p["ms"]: raise SystemExit(f"Missing Malay blog post in tools/posts_ms.json: {p['id']}")

CFG = {
    "ar": dict(dir="rtl", locale="ar_AR", read="اقرأ المقال",
               months=["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"],
               mins=lambda n: f"وقت القراءة: {n} د", suffix=" | ويز للخدمات الذكية",
               home="ويز للخدمات الذكية | تأسيس الشركات والمنصات والخدمات اللوجستية في 14 دولة"),
    "ms": dict(dir="ltr", locale="ms_MY", read="Baca artikel",
               months=["Jan","Feb","Mac","Apr","Mei","Jun","Jul","Ogo","Sep","Okt","Nov","Dis"],
               mins=lambda n: f"{n} min bacaan", suffix=" | Wizz Smart Services",
               home="Wizz Smart Services | Penubuhan syarikat, pasaran dalam talian dan logistik di 14 negara"),
}

def meta_line(post, l):
    y, m, d = map(int, post["date"].split("-"))
    p = post[l]
    words = len((p["lede"] + " " + re.sub(r"<[^>]+>", " ", p["body"])).split())
    return f"{d} {CFG[l]['months'][m-1]} {y} · {CFG[l]['mins'](max(2, round(words/200)))}"

def url_for(name, l):
    path = "" if name == "index.html" else name
    return f"{SITE}/{path}" if l == "en" else f"{SITE}/{l}/{path}"

def frag(h):
    return BeautifulSoup(h, "html.parser")

def set_inner(el, value, is_html):
    el.clear()
    if is_html: el.append(frag(value))
    else: el.string = value

def alternates(name):
    return (f'<link rel="alternate" hreflang="en" href="{url_for(name, "en")}">\n'
            f'<link rel="alternate" hreflang="ar" href="{url_for(name, "ar")}">\n'
            f'<link rel="alternate" hreflang="ms" href="{url_for(name, "ms")}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url_for(name, "en")}">\n')

# short labels where the header has little room
MS_KEY = {"nav_mp": "Pasaran", "nav_acq": "Pemerolehan", "cta_short": "Rundingan percuma"}

def ms_lookup(el, is_html):
    """Malay for an element, looked up by its English content. Returns (value, value_is_html) or None."""
    raw = el.decode_contents().strip()
    for cand in (raw, html.unescape(raw), el.get_text()):
        if cand in MS:
            v = MS[cand]
            return v, bool(re.search(r"<[a-z]", v))
    return None

# runtime strings (cart, checkout, account, forms): English -> Malay, read by the T() helpers on /ms/ pages
RT = {k: v for k, v in MS.items() if "<" not in k or "<span" in k}
MS_RT_SCRIPT = "<script>window.WIZZ_MS=" + json.dumps(RT, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"

missing = {}
for l in LANGS:
    os.makedirs(f"{D}/{l}", exist_ok=True)
    for old in glob.glob(f"{D}/{l}/*.html"): os.remove(old)
pages = sorted(p for p in glob.glob(f"{D}/*.html") if os.path.basename(p) not in SKIP)
for path in pages:
    name = os.path.basename(path)
    src = open(path).read()
    # English page: hreflang links (once)
    src = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", src)
    src = src.replace("</head>", alternates(name) + "</head>", 1)
    open(path, "w").write(src)
    page_ar = dict(AR)
    m = re.search(r"window\.WIZZ_AR=(\{.*?\});</script>", src, re.S)
    if m: page_ar.update(json.loads(m.group(1).replace("<\\/", "</")))
    for l in LANGS:
        c = CFG[l]
        soup = BeautifulSoup(src, "html.parser")
        soup.html["lang"] = l; soup.html["dir"] = c["dir"]
        for el in soup.select("[data-i18n]"):
            if l == "ar":
                v = page_ar.get(el["data-i18n"])
                if v is not None: set_inner(el, v, el.has_attr("data-html"))
            elif el["data-i18n"] in MS_KEY:
                set_inner(el, MS_KEY[el["data-i18n"]], False)
            else:
                hit = ms_lookup(el, el.has_attr("data-html"))
                if hit: set_inner(el, hit[0], hit[1])
                elif el.get_text(strip=True): missing.setdefault(el.get_text(" ", strip=True)[:90], name)
        for el in soup.select("[data-i18n-ph]"):
            if l == "ar":
                v = page_ar.get(el["data-i18n-ph"])
                if v is not None: el["placeholder"] = v
            else:
                ph = el.get("placeholder", "")
                if ph in MS: el["placeholder"] = MS[ph]
                elif ph: missing.setdefault(ph, name)
        sel = soup.find(id="langSel")
        if sel:
            for o in sel.find_all("option"):
                if o.get("value") == l: o["selected"] = ""
                elif o.has_attr("selected"): del o["selected"]
        # blog listing and articles (rendered from POSTS)
        grid = soup.find(id="blogGrid")
        if grid:
            lim = int(grid.get("data-limit") or len(POSTS))
            grid.clear()
            for post in POSTS[:lim]:
                p = post[l]
                a = soup.new_tag("a", attrs={"class": "post", "href": SLUGS[post["id"]]})
                for tag, cls, txt in (("span", "ptag", p["tag"]), ("h3", None, p["title"]), ("p", None, p["lede"])):
                    t = soup.new_tag(tag, attrs={"class": cls} if cls else {}); t.string = txt; a.append(t)
                foot = soup.new_tag("span", attrs={"class": "pfoot"}); s1 = soup.new_tag("span"); s1.string = meta_line(post, l)
                b = soup.new_tag("b"); b.string = c["read"]; foot.append(s1); foot.append(b); a.append(foot)
                grid.append(a)
        art = soup.select_one("[data-post]")
        post = next((x for x in POSTS if art and x["id"] == art["data-post"]), None)
        if post:
            p = post[l]
            for i, v in (("rTag", p["tag"]), ("rTitle", p["title"]), ("rLede", p["lede"]), ("rMeta", meta_line(post, l))):
                soup.find(id=i).string = v
            set_inner(soup.find(id="rBody"), p["body"], True)
        # title, description, canonical, social tags
        h1 = soup.find("h1")
        lede = soup.select_one(".lede, .standfirst")
        h1t = h1.get_text(" ", strip=True) if h1 else ""
        title = c["home"] if name == "index.html" else (f"{h1t}{c['suffix']}" if h1t else None)
        if title:
            soup.title.string = title
            for s_ in ('meta[property="og:title"]', 'meta[name="twitter:title"]'):
                t = soup.select_one(s_)
                if t: t["content"] = title
        if lede:
            desc = lede.get_text(" ", strip=True)
            for s_ in ('meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]'):
                t = soup.select_one(s_)
                if t: t["content"] = desc
        can = soup.select_one('link[rel="canonical"]')
        if can: can["href"] = url_for(name, l)
        og = soup.select_one('meta[property="og:url"]')
        if og: og["content"] = url_for(name, l)
        loc = soup.select_one('meta[property="og:locale"]')
        if loc: loc["content"] = c["locale"]
        out = str(soup)
        if l == "ms": out = out.replace("</head>", MS_RT_SCRIPT + "</head>", 1)
        open(f"{D}/{l}/{name}", "w").write(out)

# sitemap: the translated pages next to the English ones
sm = f"{D}/sitemap.xml"
s = open(sm).read()
s = re.sub(r"  <url><loc>https://wizz\.com\.my/(ar|ms)/[^<]*</loc></url>\n", "", s)
en = re.findall(r"<loc>(https://wizz\.com\.my/[^<]*)</loc>", s)
extra = "".join(f"  <url><loc>{u.replace(SITE + '/', SITE + '/' + l + '/', 1)}</loc></url>\n" for l in LANGS for u in en)
s = s.replace("</urlset>", extra + "</urlset>")
open(sm, "w").write(s)
print("translated pages:", len(pages), "x", len(LANGS))
if missing:
    print(f"Malay missing for {len(missing)} strings:")
    for k, v in list(missing.items())[:60]: print(f"  [{v}] {k}")
