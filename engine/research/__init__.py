"""V4 Research OS domain objects — a SECOND domain on this repo's epistemic substrate.

Normative spec: ResearchHarness/RESEARCH_OS_DEFINITIVE_SPEC_V4.md. These objects model
research (stimulus → question → model → hypothesis → protocol → claim); the credit engine
models markets. Both are falsifiable-claim machines, which is why they share a substrate
rather than a codebase each.

Nothing here imports engine.ledger: that coupling would run the wrong way. Where a pattern
already exists there (frozen models, a signed causal path, freeze-by-hash), it is FOLLOWED,
not imported.
"""
