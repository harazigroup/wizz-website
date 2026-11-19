# US LLC formation and yearly state upkeep by state, for the team quote builder (Admin → Leads → Quote).
# State fees checked Nov 2026 (state websites / LLC University). Our prices in MYR include the state fee
# and registered agent. Federal Form 5472 filing (RM 3,500) is the same for every state and is separate.
# tier: low / mid / high = state taxes and yearly fees.
US_STATES = [
 # state, tier, formation state fee, yearly state fee, formation RM, yearly upkeep RM, note
 ("New Mexico",   "low",  "$50",  "$0, no annual report",                 1199,  500, "No annual report. Gross receipts tax (about 5%) applies only to sales to New Mexico customers above $100k a year."),
 ("Wyoming",      "low",  "$100", "$60 annual report (min)",              1199,  800, "No state income or franchise tax. Owner privacy."),
 ("Montana",      "low",  "$35",  "$20 annual report (waived if filed by 15 April, 2026-2027)", 1199, 700, "No state sales tax. Annual report due 15 April."),
 ("South Dakota", "low",  "$150", "$55 annual report",                    1299,  800, "No state income, franchise or gross receipts tax. 4.2% sales tax on sales to SD customers above $100k a year."),
 ("Texas",        "mid",  "$300", "$0 franchise tax under $2.47M revenue; yearly Public Information Report", 1999, 900, "No state personal income tax. Franchise tax only above the revenue threshold."),
 ("Florida",      "mid",  "$125", "$138.75 annual report",                1399, 1200, "No state personal income tax. Annual report due 1 May."),
 ("Delaware",     "high", "$110", "$400 annual LLC tax (from 2026)",      1499, 2500, "Preferred by investors. Annual tax due 1 June."),
 ("Nevada",       "high", "$425", "$350 annual list + business licence",  2599, 2500, "No state income tax, but the highest yearly fees."),
 ("California",   "high", "$70",  "$800 minimum franchise tax + $20 statement every 2 years", 1499, 4500, "Highest cost. Extra LLC fee if California revenue is above $250k. Only if you operate in California."),
 ("New York",     "high", "$200", "$9 every 2 years",                     1499,  700, "Newspaper publication required within 120 days (about RM 1,500-7,000, quoted at cost)."),
]
TIER = {"low": "Lowest tax & fees", "mid": "Middle", "high": "Highest tax & fees"}
