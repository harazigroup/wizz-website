#!/usr/bin/env python3
"""Adds a blog post in English, Arabic and Malay, then rebuilds the site.

Usage:  python3 tools/new_post.py post.json
post.json:
{ "id": "post-uae-free-zone", "slug": "blog-uae-free-zone-or-mainland.html", "date": "2026-10-14",
  "en": {"tag": "...", "title": "...", "lede": "...", "body": "<p>...</p><h3>...</h3><ul><li>...</li></ul>"},
  "ar": {...same keys...}, "ms": {...same keys...} }

What it does: adds the post to site.js (POSTS, newest first, and POST_SLUGS), adds the Malay version to
tools/posts_ms.json, creates the article page from an existing one, refreshes the English blog grids
(blog.html, index.html), then runs tools/build_pkgs.py, which builds /ar/ and /ms/ and the sitemap.
Body HTML may use <p>, <h3>, <ul>/<ol>/<li>, <b>, <a href="page.html">. No images, no scripts.
"""
import html, json, re, subprocess, sys, os
from bs4 import BeautifulSoup

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = D + "/tools"
TEMPLATE = D + "/blog-llc-or-ltd.html"
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
ALLOWED = {"p", "h3", "ul", "ol", "li", "b", "strong", "a", "em", "br"}

def fail(m): raise SystemExit("new_post: " + m)

spec = json.load(open(sys.argv[1]))
pid, slug, date = spec["id"], spec["slug"], spec["date"]
if not re.fullmatch(r"post-[a-z0-9-]+", pid): fail("id must look like post-some-topic")
if not re.fullmatch(r"blog-[a-z0-9-]+\.html", slug): fail("slug must look like blog-some-topic.html")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date): fail("date must be YYYY-MM-DD")
for l in ("en", "ar", "ms"):
    p = spec.get(l) or fail(f"missing {l}")
    for k in ("tag", "title", "lede", "body"):
        if not str(p.get(k, "")).strip(): fail(f"{l}.{k} is empty")
    tags = {t.name for t in BeautifulSoup(p["body"], "html.parser").find_all(True)}
    if tags - ALLOWED: fail(f"{l}.body uses tags that aren't allowed: {sorted(tags - ALLOWED)}")
    for a in BeautifulSoup(p["body"], "html.parser").find_all("a"):
        href = a.get("href", "")
        if not (re.fullmatch(r"[a-z0-9-]+\.html(#[a-z0-9-]+)?", href) or href.startswith("https://wa.me/")):
            fail(f"{l}.body link {href!r}: use a page of this site like usa.html")
        if not href.startswith("https://") and not os.path.exists(f"{D}/{href.split('#')[0]}"): fail(f"{l}.body links to a missing page: {href}")

site = open(D + "/site.js").read()
if f'"{pid}"' in site or f"'{pid}'" in site: fail(f"{pid} already exists")
if os.path.exists(f"{D}/{slug}"): fail(f"{slug} already exists")

# 1) site.js: POSTS (newest first) and POST_SLUGS
entry = json.dumps({"id": pid, "date": date, "en": spec["en"], "ar": spec["ar"]}, ensure_ascii=False)
site = site.replace("const POSTS = [\n", "const POSTS = [\n" + entry + ",\n", 1)
m = re.search(r"const POST_SLUGS = (\{.*?\});", site)
slugs = json.loads(m.group(1)); slugs = {pid: slug, **slugs}
site = site[:m.start(1)] + json.dumps(slugs, ensure_ascii=False) + site[m.end(1):]
open(D + "/site.js", "w").write(site)

# 2) Malay
ms = json.load(open(T + "/posts_ms.json")); ms[pid] = spec["ms"]
json.dump(ms, open(T + "/posts_ms.json", "w"), ensure_ascii=False, indent=0)

# 3) article page from the template
en = spec["en"]
def meta_line(p, d):
    y, mo, dd = map(int, d.split("-"))
    words = len((p["lede"] + " " + re.sub(r"<[^>]+>", " ", p["body"])).split())
    return f"{dd} {MONTHS[mo-1]} {y} · {max(2, round(words/200))} min read"
soup = BeautifulSoup(open(TEMPLATE).read(), "html.parser")
old_slug = os.path.basename(TEMPLATE)
soup.select_one("[data-post]")["data-post"] = pid
for i, v in (("rTag", en["tag"]), ("rTitle", en["title"]), ("rMeta", meta_line(en, date)), ("rLede", en["lede"])):
    soup.find(id=i).string = v
body = soup.find(id="rBody"); body.clear(); body.append(BeautifulSoup(en["body"], "html.parser"))
title = f'{en["title"]} | Wizz Smart Services'
soup.title.string = title
for sel, val in (('meta[name="description"]', en["lede"]), ('meta[property="og:title"]', title), ('meta[property="og:description"]', en["lede"]),
                 ('meta[name="twitter:title"]', title), ('meta[name="twitter:description"]', en["lede"])):
    t = soup.select_one(sel)
    if t: t["content"] = val
out = str(soup).replace(old_slug, slug)
open(f"{D}/{slug}", "w").write(out)

# 4) English blog grids (the Arabic and Malay ones are rebuilt by build_ar.py)
site_posts = json.loads(subprocess.run(["node", "-e", r"""
const s=require('fs').readFileSync(process.argv[1],'utf8');
const P=s.slice(s.indexOf('const POSTS = ['),s.indexOf('const POST_SLUGS'));
eval(P.replace('const POSTS','globalThis.POSTS'));console.log(JSON.stringify(POSTS));""", D + "/site.js"], capture_output=True, text=True, check=True).stdout)
E = lambda x: html.escape(x, quote=True)
for page in ("blog.html", "index.html"):
    raw = open(f"{D}/{page}").read()
    m = re.search(r'(<div class="posts" id="blogGrid"([^>]*)>)(.*?)(</div>)', raw, re.S)
    if not m: continue
    lim = int((re.search(r'data-limit="(\d+)"', m.group(2)) or [None, len(site_posts)])[1])
    cards = "".join(f'<a class="post" href="{slugs[p_["id"]]}"><span class="ptag">{E(p_["en"]["tag"])}</span><h3>{E(p_["en"]["title"])}</h3><p>{E(p_["en"]["lede"])}</p><span class="pfoot"><span>{E(meta_line(p_["en"], p_["date"]))}</span><b>Read article</b></span></a>' for p_ in site_posts[:lim])
    open(f"{D}/{page}", "w").write(raw[:m.start(3)] + cards + raw[m.end(3):])

# 5) rebuild everything (Arabic + Malay pages, sitemap)
subprocess.run([sys.executable, "build_pkgs.py"], cwd=T, check=True)
subprocess.run(["rm", "-rf", T + "/__pycache__"])
print(f"added {pid} -> {slug} (+ ar/{slug}, ms/{slug})")
