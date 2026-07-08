---
doc_id: gc-001-funding
source_institution: JPMorgan
doc_date: "2026-03-01"
claims:
  - text: "IG spreads set to widen as funding stress builds"
    market_variable: C0A0_OAS
    direction: 1
    horizon_days: 90
    stated_conviction: 2
    mechanism_tags: [funding_stress, liquidity_premium]
  - text: "HY dispersion rising on heavier issuance supply"
    market_variable: H0A0_OAS
    direction: 1
    horizon_days: 60
    stated_conviction: 1
    mechanism_tags: [issuance_supply]
---
# Golden corpus doc 001 (single institution, two distinct claims)
Prose body is what an LLM extractor would read; the scripted provider reads the
`claims:` block above for deterministic gates.
