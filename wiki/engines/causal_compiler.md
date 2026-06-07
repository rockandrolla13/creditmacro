---
type: model
access_class: method
title: causal_compiler
slug: causal_compiler
status: active
maturity: active
sources: []
created: '2026-06-07'
---
# Engine spec: causal_compiler

**Maturity:** `active` · **Implements:** engine/llm_provider.expand_causal + workflow EXPAND_CAUSAL stage

```yaml
engine_name: causal_compiler
maturity: active
implements: engine/llm_provider.expand_causal + workflow EXPAND_CAUSAL stage
inputs:
- research_text
outputs:
- CausalNode
- CausalChain
- shared_factor
gates:
- theme node requires operational axis
depends_on: []
test_ref: tests/unit/test_expand_causal.py
non_goals: []
```
