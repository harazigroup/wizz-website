// Local-currency pricing. Base prices are USD (catalog.json). Rates checked 4 Oct 2026; update RATES occasionally.
// Rule: local = USD x rate x (1 + BUFFER), rounded up to a clean price. USD is never converted.
export const BUFFER = 0.02; // covers card-network FX and small rate moves
export const RATES = {
  USD: { rate: 1, step: 1, nine: false },
  GBP: { rate: 0.7564, step: 10, nine: true },
  EUR: { rate: 0.8888, step: 10, nine: true },
  CAD: { rate: 1.4239, step: 10, nine: true },
  AUD: { rate: 1.4397, step: 10, nine: true },
  SGD: { rate: 1.2794, step: 10, nine: true },
  AED: { rate: 3.6725, step: 10, nine: false },
  SAR: { rate: 3.75, step: 10, nine: false },
  QAR: { rate: 3.64, step: 10, nine: false },
  MYR: { rate: 4.0842, step: 10, nine: false },
  THB: { rate: 33.5643, step: 100, nine: false }
};
const EURO = "AT BE CY DE EE ES FI FR GR HR IE IT LT LU LV MT NL PT SI SK".split(" ");
const BY_COUNTRY = { GB: "GBP", CA: "CAD", AU: "AUD", SG: "SGD", AE: "AED", SA: "SAR", QA: "QAR", MY: "MYR", TH: "THB" };

export function currencyFor(country) {
  const c = (country || "").toUpperCase();
  if (EURO.includes(c)) return "EUR";
  return BY_COUNTRY[c] || "USD";
}

export function localPrice(usd, cur) {
  const r = RATES[cur] || RATES.USD;
  if (cur === "USD" || !RATES[cur]) return usd;
  const raw = usd * r.rate * (1 + BUFFER);
  const up = Math.ceil(raw / r.step) * r.step;
  return r.nine ? up - 1 : up;
}
