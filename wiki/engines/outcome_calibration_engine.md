---
type: model
access_class: method
title: outcome_calibration_engine
slug: outcome_calibration_engine
status: active
maturity: next
sources: []
created: '2026-06-07'
---
# Engine spec: outcome_calibration_engine

**Maturity:** `next` · **Implements:** engine/outcomes (ThemeOutcomeRecord) + engine/firewall.default_calibrator

```yaml
engine_name: outcome_calibration_engine
maturity: next
implements: engine/outcomes (ThemeOutcomeRecord) + engine/firewall.default_calibrator
inputs:
- closed theses (predicted vs realized)
outputs:
- calibration / edge-realization
gates: []
depends_on: []
test_ref: ''
non_goals:
- needs a corpus of closed theses first
```
