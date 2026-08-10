---
type: theme
slug: funding-liquidity-golden
mechanism:
  - [funding_stress, dealer_balance_sheet_capacity, 1]
  - [dealer_balance_sheet_capacity, liquidity_premium, 1]
  - [liquidity_premium, credit_spread, 1]
shock_direction: 1
operational_axis: C0A0_OAS
horizon_days: 90
falsifier: "IG OAS fails to widen 20bp within 60d of a funding-stress print"
mechanism_text: "funding stress drains dealer balance sheet capacity raising the liquidity premium and widening ig credit spreads"
---
# Funding → dealer capacity → liquidity → spreads (golden r3 — mechanism refinement)
Same endpoints and sign product as r1/r2, with an added intermediate node.
