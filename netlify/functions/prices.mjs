// GET [?currency=XXX] -> which currency to show this visitor, plus the rate table the page uses to display prices.
import { BUFFER, RATES, currencyFor } from "./_fx.mjs";

export default async (req, context) => {
  const want = (new URL(req.url).searchParams.get("currency") || "").toUpperCase();
  const country = context?.geo?.country?.code || "";
  const currency = RATES[want] ? want : currencyFor(country);
  return new Response(JSON.stringify({ country, currency, buffer: BUFFER, rates: RATES }), {
    headers: { "content-type": "application/json", "cache-control": "private, max-age=300" }
  });
};
