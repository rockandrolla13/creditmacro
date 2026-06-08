# Global IO network — macro-shock propagation method pair

Trace a macro shock (tariffs, regional investment blocks) through international corporate
networks to downstream earnings impairment at unlisted suppliers.

```
[macro shock: US auto tariff, regional capex block]
        | (Koopman–Wang–Wei value-added decomposition)
[global input-output network: regional-sector nodes, value-added-flow edges]
        | shock a node → propagate
[downstream earnings impairment across unlisted global suppliers]
        | (Acemoglu–Robinson, boundary conditions)
[political-economy regime as a boundary on the state-space tracker]
```

## Global IO network → CAUSAL/SYSTEM
Koopman, R., Wang, Z. & Wei, S.-J. (2014), "Tracing Value-Added and Double Counting in Gross
Exports," *American Economic Review* 104(2), 459–494.
- File: `koopman_wang_wei_2014_value_added_exports.pdf` (NBER WP 18579 twin, 72 pp)
- Source: https://www.nber.org/system/files/working_papers/w18579/w18579.pdf
  (AER DOI https://doi.org/10.1257/aer.104.2.459 is paywalled)
- Skill: build network graphs (regional-sector nodes, value-added-flow edges); shock one node
  and solve for downstream impairment across unlisted global suppliers.

## Political-economy boundary conditions → CONTEXT  *(citation only)*
Acemoglu, D. & Robinson, J. A. (2019), *The Narrow Corridor: States, Societies, and the Fate
of Liberty*, Penguin.
- **No PDF here.** This is a current commercial book with no legitimate open copy, so it is
  **not redistributed** — it is a bibliography citation only (method: model political-economy
  hysteresis and structural policy-regime shifts as boundary conditions in the state-space
  tracker). See `docs/method_bibliography.md` §7.
- Open substitutes carrying the same mechanism, if a local artifact is wanted later:
  Acemoglu & Robinson, "Why Nations Fail" framework papers, or their NBER working papers on
  state capacity / institutions (e.g. "The Emergence of Weak, Despotic and Inclusive States").

## Conversion notes
- PDFs are gitignored (`*.pdf`); only the `.md` extraction is tracked.
- Koopman–Wang–Wei: `pymupdf4llm` (primary engine), clean (~150 KB; matched pdftotext).
