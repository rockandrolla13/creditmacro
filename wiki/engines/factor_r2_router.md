---
type: model
access_class: method
title: factor_r2_router
slug: factor_r2_router
status: stub
maturity: schema_only
sources: []
created: '2026-06-07'
---
# Engine spec: factor_r2_router

**Maturity:** `schema_only` · **Implements:** engine/discovery._route_family (axis shape+direction → family)

```yaml
engine_name: factor_r2_router
maturity: schema_only
implements: "engine/discovery._route_family (axis shape+direction \u2192 family)"
inputs:
- axis
- factor returns
outputs:
- StrategyFamilyRec
gates: []
depends_on: []
test_ref: ''
non_goals:
- full factor regression (deferred until a returns/factor library exists)
```
