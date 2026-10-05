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
