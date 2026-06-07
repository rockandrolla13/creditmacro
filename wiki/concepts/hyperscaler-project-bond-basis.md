---
type: concept
access_class: method
title: Hyperscaler vs project-bond basis (mechanics)
slug: hyperscaler-project-bond-basis-mechanics
aliases: ["hyperscaler-project-basis-concept"]
tags: [concept, basis, relative-value]
status: active
sources: [jpm-ai-capex-funding-2026-05-11]
created: 2026-06-07
updated: 2026-06-07
---

# Hyperscaler vs project-bond basis (mechanics)

> Method (mechanic). The market-specific instance is the CASE theme
> [[hyperscaler-project-bond-basis]] — this page teaches the general construction only.

## What it is
A spread *relationship* between a hyperscaler's own IG credit and the data-center project bonds
funded by the same capex, at different risk profiles (IG project vs HY project).

## Mechanics (how to reason)
Same driver (capex) funds both legs; structural differences (recourse, subordination, duration,
liquidity) set a *level* for the differential. The RV signal is deviation from that level — but
only if the differential is **stationary / mean-reverting** and **net of duration and rating**.

## Operational-axis form
`hyperscaler IG OAS − IG DC-project OAS`; `hyperscaler IG OAS − HY DC-project OAS`
(duration/rating-adjusted). Express as a [[long_short]] family — never as legs here.

## Confounders
Duration, rating/subordination, liquidity premium, and the standing credit risk premium (the
level may be fair compensation, not mispricing → gross of premium).

## Linked
[[related-obligation-rv]] · [[data-center-credit]] · family [[long_short]] · theme
[[hyperscaler-project-bond-basis]].
