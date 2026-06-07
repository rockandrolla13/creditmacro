---
type: model
access_class: method
title: max_entropy_probability_justifier
slug: max_entropy_probability_justifier
status: active
maturity: active
sources: []
created: '2026-06-07'
---
# Engine spec: max_entropy_probability_justifier

**Maturity:** `active` · **Implements:** engine/probability.justify_probabilities + engine2.solve_q_tilt/run_pricing

```yaml
engine_name: max_entropy_probability_justifier
maturity: active
implements: engine/probability.justify_probabilities + engine2.solve_q_tilt/run_pricing
inputs:
- scenarios
- X_mkt
- prior
outputs:
- priced-in q
- residual edge
- ProbabilitySetJustification
gates:
- INFEASIBLE if X_mkt outside scenario span
- edge gross_of_risk_premium
depends_on: []
test_ref: tests/unit/test_probability.py
non_goals: []
```
