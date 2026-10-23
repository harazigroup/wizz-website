#!/usr/bin/env python3
"""Wizz business cards: print-ready PDF (90 x 54 mm trim, 3 mm bleed, front + back per person) and PNG previews.

Usage:  python3 tools/print/cards.py people.json out_dir
people.json: [{"name": "Full Name", "title": "Job title", "phone": "+60 11-2447 7685", "email": "info@wizz.com.my"}, ...]
phone/email are optional and default to the company WhatsApp and info@wizz.com.my. The QR opens the website (https://wizz.com.my); add "qr": "whatsapp" to make it open a WhatsApp chat with that phone instead.
Fonts and logo come from tools/social (npm install there once). Needs Playwright with Chromium and `pip install segno`.
"""
import asyncio, html, json, os, re, sys
import segno
from playwright.async_api import async_playwright

D = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.join(os.path.dirname(D), "social")
F = SOC + "/node_modules/@fontsource"
LOGO = open(SOC + "/logo_inner.svg").read()
CO_PHONE, CO_EMAIL = "+60 11-2447 7685", "info@wizz.com.my"
INK, PAPER, RED, MUTED = "#1F2328", "#F6F7F8", "#E01B22", "#5E6670"

CSS = f"""
@font-face{{font-family:Archivo;src:url('file://{F}-variable/archivo/files/archivo-latin-wdth-normal.woff2');font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:Plex;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2');font-weight:400}}
@font-face{{font-family:Plex;src:url('file://{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}}
@font-face{{font-family:PlexMono;src:url('file://{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2');font-weight:600}}
@page{{size:96mm 60mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.card{{width:96mm;height:60mm;position:relative;overflow:hidden;page-break-after:always;font-family:Plex,sans-serif}}
/* the safe area: 3 mm bleed + 4 mm inside the trim */
.safe{{position:absolute;left:7mm;top:7mm;right:7mm;bottom:7mm}}
.front{{background:{INK};color:#fff}}
.front .bar{{position:absolute;right:0;top:0;bottom:0;width:21mm;background:linear-gradient(160deg,#2A3037 0%,{INK} 75%)}}
.front .bar i{{position:absolute;left:0;top:0;bottom:0;width:1.1mm;background:{RED}}}
.front .logo{{width:24mm;color:#fff;display:block}}
.front h1{{position:absolute;left:0;bottom:7.5mm;width:58mm;font:850 15.5pt/1.02 Archivo;font-stretch:90%;letter-spacing:-.01em}}
.front h1 b{{color:#FF3A40}}
.front p{{position:absolute;left:0;bottom:0;font:600 5pt PlexMono;letter-spacing:.09em;text-transform:uppercase;color:#B7BEC6}}
.back{{background:{PAPER};color:{INK}}}
.back .top{{position:absolute;left:0;top:0;right:22mm}}
.back h2{{font:800 12.5pt/1.05 Archivo;font-stretch:95%;letter-spacing:-.005em}}
.back .role{{margin-top:1.2mm;font:600 6.6pt Plex;color:{RED};letter-spacing:.02em}}
.back ul{{list-style:none;position:absolute;left:0;bottom:8.6mm;display:grid;gap:1.05mm}}
.back li{{display:flex;gap:2.2mm;align-items:baseline;font:400 7pt Plex}}
.back li span{{font:600 5.2pt PlexMono;letter-spacing:.1em;color:{MUTED};width:5.5mm}}
.back .addr{{position:absolute;left:0;bottom:0;right:0;font:400 5.3pt/1.35 Plex;color:{MUTED};border-top:.25mm solid #D9DEE3;padding-top:1.3mm}}
.back .qr{{position:absolute;right:0;top:0;width:17mm;text-align:center}}
.back .qr svg{{width:17mm;height:17mm;display:block}}
.back .qr small{{display:block;margin-top:.8mm;font:600 4.6pt PlexMono;letter-spacing:.08em;text-transform:uppercase;color:{MUTED}}}
.back .edge{{position:absolute;left:0;top:0;bottom:0;width:4.6mm;background:{RED}}}
"""

def front():
    return f'''<section class="card front"><div class="bar"><i></i></div><div class="safe">
<svg class="logo" viewBox="330 428 420 204">{LOGO}</svg>
<h1>Build your business beyond borders<b>.</b></h1>
<p>Formation · Banking · Marketplaces · Logistics</p></div></section>'''

def back(p):
    e = html.escape
    phone = p.get("phone") or CO_PHONE
    email = p.get("email") or CO_EMAIL
    wa = p.get("qr") == "whatsapp"
    target = f"https://wa.me/{re.sub(r'[^0-9]', '', phone)}" if wa else "https://wizz.com.my"
    qr = segno.make(target, error="m").svg_inline(border=0, dark=INK, omitsize=True)
    return f'''<section class="card back"><div class="edge"></div><div class="safe">
<div class="top"><h2>{e(p["name"])}</h2><p class="role">{e(p["title"])}</p></div>
<div class="qr">{qr}<small>{"WhatsApp" if wa else "Website"}</small></div>
<ul><li><span>TEL</span>{e(phone)}</li><li><span>MAIL</span>{e(email)}</li><li><span>WEB</span>wizz.com.my</li></ul>
<p class="addr">WIZZ SMART SERVICES SDN. BHD. (202501029005)<br>B2-2-3, Publika, Solaris Dutamas, 50480 Kuala Lumpur, Malaysia</p>
</div></section>'''

async def main(people_path, out):
    people = json.load(open(people_path)); out = os.path.abspath(out); os.makedirs(out, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for p in people:
            slug = re.sub(r"[^a-z0-9]+", "-", p["name"].lower()).strip("-") or "card"
            doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{front()}{back(p)}</body></html>'
            path = f"{out}/.{slug}.html"; open(path, "w").write(doc)
            pg = await b.new_page()
            await pg.goto("file://" + path); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            await pg.pdf(path=f"{out}/wizz-card-{slug}.pdf", width="96mm", height="60mm", print_background=True, prefer_css_page_size=True)
            # previews at the trim size (bleed cropped), 2x for sharpness
            prev = await b.new_page(viewport={"width": 363, "height": 227}, device_scale_factor=3)
            await prev.goto("file://" + path); await prev.evaluate("document.fonts.ready"); await prev.wait_for_timeout(200)
            for i, side in enumerate(("front", "back")):
                el = (await prev.query_selector_all(".card"))[i]
                bb = await el.bounding_box()
                bleed = bb["width"] * 3 / 96
                await prev.screenshot(path=f"{out}/preview-{slug}-{side}.png", clip={"x": bb["x"] + bleed, "y": bb["y"] + bleed, "width": bb["width"] - 2 * bleed, "height": bb["height"] - 2 * bleed}, full_page=True)
            os.remove(path); await pg.close(); await prev.close()
            print("ok", slug)
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
