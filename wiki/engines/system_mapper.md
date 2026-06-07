---
type: model
access_class: method
title: system_mapper
slug: system_mapper
status: active
maturity: active
sources: []
created: '2026-06-07'
---
# Engine spec: system_mapper

**Maturity:** `active` · **Implements:** engine/workflow build_system_map (SYSTEM_MAP) + engine/schema system_map

```yaml
engine_name: system_mapper
maturity: active
implements: engine/workflow build_system_map (SYSTEM_MAP) + engine/schema system_map
inputs:
- CausalChain
outputs:
- SystemMap
gates: []
depends_on: []
test_ref: tests/integration/test_system_stages.py
non_goals: []
```
