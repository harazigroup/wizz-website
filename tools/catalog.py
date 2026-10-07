# Single source of truth for packages. Prices in USD (major units). Edit here, then run build_pkgs.py.
COUNTRIES = [
 dict(c="US", n="United States", g="North America", e="LLC in Wyoming or New Mexico (Delaware on request). Owned 100% by non-residents.",
  tiers=[
   dict(sku="us-starter", n="Starter", p=349, buy=True, i=["State filing fee included","Articles of organization & operating agreement","EIN application for non-residents","Registered agent, 12 months","Digital document pack"]),
   dict(sku="us-business", n="Business", p=649, buy=True, pop=True, plus="Everything in Starter, plus", i=["US business mailing address, 12 months","Business account application support (one provider)","Amazon / Shopify readiness call"]),
   dict(sku="us-complete", n="Complete", p=1190, buy=True, plus="Everything in Business, plus", i=["First-year Form 5472 + pro-forma 1120 filing","State annual report filing","Compliance calendar & reminders"])],
  notes=["Delaware: add $100. Delaware charges a $400 yearly tax from 2026.","Yearly renewal from $499 (registered agent + annual report)."]),
 dict(c="UK", n="United Kingdom", g="Europe", e="Private limited company (Ltd) at Companies House. No UK-resident director needed.",
  tiers=[
   dict(sku="uk-starter", n="Starter", p=299, buy=True, i=["Companies House fee (£100) included","Director identity verification","Registered office address, 12 months","Share certificates & digital documents"]),
   dict(sku="uk-business", n="Business", p=599, buy=True, pop=True, plus="Everything in Starter, plus", i=["Director service address, 12 months","HMRC Corporation Tax (UTR) registration","Business account application support","VAT registration if needed"]),
   dict(sku="uk-complete", n="Complete", p=1290, buy=True, plus="Everything in Business, plus", i=["First-year accounts via our accountant partner","Confirmation statement filing (£50 fee included)"])],
  notes=["Yearly renewal from $449 (registered office + confirmation statement)."]),
 dict(c="CA", n="Canada", g="North America", e="Ontario or BC corporation. No resident-director rule in either province.",
  tiers=[
   dict(sku="ca-starter", n="Starter", p=749, buy=True, i=["Government fees & NUANS name search included","Articles & bylaws","Business Number (BN) registration","Digital minute book"]),
   dict(sku="ca-business", n="Business", p=1190, buy=True, pop=True, plus="Everything in Starter, plus", i=["Registered office address, 12 months","GST/HST registration","Business account application support","Amazon.ca readiness call"])],
  notes=["Federal corporation available on request (25% of directors must be Canadian residents)."]),
 dict(c="EE", n="Estonia", g="Europe", e="Private limited company (OÜ), run fully online with e-Residency.",
  tiers=[
   dict(sku="ee-starter", n="Starter", p=749, buy=True, i=["State fee (€265) included","Articles of association","Legal address & contact person, 12 months","Registration guidance for e-Residency holders"]),
   dict(sku="ee-business", n="Business", p=1290, buy=True, pop=True, plus="Everything in Starter, plus", i=["VAT registration if needed","Business account (EMI) application support","Accounting partner introduction"])],
  notes=["You apply for e-Residency yourself and pay its fee to the Estonian government. e-Residency is not a visa or residence permit."]),
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
   dict(sku="sa-assessment", n="Market-entry assessment", p=299, buy=True, i=["Activity & licence route review","Capital and Saudization overview","Written plan and quote","Credited if you go ahead"]),
   dict(sku=None, n="Company setup", p=6900, frm=True, pop=True, i=["Investment licence & commercial registration","Chamber & municipality registrations","Bank account support","Government fees and capital not included"])],
  notes=["Setup usually takes 3–6 weeks. Work permits and expat levies are separate."]),
 dict(c="OM", n="Oman", g="Middle East", e="LLC with 100% foreign ownership for most activities.",
  tiers=[
   dict(sku=None, n="Company setup", p=1490, frm=True, i=["Commercial registration","Activity licences","Company documents","Chamber of commerce registration"]),
   dict(sku=None, n="Setup + investor visa", p=2690, frm=True, pop=True, plus="Everything in setup, plus", i=["One investor residence visa","Bank account support"])],
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
   dict(sku=None, n="Work permit", p=990, frm=True, i=["Per person","Eligibility check first","Application & visa coordination"])],
  notes=["Each foreign work permit generally needs THB 2M paid-up capital and 4 Thai employees (BOI companies differ). The Thai authorities decide.","BOI promotion and Foreign Business Licence are quoted separately."]),
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
