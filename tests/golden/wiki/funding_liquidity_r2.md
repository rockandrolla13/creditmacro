---
type: theme
slug: funding-liquidity-golden
mechanism:
  - [funding_stress, liquidity_premium, 1]
  - [liquidity_premium, credit_spread, 1]
shock_direction: 1
operational_axis: C0A0_OAS
horizon_days: 90
falsifier: "IG OAS fails to widen 20bp within 60d of a funding-stress print"
mechanism_text: "rising funding stress lifts the liquidity premium which widens ig credit spreads modestly"
---
# Funding → liquidity → spreads (golden r2 — cosmetic reword)
Only the prose wording changed; the chain, axis, horizon, falsifier are identical.
