---
type: model
access_class: method
title: system_trap_detector
slug: system_trap_detector
status: active
maturity: active
sources: []
created: '2026-06-07'
---
# Engine spec: system_trap_detector

**Maturity:** `active` · **Implements:** engine/workflow diagnose_loops (pre-pricing) + assess_trap_implications (post)

```yaml
engine_name: system_trap_detector
maturity: active
implements: engine/workflow diagnose_loops (pre-pricing) + assess_trap_implications
  (post)
inputs:
- SystemMap
outputs:
- LoopDiagnosis
- TrapImplications
gates: []
depends_on: []
test_ref: tests/integration/test_loop_stage.py
non_goals: []
```
