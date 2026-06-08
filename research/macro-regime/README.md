# Macro state inference — regime (HMM) + factor (DFM) method pair

Turn many conflicting, asynchronous macro series into a single latent state. Two canonical
methods, paired:

```
[hundreds of asynchronous data streams]
        | (Stock–Watson DFM)  → clean/align/extract ONE latent signal
[conflicting arrays: low unemployment + plunging PMIs]
        | (Hamilton HMM/Markov-switching)  → unobserved state-probability vector
[has the economy crossed a phase threshold?]
```

## Regime / HMM → CONTEXT
Hamilton, J. D. (1989), "A New Approach to the Economic Analysis of Nonstationary Time Series
and the Business Cycle," *Econometrica* 57(2), 357–384.
- **The canonical 1989 paper is paywalled (JSTOR/Econometrica) — not redistributed here.**
- Captured instead: Hamilton's own open method survey, `hamilton_2005_regime_switching_models.pdf`
  ("Regime-Switching Models," prepared for *The New Palgrave Dictionary of Economics*, 2005) —
  same Markov-switching/HMM machinery, openly hosted by the author.
  Source: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- Skill: map conflicting data arrays into an unobserved state-probability vector (regime).

## Factor / DFM → CONTEXT
Stock, J. H. & Watson, M. W. (2002), "Forecasting Using Principal Components From a Large
Number of Predictors," *Journal of the American Statistical Association* 97(460), 1167–1179.
- File: `stock_watson_2002_principal_components.pdf` (15 pp)
- Source: https://www.princeton.edu/~mwatson/papers/Stock_Watson_JASA_2002.pdf (open author copy)
- Skill: dynamic factor modeling — clean, align, and extract a single latent signal from
  hundreds of asynchronous predictors; the framework behind real-time macro nowcasting.

## Conversion notes
- PDFs are gitignored (`*.pdf`); only the `.md` extractions are tracked.
- Hamilton survey: `pymupdf4llm` (primary engine), clean.
- Stock–Watson: primary engine silently under-extracted (valid Type-1 text layer misread as
  images → 5 KB of empty headings). Regenerated with `pdftotext -layout` fallback (94 KB).
  No OCR needed.
