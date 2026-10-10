#!/usr/bin/env python3
"""Builds the Arabic site under /ar/: one pre-translated copy of each public page, so every page has its own
Arabic URL (wizz.com.my/ar/...), Arabic text in the HTML for search engines, and hreflang links between versions.
Run after build_pkgs.py (it calls this at the end). Assets resolve through the /ar/* rewrite in netlify.toml."""
import glob, json, os, re, subprocess
from bs4 import BeautifulSoup

D = "/home/claude/wizz-dist"
SITE = "https://wizz.com.my"
SKIP = {"admin.html"}
OUT = f"{D}/ar"

site_js = open(f"{D}/site.js").read()
AR = json.loads(re.match(r"const AR = (\{.*?\});\n", site_js).group(1))

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
MONTHS = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
def meta_line(post):
    y, m, d = map(int, post["date"].split("-"))
    words = len((post["ar"]["lede"] + " " + re.sub(r"<[^>]+>", " ", post["ar"]["body"])).split())
    return f"{d} {MONTHS[m-1]} {y} · وقت القراءة: {max(2, round(words/200))} د"

def url_for(name, ar):
    path = "" if name == "index.html" else name
    return f"{SITE}/ar/{path}" if ar else f"{SITE}/{path}"

def frag(html):
    return BeautifulSoup(html, "html.parser")

def set_inner(el, value, is_html):
    el.clear()
    if is_html: el.append(frag(value))
    else: el.string = value

def alternates(name):
    return (f'<link rel="alternate" hreflang="en" href="{url_for(name, False)}">\n'
            f'<link rel="alternate" hreflang="ar" href="{url_for(name, True)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url_for(name, False)}">\n')

os.makedirs(OUT, exist_ok=True)
for old in glob.glob(f"{OUT}/*.html"): os.remove(old)
pages = sorted(p for p in glob.glob(f"{D}/*.html") if os.path.basename(p) not in SKIP)
for path in pages:
    name = os.path.basename(path)
    src = open(path).read()
    # English page: add hreflang links (once)
    src = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", src)
    src = src.replace("</head>", alternates(name) + "</head>", 1)
    open(path, "w").write(src)
    d = dict(AR)
    m = re.search(r"window\.WIZZ_AR=(\{.*?\});</script>", src, re.S)
    if m: d.update(json.loads(m.group(1).replace("<\\/", "</")))
    soup = BeautifulSoup(src, "html.parser")
    soup.html["lang"] = "ar"; soup.html["dir"] = "rtl"
    for el in soup.select("[data-i18n]"):
        v = d.get(el["data-i18n"])
        if v is not None: set_inner(el, v, el.has_attr("data-html"))
    for el in soup.select("[data-i18n-ph]"):
        v = d.get(el["data-i18n-ph"])
        if v is not None: el["placeholder"] = v
    lb = soup.find(id="langBtn")
    if lb: lb.string = "English"
    # blog listing and articles (rendered from POSTS)
    grid = soup.find(id="blogGrid")
    if grid:
        lim = int(grid.get("data-limit") or len(POSTS))
        grid.clear()
        for post in POSTS[:lim]:
            p = post["ar"]
            a = soup.new_tag("a", attrs={"class": "post", "href": SLUGS[post["id"]]})
            for tag, cls, txt in (("span", "ptag", p["tag"]), ("h3", None, p["title"]), ("p", None, p["lede"])):
                t = soup.new_tag(tag, attrs={"class": cls} if cls else {}); t.string = txt; a.append(t)
            foot = soup.new_tag("span", attrs={"class": "pfoot"}); s1 = soup.new_tag("span"); s1.string = meta_line(post)
            b = soup.new_tag("b"); b.string = "اقرأ المقال"; foot.append(s1); foot.append(b); a.append(foot)
            grid.append(a)
    art = soup.select_one("[data-post]")
    post = next((x for x in POSTS if art and x["id"] == art["data-post"]), None)
    if post:
        p = post["ar"]
        for i, v in (("rTag", p["tag"]), ("rTitle", p["title"]), ("rLede", p["lede"]), ("rMeta", meta_line(post))):
            soup.find(id=i).string = v
        set_inner(soup.find(id="rBody"), p["body"], True)
    # title, description, canonical, social tags
    h1 = soup.find("h1")
    lede = soup.select_one(".lede, .standfirst")
    h1t = h1.get_text(" ", strip=True) if h1 else ""
    title = "ويز للخدمات الذكية | تأسيس الشركات والمنصات والخدمات اللوجستية في 13 دولة" if name == "index.html" else (f"{h1t} | ويز للخدمات الذكية" if h1t else None)
    if title:
        soup.title.string = title
        for sel in ('meta[property="og:title"]', 'meta[name="twitter:title"]'):
            t = soup.select_one(sel)
            if t: t["content"] = title
    if lede:
        desc = lede.get_text(" ", strip=True)
        for sel in ('meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]'):
            t = soup.select_one(sel)
            if t: t["content"] = desc
    can = soup.select_one('link[rel="canonical"]')
    if can: can["href"] = url_for(name, True)
    og = soup.select_one('meta[property="og:url"]')
    if og: og["content"] = url_for(name, True)
    loc = soup.select_one('meta[property="og:locale"]')
    if loc: loc["content"] = "ar_AR"
    open(f"{OUT}/{name}", "w").write(str(soup))

# sitemap: add the Arabic pages next to the English ones
sm = f"{D}/sitemap.xml"
s = open(sm).read()
s = re.sub(r"  <url><loc>https://wizz\.com\.my/ar/[^<]*</loc></url>\n", "", s)
en = re.findall(r"<loc>(https://wizz\.com\.my/[^<]*)</loc>", s)
extra = "".join(f"  <url><loc>{u.replace(SITE + '/', SITE + '/ar/', 1)}</loc></url>\n" for u in en)
s = s.replace("</urlset>", extra + "</urlset>")
open(sm, "w").write(s)
print("arabic pages:", len(pages))
