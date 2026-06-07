---
type: concept
access_class: method
title: Related-obligation relative value
slug: related-obligation-rv
tags: [concept, relative-value, ai-capex]
status: active
sources: [jpm-ai-capex-funding-2026-05-11]
created: 2026-06-07
updated: 2026-06-07
---

# Related-obligation relative value

## What it is
RV between obligations that share a **common economic driver** but sit at different points of a
capital structure / risk profile (e.g. a hyperscaler's IG credit vs the data-center project bonds
its capex funds, vs the HY HPC issuers in the same chain).

## Mechanics (how to reason)
Because the legs load on one factor (here: AI-capex funding), a multi-leg expression is **not a
diversified bet** — it is a bet on the *relationship* between legs (the differential), net of the
standing premium. Build a named differential axis; require it to be stationary and clean; size
the family confidence by data sufficiency and liquidity. The shared factor is recorded so the
portfolio layer does not double-count diversification.

## Operational-axis form
`leg-A OAS − leg-B OAS` (duration/rating-adjusted) for any two related obligations; routes to the
[[long_short]] family (or [[index_index_rv]] / [[etf_basket_rv]] for index/ETF wrappers).

## Confounders
Standing credit risk premium; shared-factor illusion (legs look independent but co-move);
duration/rating contamination; liquidity asymmetry between legs.

## Linked
[[hyperscaler-project-bond-basis-mechanics]] · [[data-center-credit]] ·
[[high-performance-computing-credit]] · families [[long_short]], [[index_index_rv]],
[[etf_basket_rv]] · theme [[ai-capex-funding-credit-ecosystem]].
