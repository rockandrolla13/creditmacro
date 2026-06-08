# Preferred habitat — balance-sheet → risk-premium method pair

How a change in central-bank / institutional balance sheets (net asset buying, QE/QT)
re-prices risk-free and risky term premiums. Two canonical sources, paired:

```
[Central-bank balance-sheet change]
        | (flow vs stock friction matrices)
   [Brunner–Meltzer]  → splits the macro input into stock vs flow channels
        | (risk-premium shock)
   [Vayanos–Vila preferred habitat]  → continuous, non-linear term-premium re-pricing
```

## Term-structure / supply-shock → PRICING
Vayanos, D. & Vila, J.-L. (2021), "A Preferred-Habitat Model of the Term Structure of
Interest Rates," *Econometrica* 89(1), 77–112.
- File: `vayanos_vila_2021_preferred_habitat.pdf` (full final version + online appendix, 100 pp)
- Source: https://personal.lse.ac.uk/vayanos/Papers/PHMTSIR_ECMAf.pdf
  (open author copy; NBER WP 15487 twin: https://www.nber.org/papers/w15487; Econometrica DOI
  https://doi.org/10.3982/ECTA17440 is paywalled)
- Skill: translate institutional asset-supply shocks into continuous shifts in risk-free and
  risky term premiums — model the shock mathematically, not observationally.

## Monetary transmission / stock-vs-flow → CONTEXT/CAUSAL
Brunner, K. & Meltzer, A. H. (1976), "An Aggregative Theory for a Closed Economy," in
*Monetarism* (ed. J. L. Stein), Ch. 2, 69–103, North-Holland.
- File: `brunner_meltzer_1976_aggregative_theory.pdf` (35 pp)
- Source: Carnegie Mellon KiltHub (Meltzer archive) —
  https://kilthub.cmu.edu/articles/journal_contribution/An_Aggregative_Theory_for_a_Closed_Economy/6703592
  (figshare-backed; direct file via the figshare API)
- Skill: construct flow-of-funds transmission matrices; split macro inputs into stock vs flow
  channels to model asset substitution when central-bank balance sheets turn.

## Conversion notes
- PDFs are gitignored (`*.pdf`); only the `.md` extractions are tracked.
- Vayanos–Vila: `pymupdf4llm` (primary engine), clean.
- Brunner–Meltzer: the primary engine silently under-extracted this PDF (valid text layer it
  misread as images → near-empty output). Regenerated with the `pdftotext -layout` fallback,
  which recovered the full ~95 KB of text. No OCR was needed (the text layer is intact).
