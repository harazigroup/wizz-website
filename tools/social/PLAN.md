# Wizz social content playbook

Used by the weekly content task. Every Sunday it prepares the next week's posts for TikTok and Instagram (@wizz.com.my).

## Rules (always)
- **English only** on TikTok and Instagram.
- Carousels are rendered with `tools/social/carousel.py`: 1080×1920, 5–7 slides, cover + 3–5 content slides + CTA slide.
  The renderer enforces TikTok's safe area. If it fails, shorten the copy. Never shrink the type.
- Alternate light and dark covers across the week so the profile grid stays checkerboard (light, dark, light…).
- One idea per carousel. Short lines. Facts must match the website (prices, timelines, what is included).
- Prices come from the website catalogue (`tools/catalog.py`). Show ringgit first for packages that are set in ringgit.
- **Compliance, every post:**
  - Never promise or imply guaranteed bank accounts, Stripe, Wise, Payoneer, marketplace accounts, licences, visas, residency, tax savings or business success.
  - Say clearly that approvals are decided by banks, providers, platforms or authorities.
  - Forming a company does not give a visa or residency. Say so when the topic touches immigration.
  - No legal or tax advice. Refer to a qualified professional for personal tax questions.
  - No fake reviews, testimonials, client names or "was" prices.
- **Advertiser identity (TikTok ad review):** every cover names the service sold in plain words (`"offer"`, e.g. "US LLC formation service · from RM 1,199").
  The renderer prints "Wizz Smart Services" next to the logo and "by Wizz Smart Services Sdn. Bhd., Malaysia" under the offer.
  Covers that are only a question ("US LLC or UK Ltd?") were rejected in Malaysia for "Financial Misrepresentation" (Oct 2026).
- **Captions:** short, under 500 characters (Instagram can't share longer captions to Threads). Hook line, link, WhatsApp, 5–8 hashtags. Don't repeat what the slides already say.
- CTA slide: `wizz.com.my/<page>` + `WhatsApp +60 11-2447 7685`, with one line of fine print.

## Posting routine (Monday, Wednesday, Friday at 08:47 MYT)
On each posting day one topic becomes:
1. A **blog article** in English, Arabic and Malay, added with `python3 tools/new_post.py post.json` (rebuilds the site; push to deploy).
2. A **carousel** (5–7 slides) built from the same article, ending with a CTA to the article or the matching package page.
3. **Captions** for Instagram and TikTok.
4. If a Postiz key is saved (admin page → Settings), the carousel is **scheduled** on Instagram and TikTok for 20:30 Malaysia time.
   Otherwise the slides and captions are sent to the owner to post by hand.
On Fridays, also write 2 talking-video scripts for Arkan for the coming week (30–60 s each).

Posting times (Malaysia time, GMT+8): 20:30 by default; 12:00–13:00 also works. Gulf audience: 21:00–23:00 MYT.

## Backlog (take the next unused topics, then mark them used with the date)
1. US LLC vs UK Ltd: which fits your business? (blog: blog-llc-or-ltd.html)
2. 3 reasons Stripe or a bank rejects a new company, and how to prepare (blog-payment-approval.html)
3. Own brand or reseller? What to sort out before selling on Amazon (blog-own-brand-or-reseller.html)
4. What RM 1,199 gets you: the US Starter package explained (usa.html)
5. Estonia e-Residency: what it is and what it isn't (not a visa)
6. Saudi company setup in 2 stages: foreign company first, then MISA licence (saudi-investment.html)
7. UAE free zone or mainland: how to choose
8. Selling on Noon, Shopee, Lazada and TikTok Shop with the right company
9. Amazon FBA prep from Malaysia: how it works, step by step
10. Myths: "A US company gives me a US visa" and 4 more
11. What documents you need to open a company abroad (passport, full residential address, national ID number…)
12. Marketplace onboarding from RM 300 per platform: what we prepare
13. Thailand work permit through our Thai company: how it works and what the authorities decide
14. Oman: company setup or setup with a 2-year investor visa
15. UK London address plans: registered office, director's address, business address, call answering
16. Yearly duties after you form a company (US, UK): what you must file

## Used topics
- 2026-10-12 · UK company without living in the UK (posted)
- 2026-10-12 · US LLC from anywhere (posted)
- 2026-10-13 · Established company for Saudi investment (posted)
- 2026-10-11 · Digital banking (posted)
- 2026-10-13 · Topic 1, US LLC vs UK Ltd (carousel prepared, not yet posted; blog already existed)
- 2026-10-13 · Topic 7, UAE free zone or mainland (blog published)
- 2026-10-14 · Topic 4, What RM 1,199 gets you: the US Starter package explained (blog + carousel, light cover, sent for manual posting)
- 2026-10-14 · Malaysia Budget 2027 for companies (blog published, extra post; carousel + story, dark cover, sent for manual posting)
- 2026-10-15 · Adding a partner to a US LLC (blog published, extra post)
