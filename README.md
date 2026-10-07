# wizz.com.my

Static website for Wizz Smart Services Sdn. Bhd., hosted on Netlify.

- Pages: plain HTML at the repo root (`index.html`, `packages.html`, …), styles in `site.css`, scripts in `site.js`, `fx.js`, `globe.js`.
- Payments: Stripe Checkout when `STRIPE_SECRET_KEY` is set, otherwise Airwallex Hosted Payment Page.
  - `netlify/functions/checkout.mjs` creates a PaymentIntent (price taken from `netlify/functions/catalog.json`, never from the browser).
  - `netlify/functions/verify.mjs` confirms the payment on `thank-you.html`, which then shows the onboarding form (Netlify Forms, form name `onboarding`).
- Netlify environment variables:
  - `STRIPE_SECRET_KEY` (secret; restricted key with Checkout Sessions: Write), or
  - `AIRWALLEX_CLIENT_ID`, `AIRWALLEX_API_KEY` (secret)
  - `AIRWALLEX_ENV` = `demo` for sandbox, `prod` for live
  - `SITE_URL` = `https://wizz.com.my`
- Prices: edit `tools/catalog.py`, run `python3 tools/build_pkgs.py` from `tools/` (it regenerates `packages.html`), and update `netlify/functions/catalog.json` to match.
- Local currency: prices are set in USD. `netlify/functions/prices.mjs` picks the visitor's currency from their country (Netlify geolocation) and the page converts with the same formula checkout uses (`netlify/functions/_fx.mjs`: USD × rate × 1.02, rounded up; GBP/EUR/CAD/AUD/SGD end in 9). Supported: USD, GBP, EUR, CAD, AUD, SGD, AED, SAR, QAR, MYR, THB; everything else falls back to USD. Visitors can switch currency; the choice is remembered. Update the rates in `_fx.mjs` every month or two, or when a currency moves a lot.

## Client accounts (Supabase project "Wizz Smart Services", Frankfurt)
- `account.html` + `account.js`: clients sign in with an email link, see their orders and status, upload documents, download what the team uploads.
- `admin.html` + `admin.js`: team page. Access is limited to emails in the `admins` table (add one in Supabase: Table editor → admins → insert row, lowercase email).
- Paid orders are saved by `netlify/functions/verify.mjs` when the Thank-you page loads; the onboarding form is saved by `onboarding.mjs`. Both call database functions guarded by `WIZZ_DB_SECRET` (Netlify env, functions scope).
- Files live in the private `docs` storage bucket under `<order id>/client/` or `<order id>/team/`. Row-level security limits every table and file to the client's own email or a team admin.
- Edit the page scripts in `tools/portal/`; the build copies them to the site root.
