#!/usr/bin/env python3
"""Wizz TikTok/Instagram carousel renderer (1080x1920, English only).

Usage:  python3 tools/social/carousel.py spec.json out_dir
Setup once: cd tools/social && npm install   (fonts)   ·   Playwright with Chromium must be available.

Every slide keeps TikTok's safe area clear: 300px top (search bar), ~560px bottom (caption, buttons),
140px left and 200px right (side crop on tall phones, like/share buttons). The script fails if text runs
into the bottom zone, so shorten the copy rather than shrinking the type.

spec.json:
{ "name": "wizz-us-llc",
  "slides": [
    {"kind":"cover","theme":"light","eyebrow":"US LLC · 2026","title":"Start a US company <r>from anywhere.</r>","lede":"..."},
    {"kind":"list","title":"No US visit. <r>No SSN.</r>","items":["...","..."],"note":"optional"},
    {"kind":"cards","title":"Pick your state.","cards":[{"tag":"WY","title":"Wyoming","text":"..."}],"note":"optional","tight":false},
    {"kind":"cta","title":"Start your US LLC <r>with Wizz.</r>","lede":"...","buttons":["wizz.com.my/usa","WhatsApp +60 11-2447 7685"],"fine":"..."}
  ] }
<r>…</r> marks red words. Content slides are numbered 01, 02… automatically. CTA slides are dark by default.
"""
import asyncio, html, json, os, re, sys
from playwright.async_api import async_playwright

D = os.path.dirname(os.path.abspath(__file__))
F = D + "/node_modules/@fontsource"
LOGO = open(D + "/logo_inner.svg").read()
CSS = f"""
@font-face{{font-family:Archivo;src:url('file://{F}-variable/archivo/files/archivo-latin-wdth-normal.woff2');font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:Plex;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2');font-weight:400}}
@font-face{{font-family:Plex;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}}
@font-face{{font-family:PlexMono;src:url('file://{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2');font-weight:600}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:Plex,sans-serif}}
.s{{width:1080px;height:1920px;padding:300px 200px 0 140px;position:relative;display:flex;flex-direction:column}}
.dark{{background:#1F2328;color:#fff}} .light{{background:#F3F5F7;color:#1F2328}}
.top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:56px}}
.logo{{height:64px}} .dark .logo{{color:#fff}} .light .logo{{color:#1F2328}}
.n{{font:600 30px PlexMono;letter-spacing:.08em;opacity:.6}}
.eb{{font:600 32px PlexMono;letter-spacing:.14em;text-transform:uppercase;color:#E01B22;margin-bottom:34px;display:flex;align-items:center;gap:18px}}
.eb:before{{content:"";width:18px;height:18px;border-radius:50%;background:#E01B22}}
h1{{font-family:Archivo;font-weight:850;font-stretch:88%;font-size:96px;line-height:1;letter-spacing:-.02em}}
h2{{font-family:Archivo;font-weight:850;font-stretch:88%;font-size:74px;line-height:1.02;letter-spacing:-.015em;margin-bottom:30px}}
.red{{color:#E01B22}}
.bign{{font:600 104px PlexMono;color:#E01B22;line-height:1;margin-bottom:10px}}
p.lede{{font-size:36px;line-height:1.38;margin-top:34px;opacity:.85}}
.cards{{display:flex;flex-direction:column;gap:26px}}
.card{{border-radius:24px;padding:28px 32px;display:flex;gap:30px;align-items:flex-start}}
.dark .card{{background:#2A3037}} .light .card{{background:#fff;border:2px solid #DDE2E7}}
.tight{{gap:18px}} .tight .card{{padding:20px 30px}}
.card b{{display:block;font-size:37px;font-weight:600;margin-bottom:8px;line-height:1.2}}
.card span{{font-size:31px;line-height:1.4;opacity:.78}}
.num{{flex:none;min-width:64px;padding:0 10px;height:64px;border-radius:50%;background:#E01B22;color:#fff;font:600 30px PlexMono;display:grid;place-items:center;margin-top:4px}}
.ck{{flex:none;width:56px;height:56px;border-radius:50%;display:grid;place-items:center;margin-top:2px}}
.dark .ck{{background:#fff;color:#1F2328}} .light .ck{{background:#1F2328;color:#fff}}
.ck svg{{width:32px}}
.li{{display:flex;gap:28px;align-items:flex-start;font-size:37px;line-height:1.32;padding:18px 0;border-bottom:2px dashed rgba(127,127,127,.35)}}
.li:last-child{{border-bottom:0}}
.note{{margin-top:32px;font-size:30px;line-height:1.45;opacity:.7}}
.swipe{{position:absolute;left:140px;bottom:560px;font:600 34px PlexMono;letter-spacing:.1em;display:flex;align-items:center;gap:20px}}
.swipe i{{font-style:normal;background:#E01B22;color:#fff;border-radius:99px;padding:14px 26px}}
.cta{{margin-top:36px;display:flex;flex-direction:column;gap:16px}}
.btn{{background:#E01B22;color:#fff;border-radius:22px;padding:28px 34px;font-size:36px;font-weight:600;display:flex;justify-content:space-between}}
.btn.o{{background:transparent;border:3px solid currentColor}}
.fine{{margin-top:24px;font-size:25px;line-height:1.45;opacity:.6}}
"""
CHK = '<svg viewBox="0 0 20 20"><path d="M5 10.5l3.2 3L15 6.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SAFE_BOTTOM = 1380  # px; below this TikTok's caption and buttons cover the image

def rich(t):  # escape, then allow <r>…</r> for red words
    return re.sub(r"&lt;r&gt;(.*?)&lt;/r&gt;", r'<span class="red">\1</span>', html.escape(t))

def slide_html(s, i, n, k):
    top = f'<div class="top"><svg class="logo" viewBox="330 428 420 204">{LOGO}</svg><span class="n">{i:02d} / {n:02d}</span></div>'
    kind = s["kind"]
    if kind == "cover":
        return top + (f'<div class="eb">{rich(s["eyebrow"])}</div>' if s.get("eyebrow") else "") + f'<h1>{rich(s["title"])}</h1>' + \
               (f'<p class="lede">{rich(s["lede"])}</p>' if s.get("lede") else "") + '<div class="swipe"><i>Swipe</i> →</div>'
    if kind == "cta":
        btns = "".join(f'<div class="btn{" o" if j else ""}">{rich(b)} <span>→</span></div>' for j, b in enumerate(s.get("buttons", [])))
        return top + f'<div class="eb">{rich(s.get("eyebrow", "Wizz Smart Services"))}</div><h1>{rich(s["title"])}</h1>' + \
               (f'<p class="lede">{rich(s["lede"])}</p>' if s.get("lede") else "") + f'<div class="cta">{btns}</div>' + \
               (f'<p class="fine">{rich(s["fine"])}</p>' if s.get("fine") else "")
    body = f'<div class="bign">{k:02d}</div><h2>{rich(s["title"])}</h2>'
    if kind == "list":
        body += "".join(f'<div class="li"><span class="ck">{CHK}</span><div>{rich(x)}</div></div>' for x in s["items"])
    elif kind == "cards":
        body += f'<div class="cards{" tight" if s.get("tight") or len(s["cards"]) > 3 else ""}">' + "".join(
            f'<div class="card"><span class="num">{html.escape(c.get("tag", str(j + 1)))}</span><div><b>{rich(c["title"])}</b>' +
            (f'<span>{rich(c["text"])}</span>' if c.get("text") else "") + '</div></div>' for j, c in enumerate(s["cards"])) + '</div>'
    else:
        raise SystemExit(f"unknown slide kind: {kind}")
    if s.get("note"): body += f'<p class="note">{rich(s["note"])}</p>'
    return top + body

async def main(spec_path, out):
    spec = json.load(open(spec_path))
    os.makedirs(out, exist_ok=True)
    slides, n, k, bad = spec["slides"], len(spec["slides"]), 0, []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(slides, 1):
            if s["kind"] in ("list", "cards"): k += 1
            theme = s.get("theme") or ("dark" if s["kind"] == "cta" else "light")
            doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s {theme}">{slide_html(s, i, n, k)}</div></body></html>'
            path = f"{out}/.slide.html"; open(path, "w").write(doc)
            await pg.goto("file://" + path); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(150)
            low = await pg.evaluate("Math.max(...[...document.querySelectorAll('.s > *:not(.swipe)')].map(e=>e.getBoundingClientRect().bottom))")
            wide = await pg.evaluate("[...document.querySelectorAll('.s *')].some(e=>e.getBoundingClientRect().right>1080-150)")
            f = f'{out}/{spec["name"]}-{i:02d}.png'
            await pg.screenshot(path=f)
            if low > SAFE_BOTTOM: bad.append(f"slide {i}: text reaches {int(low)}px (limit {SAFE_BOTTOM}), shorten it")
            if wide: bad.append(f"slide {i}: text too close to the right edge")
            print(f, "ok" if low <= SAFE_BOTTOM and not wide else "CHECK")
        os.remove(f"{out}/.slide.html")
        await b.close()
    if bad: raise SystemExit("Safe-area problems:\n  " + "\n  ".join(bad))

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
