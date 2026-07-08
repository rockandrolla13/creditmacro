---
doc_id: gc-002-mixed
source_institution: GoldmanSachs
doc_date: "2026-03-05"
claims:
  # two entries share (C0A0_OAS, +1, 90d) → merge to one claim, union of tags
  - text: "IG wider on funding stress"
    market_variable: C0A0_OAS
    direction: 1
    horizon_days: 90
    stated_conviction: 1
    mechanism_tags: [funding_stress]
  - text: "IG wider as dealer capacity thins"
    market_variable: C0A0_OAS
    direction: 1
    horizon_days: 90
    stated_conviction: 3
    mechanism_tags: [dealer_balance_sheet_capacity]
  # an out-of-vocabulary tag → dropped from the claim, routed to review
  - text: "curve steepens on term premium and a novel channel"
    market_variable: 3M10Y
    direction: 1
    horizon_days: 120
    stated_conviction: 2
    mechanism_tags: [term_premium, some_made_up_node]
---
# Golden corpus doc 002 (granularity-merge + out-of-vocab tag)
