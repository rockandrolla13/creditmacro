---
type: model
access_class: method
title: backdoor_identifiability_gate
slug: backdoor_identifiability_gate
status: stub
maturity: not_built
sources: []
created: '2026-06-07'
---
# Engine spec: backdoor_identifiability_gate

**Maturity:** `not_built` · **Implements:** (none yet — next-ish build)

```yaml
engine_name: backdoor_identifiability_gate
maturity: not_built
implements: "(none yet \u2014 next-ish build)"
inputs:
- CausalChain
outputs:
- identifiability verdict
gates:
- refuse promotion if effect not identified
depends_on: []
test_ref: ''
non_goals:
- DoWhy integration (deferred)
```
