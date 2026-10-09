# Single source of truth for packages. Prices in USD (major units). Edit here, then run build_pkgs.py.
# A tier can also have a fixed local price, fix={"MYR": 18000}: visitors paying in that currency see and pay exactly that;
# everyone else sees it converted from p (USD), which fx() works out from the same rates the site uses.
import re as _re, math as _math, os as _os
_FX = open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "netlify", "functions", "_fx.mjs")).read()
RATES = {m[0]: float(m[1]) for m in _re.findall(r"([A-Z]{3}): \{ rate: ([0-9.]+)", _FX)}
def fx(cur, amount):
    """USD base price for a price set in another currency (rounded up, with the same 2% buffer)."""
    return _math.ceil(amount / RATES[cur] * 1.02)
COUNTRIES = [
 dict(c="US", n="United States", g="North America", e="LLC in Wyoming or New Mexico (Delaware on request). Owned 100% by non-residents.",
  tiers=[
   dict(sku="us-starter", n="Starter", p=289, buy=True, i=["State filing fee included","Articles of organization & operating agreement","EIN application for non-residents","Registered agent, 12 months","Digital document pack"]),
   dict(sku="us-business", n="Business", p=1899, buy=True, pop=True, plus="Everything in Starter, plus", i=["US business mailing address, 12 months","Business account application support (one provider)","Amazon / Shopify readiness call"]),
   dict(sku="us-complete", n="Complete", p=2899, buy=True, plus="Everything in Business, plus", i=["First-year Form 5472 + pro-forma 1120 filing","State annual report filing","Compliance calendar & reminders"])],
  notes=["Delaware: add $100. Delaware charges a $400 yearly tax from 2026.","Yearly renewal from $499 (registered agent + annual report)."]),
 dict(c="UK", n="United Kingdom", g="Europe", e="Private limited company (Ltd) at Companies House. No UK-resident director needed.",
  tiers=[
   dict(sku="uk-starter", n="Starter", p=299, buy=True, i=["Companies House fee (£100) included","Director identity verification","Registered office address, 12 months","Share certificates & digital documents"]),
   dict(sku="uk-business", n="Business", p=599, buy=True, pop=True, plus="Everything in Starter, plus", i=["Director service address, 12 months","HMRC Corporation Tax (UTR) registration","Business account application support","VAT registration if needed"]),
   dict(sku="uk-complete", n="Complete", p=1290, buy=True, plus="Everything in Business, plus", i=["First-year accounts via our accountant partner","Confirmation statement filing (£50 fee included)"]),
   dict(sku="uk-addr-ro-da", grp="uk-addr", n="Registered office + director's address", p=fx("GBP", 34.99), fix={"GBP": 34.99}, buy=True, i=["Registered office address in London","Director's service address","12 months"]),
   dict(sku="uk-addr-ba-ro", grp="uk-addr", n="Business address + registered office", p=fx("GBP", 94.49), fix={"GBP": 94.49}, buy=True, i=["Virtual business address in London, with mail handling","Registered office address","12 months"]),
   dict(sku="uk-addr-ba-ro-da", grp="uk-addr", n="Business address + registered office + director's address", p=fx("GBP", 100.09), fix={"GBP": 100.09}, buy=True, pop=True, i=["Virtual business address in London, with mail handling","Registered office address","Director's service address","12 months"]),
   dict(sku="uk-addr-ba-call", grp="uk-addr", n="Business address + call answering", p=fx("GBP", 220.50), fix={"GBP": 220.50}, buy=True, i=["Virtual business address in London, with mail handling","Call answering service in your company name","12 months"]),
   dict(sku="uk-addr-all", grp="uk-addr", n="All-in-one London office", p=fx("GBP", 250.60), fix={"GBP": 250.60}, buy=True, i=["Virtual business address in London, with mail handling","Registered office address","Director's service address","Call answering service in your company name","12 months"])],
  groups={"uk-addr": ("London address plans", "Registered office, director's address, business address and call answering for your UK company, for 12 months. Prices are set in pounds sterling.")},
  notes=["Yearly renewal from $449 (registered office + confirmation statement).","Address services need identity checks under UK anti-money-laundering rules before they start."]),
 dict(c="CA", n="Canada", g="North America", e="Ontario or BC corporation. No resident-director rule in either province.",
  tiers=[
   dict(sku="ca-starter", n="Starter", p=749, buy=True, i=["Government fees & NUANS name search included","Articles & bylaws","Business Number (BN) registration","Digital minute book"]),
   dict(sku="ca-business", n="Business", p=1190, buy=True, pop=True, plus="Everything in Starter, plus", i=["Registered office address, 12 months","GST/HST registration","Business account application support","Amazon.ca readiness call"])],
  notes=["Federal corporation available on request (25% of directors must be Canadian residents)."]),
 dict(c="EE", n="Estonia", g="Europe", e="Private limited company (OÜ), run fully online with e-Residency.",
  tiers=[
   dict(sku="ee-starter", n="Starter", p=749, buy=True, i=["State fee (€265) included","Articles of association","Legal address & contact person, 12 months","Registration guidance for e-Residency holders"]),
   dict(sku="ee-business", n="Business", p=fx("MYR", 7500), fix={"MYR": 7500}, buy=True, pop=True, plus="Everything in Starter, plus", i=["VAT registration if needed","Business account (EMI) application support","Accounting partner introduction"]),
   dict(sku="ee-eresidency", n="e-Residency card", p=fx("EUR", 250), fix={"EUR": 250}, buy=True, i=["We prepare and submit your e-Residency application","Government card fee included","Collect your card at an Estonian embassy or pick-up point you choose"])],
  notes=["e-Residency is a digital ID for running an Estonian company online. It is not a visa or residence permit, and the Estonian Police and Border Guard Board decides each application."]),
 dict(c="PL", n="Poland", g="Europe", e="Limited liability company (sp. z o.o.) via the S24 online system.",
  tiers=[
   dict(sku=None, n="Standard", p=1690, frm=True, i=["Court & publication fees included","KRS registration via S24","Tax ID & VAT registration","Virtual office, 12 months"]),
   dict(sku=None, n="Full setup", p=2490, frm=True, pop=True, plus="Everything in Standard, plus", i=["Qualified e-signature setup","Sworn translations","Business bank account support"])],
  notes=["Minimum share capital of PLN 5,000 is paid into your company and stays your money; it isn't included in the price.","Accounting is mandatory in Poland and quoted separately."]),
 dict(c="FR", n="France", g="Europe", e="Simplified joint-stock company (SAS/SASU). Minimum capital €1.",
  tiers=[
   dict(sku="fr-starter", n="Starter", p=849, buy=True, i=["Articles (statuts) drafted","Legal notice publication included","Guichet unique filing & registration","Registered address (domiciliation), 12 months"]),
   dict(sku="fr-business", n="Business", p=1390, buy=True, pop=True, plus="Everything in Starter, plus", i=["Capital deposit & bank account support","EU VAT number registration","Cdiscount / Octopia seller readiness"])],
  notes=["A non-EU manager may need a French residence permit to run day-to-day operations in France."]),
 dict(c="NL", n="Netherlands", g="Europe", e="Private limited company (BV) set up through a Dutch notary. Run it fully from abroad.",
  tiers=[
   dict(sku="nl-starter", n="Starter", p=2490, buy=True, i=["Notary deed & articles of association","Chamber of Commerce (KVK) registration fee included","Shareholder register & UBO registration","Dutch business address, 12 months","Remote signing by power of attorney"]),
   dict(sku="nl-business", n="Business", p=3490, buy=True, pop=True, plus="Everything in Starter, plus", i=["VAT number & EORI registration","Business account (EMI) application support","Amazon EU / Bol.com readiness call","Accounting partner introduction"])],
  notes=["Passport copies must be certified with an apostille for the notary; we arrange this at cost.","Bookkeeping, VAT returns and annual accounts are yearly obligations, quoted separately."]),
 dict(c="AE", n="UAE", g="Middle East", e="Free zone company (fastest) or mainland LLC (trade anywhere in the UAE).",
  tiers=[
   dict(sku="ae-deposit", n="Free zone, no visa", p=2490, frm=True, deposit=500, i=["Licence in a cost-effective free zone","Company documents & registration","Bank account application support"]),
   dict(sku="ae-deposit-visa", n="Free zone + 1 visa", p=4990, frm=True, deposit=500, pop=True, plus="Everything in no-visa, plus", i=["One investor/employee visa","Emirates ID & medical coordination","Corporate tax registration"]),
   dict(sku=None, n="Mainland LLC", p=None, i=["Licence, office and approvals","Quoted after a short call"])],
  notes=["Pay a deposit of $500 online. It's credited to your package; the final price depends on the free zone and activity.","Licences renew yearly at roughly the first-year cost."]),
 dict(c="SA", n="Saudi Arabia", g="Middle East", e="LLC with an investment licence (MISA) for foreign owners.",
  tiers=[
   dict(sku="sa-assessment", n="Market-entry assessment", p=fx("MYR", 500), fix={"MYR": 500}, buy=True, i=["Activity & licence route review","Capital and Saudization overview","Written plan and quote","Credited if you go ahead"]),
   dict(sku=None, n="Company setup", p=fx("MYR", 12000), fix={"MYR": 12000}, frm=True, pop=True, i=["Investment licence & commercial registration","Chamber & municipality registrations","Bank account support","Government fees and capital not included"])],
  notes=["Setup usually takes 3–6 weeks. Work permits and expat levies are separate."]),
 dict(c="OM", n="Oman", g="Middle East", e="LLC with 100% foreign ownership for most activities.",
  tiers=[
   dict(sku=None, n="Company setup", p=fx("MYR", 3500), fix={"MYR": 3500}, frm=True, i=["Commercial registration","Activity licences","Company documents","Chamber of commerce registration"]),
   dict(sku=None, n="Setup + investor visa", p=fx("MYR", 7500), fix={"MYR": 7500}, frm=True, pop=True, plus="Everything in setup, plus", i=["Investor residence visa, valid 2 years","Bank account support"])],
  notes=["Office space, when your activity requires it, is quoted separately."]),
 dict(c="MY", n="Malaysia", g="Asia", e="Private limited company (Sdn. Bhd.) at SSM. Our home base.",
  tiers=[
   dict(sku="my-starter", n="Starter", p=990, buy=True, i=["SSM incorporation fee included","Company secretary, 12 months","Registered address, 12 months","Constitution & company documents"]),
   dict(sku="my-business", n="Business", p=1790, buy=True, pop=True, plus="Everything in Starter, plus", i=["Bank account application support","Shopee / Lazada / TikTok Shop setup call","SST & licence check"])],
  notes=["A foreign-owned Sdn Bhd needs at least one director resident in Malaysia. If you don't have one, we quote a resident director service separately.","Audit and tax filing are yearly obligations, quoted separately."]),
 dict(c="TH", n="Thailand", g="Asia", e="Thai limited company. Foreign ownership limits apply to many activities.",
  tiers=[
   dict(sku=None, n="Company setup", p=1490, frm=True, i=["Ownership & activity review","Government registration fees included","Company documents & tax ID"]),
   dict(sku=None, n="Setup + compliance", p=2490, frm=True, pop=True, plus="Everything in setup, plus", i=["VAT registration","Accounting partner setup","Bank account support"]),
   dict(sku=None, n="Work permit, 2 years", p=fx("MYR", 18000), fix={"MYR": 18000}, i=["Work permit and visa for 2 years","Sponsored by our Thai company: you're employed under it, so you don't need your own Thai company or capital","Eligibility check first","Application & visa coordination"])],
  notes=["The work permit lets you work only in the role and for the employer named on it. The Thai authorities decide every application.","If you set up your own Thai company instead, each foreign work permit generally needs THB 2M paid-up capital and 4 Thai employees (BOI companies differ).","BOI promotion and Foreign Business Licence are quoted separately."]),
 dict(c="PK", n="Pakistan", g="Asia", e="Private limited company at SECP.",
  tiers=[
   dict(sku=None, n="Starter", p=790, frm=True, i=["Name reservation & incorporation","Tax number (NTN) registration","Company documents"]),
   dict(sku=None, n="Business", p=1390, frm=True, pop=True, plus="Everything in Starter, plus", i=["Security clearance filing for foreign shareholders","Bank account support","Chamber registration"])],
  notes=["Foreign directors and shareholders need security clearance, which can take 8–14 weeks."]),
]
ADDONS = [("Amazon seller account application support","$299"),("Marketplace onboarding: Noon, TikTok Shop, Shopee and others","$249 each"),("Shopify store setup","from $490"),("Business bank or payment account application (per provider)","$199"),("Amazon FBA prep from Malaysia","quote"),("Document attestation / apostille","quote")]

# Add-ons that can be bought online (label must match ADDONS above). Prices in USD per unit.
ADDON_SKUS = {
 "Amazon seller account application support": ("addon-amazon", 299),
 "Marketplace onboarding: Noon, TikTok Shop, Shopee and others": ("addon-marketplace", 249),
 "Business bank or payment account application (per provider)": ("addon-bank", 199),
}
