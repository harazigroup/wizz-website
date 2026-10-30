#!/usr/bin/env python3
"""Friday "Jumaat Mubarak / جمعة مباركة" post for Instagram and TikTok (@wizz.com.my).

Usage:  python3 tools/social/jumuah.py [YYYY-MM-DD] [out_dir]
        (date defaults to today in Malaysia time; out_dir defaults to tools/social/out/jumuah-<date>)

Writes:
  jumuah-<date>-tiktok.png     1080x1920, text kept above TikTok's caption area
  jumuah-<date>-instagram.png  1080x1350 (4:5 feed post)
  caption.txt                  Malay + Arabic caption with hashtags

The verse, the prayer line and the colour theme rotate by week number, so every Friday is different.
Verses come only from jumuah_verses.json (Quran text checked by a person). Never type a verse by hand
in this script or in a caption: a wrong letter in a Quran verse is a serious mistake.
Setup once: cd tools/social && npm install   (fonts: Amiri for the Quran, IBM Plex Sans Arabic, Archivo, Plex)
"""
import asyncio, datetime as dt, html, json, os, sys
from playwright.async_api import async_playwright

D = os.path.dirname(os.path.abspath(__file__))
F = D + "/node_modules/@fontsource"
LOGO = open(D + "/logo_inner.svg").read()
DATA = json.load(open(D + "/jumuah_verses.json"))
SAFE_BOTTOM = 1380  # same limit as carousel.py: below this TikTok's caption and buttons cover the image

THEMES = [  # sky top, sky bottom, mosque, accent (gold), glow
    dict(name="night", top="#0B1530", bot="#1D3A66", mosque="#081022", gold="#E7C77A", glow="rgba(231,199,122,.35)"),
    dict(name="emerald", top="#062A23", bot="#0F5546", mosque="#041A16", gold="#E9CF8C", glow="rgba(233,207,140,.32)"),
    dict(name="dusk", top="#2A1636", bot="#7A3B4E", mosque="#1A0D22", gold="#F2D193", glow="rgba(242,209,147,.38)"),
]

def mosque_svg(c, w, h):
    """Layered mosque skyline: a big central dome with two minarets, smaller domes either side."""
    g = c["gold"]
    return f'''<svg viewBox="0 0 1080 520" width="{w}" height="{h}" preserveAspectRatio="xMidYMax slice" style="display:block">
  <defs><linearGradient id="lit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g}" stop-opacity=".55"/><stop offset=".25" stop-color="{g}" stop-opacity="0"/></linearGradient></defs>
  <g fill="{c["mosque"]}" opacity=".55">
    <path d="M0 360 Q60 300 120 360 L120 520 L0 520Z"/><path d="M930 350 Q1000 280 1080 340 L1080 520 L930 520Z"/>
    <rect x="70" y="250" width="22" height="150"/><path d="M66 250 L81 200 L96 250Z"/>
    <rect x="985" y="230" width="22" height="160"/><path d="M981 230 L996 180 L1011 230Z"/>
  </g>
  <g fill="{c["mosque"]}">
    <rect x="250" y="130" width="34" height="390"/><path d="M244 130 L267 52 L290 130Z"/><rect x="240" y="200" width="54" height="10"/><rect x="240" y="300" width="54" height="10"/>
    <rect x="796" y="130" width="34" height="390"/><path d="M790 130 L813 52 L836 130Z"/><rect x="786" y="200" width="54" height="10"/><rect x="786" y="300" width="54" height="10"/>
    <path d="M330 330 Q330 170 540 150 Q750 170 750 330 Z"/><rect x="530" y="96" width="20" height="56"/>
    <path d="M300 520 L300 330 L780 330 L780 520Z"/>
    <path d="M150 520 L150 400 Q150 330 225 320 Q300 330 300 400 L300 520Z"/>
    <path d="M780 520 L780 400 Q780 330 855 320 Q930 330 930 400 L930 520Z"/>
  </g>
  <path d="M330 330 Q330 170 540 150 Q750 170 750 330 Z" fill="url(#lit)"/>
  <g fill="{g}" opacity=".9">
    <path d="M540 70 a16 16 0 1 0 12 26 a12 12 0 1 1 -12 -26Z"/>
    <path d="M470 520 L470 420 Q470 380 540 372 Q610 380 610 420 L610 520Z" opacity=".55"/>
    <path d="M360 430 Q360 400 385 396 Q410 400 410 430 L410 470 L360 470Z" opacity=".4"/>
    <path d="M670 430 Q670 400 695 396 Q720 400 720 430 L720 470 L670 470Z" opacity=".4"/>
  </g>
</svg>'''

def stars(seed, n=46):
    import random
    r = random.Random(seed)
    return "".join(f'<i style="left:{r.randint(20,1060)}px;top:{r.randint(20,760)}px;width:{s}px;height:{s}px;opacity:{r.uniform(.35,.9):.2f}"></i>'
                   for s in (r.choice((2, 2, 3, 4)) for _ in range(n)))

CSS = """
@font-face{font-family:Amiri;src:url('file://F/amiri/files/amiri-arabic-400-normal.woff2');font-weight:400}
@font-face{font-family:Amiri;src:url('file://F/amiri/files/amiri-arabic-700-normal.woff2');font-weight:700}
@font-face{font-family:PlexAr;src:url('file://F/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-400-normal.woff2');font-weight:400}
@font-face{font-family:PlexAr;src:url('file://F/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-600-normal.woff2');font-weight:600}
@font-face{font-family:Archivo;src:url('file://F-variable/archivo/files/archivo-latin-wdth-normal.woff2');font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:Plex;src:url('file://F/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2');font-weight:400}
@font-face{font-family:Plex;src:url('file://F/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;overflow:hidden;font-family:Plex,sans-serif;color:#fff}
.s{position:relative;width:1080px;overflow:hidden;background:linear-gradient(180deg,TOP 0%,BOT 78%)}
.stars i{position:absolute;border-radius:50%;background:#fff}
.glow{position:absolute;left:50%;width:900px;height:900px;margin-left:-450px;border-radius:50%;background:radial-gradient(circle,GLOW 0%,transparent 62%)}
.m{position:absolute;left:0;right:0;bottom:0}
.c{position:relative;z-index:2;padding:0 110px;text-align:center}
.brand{display:flex;align-items:center;justify-content:center;gap:20px;color:#fff}
.brand svg{height:58px}
.bname{font:600 24px Plex;line-height:1.15;text-align:left;padding-left:18px;border-left:2px solid rgba(255,255,255,.6);opacity:.9}
.orn{color:GOLD;font:400 34px Amiri;letter-spacing:.3em;opacity:.85}
h1{font:700 128px/1.15 Amiri;color:GOLD;direction:rtl;text-shadow:0 4px 30px rgba(0,0,0,.35)}
.lat{font-family:Archivo;font-weight:800;font-stretch:92%;font-size:52px;letter-spacing:.04em;text-transform:uppercase}
.card{margin:0 auto;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);border-radius:34px;padding:44px 50px;backdrop-filter:blur(2px)}
.ay{font:400 SIZEpx/1.95 Amiri;direction:rtl;color:#fff}
.ref{font:600 25px PlexAr;color:GOLD;direction:rtl;margin-top:10px}
.ms{font:400 31px/1.45 Plex;opacity:.92;margin-top:26px}
.msref{font:600 23px Plex;color:GOLD;margin-top:12px;letter-spacing:.02em}
.dua{font:400 37px/1.6 Amiri;direction:rtl;color:GOLD}
.duams{font:400 27px/1.45 Plex;opacity:.85;margin-top:6px}
.site{font:600 24px Plex;opacity:.75;letter-spacing:.06em}
"""

def page(c, v, d, h, story):
    css = (CSS.replace("file://F", "file://" + F).replace("TOP", c["top"]).replace("BOT", c["bot"]).replace("GOLD", c["gold"])
           .replace("GLOW", c["glow"]).replace("SIZE", str(46 if len(v["ar"]) < 90 else 40 if len(v["ar"]) < 150 else 35)))
    gap = 44 if story else 30
    mh = 560 if story else 420
    body = f'''<div class="s" style="height:{h}px">
<div class="stars">{stars(v["ref_en"])}</div><div class="glow" style="top:{120 if story else 40}px"></div>
<div class="m" style="{"" if story else "opacity:.45;bottom:-40px"}">{mosque_svg(c, 1080, mh)}</div>
<div class="c" style="padding-top:{110 if story else 64}px;display:flex;flex-direction:column;gap:{gap}px">
  <div class="brand"><svg viewBox="330 428 420 204">{LOGO}</svg><span class="bname">Wizz Smart<br>Services</span></div>
  <div><h1>جمعة مباركة</h1><div class="lat">Jumaat Mubarak</div></div>
  <div class="card"><div class="ay">﴿ {html.escape(v["ar"])} ﴾</div><div class="ref">{html.escape(v["ref_ar"])}</div>
    <div class="ms">“{html.escape(v["ms"])}”</div><div class="msref">{html.escape(v["ref_ms"])}</div></div>
  <div><div class="dua">{html.escape(d["ar"])}</div><div class="duams">{html.escape(d["ms"])}</div></div>
  {'' if story else '<div class="site">wizz.com.my</div>'}
</div></div>'''
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'

async def main(day, out):
    wk = day.isocalendar()[1]
    v = DATA["verses"][wk % len(DATA["verses"])]
    d = DATA["prayers"][wk % len(DATA["prayers"])]
    c = THEMES[wk % len(THEMES)]
    os.makedirs(out, exist_ok=True)
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for kind, h in (("tiktok", 1920), ("instagram", 1350)):
            pg = await b.new_page(viewport={"width": 1080, "height": h})
            path = f"{out}/.{kind}.html"; open(path, "w").write(page(c, v, d, h, kind == "tiktok"))
            await pg.goto("file://" + path); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            low = await pg.evaluate("Math.max(...[...document.querySelectorAll('.c > *')].map(e=>e.getBoundingClientRect().bottom))")
            limit = SAFE_BOTTOM if kind == "tiktok" else h - 40
            f = f"{out}/jumuah-{day}-{kind}.png"
            await pg.screenshot(path=f)
            print(f, "ok" if low <= limit else "CHECK")
            if low > limit: bad.append(f"{kind}: text reaches {int(low)}px (limit {limit})")
            os.remove(path)
        await b.close()
    cap = (f"Jumaat Mubarak 🤍 جمعة مباركة\n\n{v['ms']} ({v['ref_ms']})\n\n{d['ms']}\n{d['ar']}\n\n"
           "#JumaatMubarak #جمعة_مباركة #HariJumaat #WizzSmartServices #Malaysia")
    open(f"{out}/caption.txt", "w").write(cap)
    print(f"verse: {v['ref_en']} · prayer {DATA['prayers'].index(d) + 1} · theme {c['name']}")
    if bad: raise SystemExit("Too much text: " + "; ".join(bad) + ". Report it; do not edit the verse.")

if __name__ == "__main__":
    day = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else (dt.datetime.utcnow() + dt.timedelta(hours=8)).date()
    out = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else f"{D}/out/jumuah-{day}")
    asyncio.run(main(day, out))
