# METHOD-layer bibliography

Curated, source-quality references that serve as the **method layer** (how to reason)
for the theme-to-trade engine. Everything here is **method, not market views**. Each
item maps to a pipeline stage and the primitive/skill it yields. Foundational/canonical
work is listed first per stage.

**Verification:** every non-obvious citation was web-verified (year, venue, pages). Four
metadata errors caught and corrected during review (titles/venues, not fabricated works):
Jurado-Ludvigson-Ng *Measuring Uncertainty* (AER 2015); Ang-Bekaert *International Asset
Allocation With Regime Shifts* (RFS 2002); Yu *How Profitable Is Capital Structure
Arbitrage?* (FAJ 2006); Bai-Collin-Dufresne *The CDS-Bond Basis* (Financial Management
2019). **Method-suspect flags** (use the method, not any backtest/marketing): Soros and
Carver (practitioner books); CreditGrades (industry doc); arXiv q-fin (un-refereed).

Pipeline stages: `ICEBERG` (Stage-0 classify) · `CAUSAL` (Causal Compiler) ·
`SYSTEM`/`TRAP` (System Mapper + loop/trap) · `PRICING` (Scenario & Counterfactual) ·
`EXPRESSION` (strategy-family routing) · `CONTEXT` (driver/regime) · `DOWNSTREAM` (sizing,
reference only).

---

## 1. Causal reasoning → feeds `CAUSAL`

| Title | Authors · Yr | Venue · Type | Stage → primitive it yields | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [Causality (2e)](https://bayes.cs.ucla.edu/BOOK-2K/) | Pearl · 2009 | CUP · book | CAUSAL → the do-calculus ladder (see vs do); back-door identification | paywalled · **Y** | The foundational text of modern causal inference |
| [The Book of Why](https://en.wikipedia.org/wiki/The_Book_of_Why) | Pearl & Mackenzie · 2018 | Basic Books · book | CAUSAL → classify each edge (confounder/collider/mediator) | paywalled · Y | Accessible statement of the ladder the compiler walks |
| [Causal Inference for Statistics, Social, and Biomedical Sciences](https://www.cambridge.org/core/books/causal-inference-for-statistics-social-and-biomedical-sciences/71126BE90C58F1A431FE9B2DD07938AB) | Imbens & Rubin · 2015 | CUP · book | CAUSAL → state the assumption that makes an effect identified | paywalled · **Y** | Canonical potential-outcomes treatment |
| [Mostly Harmless Econometrics](https://www.mostlyharmlesseconometrics.com/) | Angrist & Pischke · 2009 | Princeton · book | CAUSAL → pick the identification strategy (IV/DiD/RD) | paywalled · **Y** | Applied-identification standard (Angrist, 2021 Nobel) |
| [Causal Inference: The Mixtape](https://mixtape.scunning.com/) | Cunningham · 2021 | Yale UP · book | CAUSAL → operationalize confounder control (code-first) | **open** · Y | Reputable press, freely readable; theory→implementation |
| [Elements of Causal Inference](https://library.oapen.org/handle/20.500.12657/26040) | Peters, Janzing & Schölkopf · 2017 | MIT Press · book | CAUSAL → the SCM formalism behind a CausalChain | **open** · Y | MIT Press, open; formal backbone for graph causality |

## 2. Systems dynamics → feeds `SYSTEM` + `TRAP`

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [Thinking in Systems: A Primer](https://www.chelseagreen.com/product/thinking-in-systems/) | Meadows · 2008 | Chelsea Green · book | SYSTEM → stocks/flows/R-B loops/delays/leverage points (the mapper's vocabulary) | paywalled · **Y** | The canonical systems-thinking text; the mapper is built on it |
| [Business Dynamics](https://www.mheducation.com/highered/product/business-dynamics-systems-thinking-modeling-complex-world-sterman/M9780072389159.html) | Sterman · 2000 | McGraw-Hill · book | TRAP → diagnose which loop dominates now | paywalled · **Y** | Graduate standard for operational system dynamics |
| [Industrial Dynamics](https://mitpress.mit.edu/9780262560016/) | Forrester · 1961 | MIT Press · book | SYSTEM → the stock-vs-flow primitive | paywalled · **Y** | Founding work of the field |
| [The Limits of Arbitrage](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.35053) | Shleifer & Vishny · 1997 | J. Finance · paper | TRAP → why crowded trades reverse, not converge | paywalled · **Y** | Foundation of limits-to-arbitrage; the trap detector's core |
| [Noise Trader Risk in Financial Markets](https://www.journals.uchicago.edu/doi/10.1086/261703) | De Long, Shleifer, Summers & Waldmann · 1990 | J. Political Economy · paper | TRAP → crowding as a self-reinforcing priced risk | paywalled · **Y** | Top-5 journal; foundational for crowding/overshoot |
| [The Alchemy of Finance](https://www.wiley.com/en-us/The+Alchemy+of+Finance-p-9780471445494) | Soros · 1987/2003 | Wiley · book | TRAP → flag reflexive edges (`feedback=True`) | paywalled · N | Seminal for reflexivity — **caveat: practitioner, not peer-reviewed; use the mechanism** |

## 3. Scenario & probability → feeds `PRICING` + Q4 justification

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [Elements of Information Theory (2e)](https://onlinelibrary.wiley.com/doi/book/10.1002/047174882X) | Cover & Thomas · 2006 | Wiley · book | PRICING → min-relative-entropy = the tilt q solver's foundation | paywalled · **Y** | Canonical information-theory text; justifies min-KL(q‖prior) |
| [A Simple Nonparametric Approach to Derivative Security Valuation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7925) | Stutzer · 1996 | J. Finance 51(5) 1633–52 · paper | PRICING → priced-in q from (prior, price) | paywalled · **Y** | Top journal; seminal entropy-pricing method the engine implements |
| [The Maximum Entropy Distribution of an Asset Inferred from Option Prices](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7617) | Buchen & Kelly · 1996 | JFQA 31(1) 143–59 · paper | PRICING → K>1 tilt with option-payoff constraints | paywalled · **Y** | Peer-reviewed origin of option-constrained entropy q |
| [Prices of State-Contingent Claims Implicit in Option Prices](https://www.journals.uchicago.edu/doi/10.1086/296025) | Breeden & Litzenberger · 1978 | J. Business 51 621–51 · paper | PRICING → model-free option-implied distribution | paywalled · **Y** | Foundational state-price-density result |
| [Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf) | Gneiting & Raftery · 2007 | JASA 102 359–78 · paper | Q4 → how to score/justify p_s | **open (PDF)** · **Y** | JASA, very high citation; defines defensible probability eval |
| [Verification of Forecasts Expressed in Terms of Probability](https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml) | Brier · 1950 | Mon. Weather Rev. 78 1–3 · paper | Q4 → the Brier calibration primitive | paywalled · **Y** | Origin of probabilistic calibration scoring |
| [Superforecasting](https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/) | Tetlock & Gardner · 2015 | Crown · book | Q4 → disciplined p_s elicitation (base rates, updating) | paywalled · N | Distills peer-reviewed GJP — **cite the process, not anecdotes** |

## 4. Risk premia & factors → feeds `EXPRESSION` (the gross-of-premium constraint)

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [Expected Returns](https://www.wiley.com/en-us/Expected+Returns%3A+An+Investor%27s+Guide+to+Harvesting+Market+Rewards-p-9781119990727) | Ilmanen · 2011 | Wiley · book | EXPRESSION → alpha-vs-premium taxonomy | paywalled · **Y** | Standard synthesis of the risk-premia literature |
| [Carry](https://www.nber.org/system/files/working_papers/w19325/w19325.pdf) | Koijen, Moskowitz, Pedersen & Vrugt · 2018 | JFE 127(2) 197–225 · paper | EXPRESSION → cross-asset carry signal | preprint open · **Y** | Top-3 journal; defines carry as a model-free primitive |
| [Value and Momentum Everywhere](https://onlinelibrary.wiley.com/doi/10.1111/jofi.12021) | Asness, Moskowitz & Pedersen · 2013 | J. Finance · paper | EXPRESSION → value/momentum signals + shared-factor caution | paywalled · **Y** | Canonical cross-asset factor evidence |
| [Betting Against Beta](https://www.sciencedirect.com/science/article/abs/pii/S0304405X13002675) | Frazzini & Pedersen · 2014 | JFE · paper | EXPRESSION → low-beta/defensive signal | paywalled · **Y** | Canonical low-risk-anomaly mechanism |
| [The Determinants of Credit Spread Changes](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00402) | Collin-Dufresne, Goldstein & Martin · 2001 | J. Finance 56(6) 2177–207 · paper | PRICING/EXPRESSION → spread ≠ mispricing (the standing confounder → `edge_basis`) | paywalled · **Y** | Top journal; empirical basis for "gross of risk premium" |
| [Explaining the Rate Spread on Corporate Bonds](https://pages.stern.nyu.edu/~mgruber/working%20papers/explaining_rate_final_JF.pdf) | Elton, Gruber, Agrawal & Mann · 2001 | J. Finance 56(1) 247–77 · paper | EXPRESSION → spread decomposition (default is a small part) | preprint open · **Y** | The credit-spread-puzzle reference |

## 5. Credit & relative value → feeds credit `EXPRESSION` families

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [On the Pricing of Corporate Debt (Merton model)](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1974.tb03058.x) | Merton · 1974 | J. Finance 29 449–70 · paper | EXPRESSION → structural credit-vs-equity link | paywalled · **Y** | Founding structural credit model |
| [CreditGrades Technical Document](https://www.msci.com/documents/10199/dd31bcce-6fe3-47b7-9fb7-10c4c8f750ba) | Finger et al. (RiskMetrics/DB/GS/JPM) · 2002 | RiskMetrics · tech doc | EXPRESSION → capital-structure-arb mechanics | **open** · Y | Four-dealer standard structural model — **caveat: industry doc, not peer-reviewed** |
| [Modelling Single-name and Multi-name Credit Derivatives](https://www.wiley.com/en-us/Modelling+Single-name+and+Multi-name+Credit+Derivatives-p-9780470519288) | O'Kane · 2008 | Wiley · book | EXPRESSION → cash-CDS basis + curve mechanics | paywalled · **Y** | The practitioner-standard credit-derivatives reference |
| [How Profitable Is Capital Structure Arbitrage?](https://www.tandfonline.com/doi/abs/10.2469/faj.v62.n5.4282) | Yu · 2006 | FAJ 62(5) 47–62 · paper | EXPRESSION → cap-structure-arb risk/return | paywalled · Y | Peer-reviewed test of the trade family + its drawdowns |
| [The CDS-Bond Basis](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2024531) | Bai & Collin-Dufresne · 2019 | Financial Management 48(2) 417–39 · paper | EXPRESSION → why the basis exists & mean-reverts | paywalled · Y | Peer-reviewed decomposition of the exact basis the engine prices |

## 6. Rates & term structure → feeds curve/steepener `EXPRESSION`

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [Expected Returns in Treasury Bonds](https://academic.oup.com/rfs/article-abstract/28/10/2859/1580557) | Cieslak & Povala · 2015 | RFS 28(10) 2859–901 · paper | PRICING → rates fair-value (g) + cycle predictor | paywalled · **Y** | Top journal; leading bond risk-premium predictor |
| [Resolving the Spanning Puzzle in Macro-Finance Term Structure Models](https://www.michaeldbauer.com/publication/spanning-puzzle/) | Bauer & Rudebusch · 2017 | Review of Finance 21(2) 511 · paper | CONTEXT → how macro enters a curve fair-value | preprint open · **Y** | Top journal; resolves a central macro-finance question |
| [A Yield-Factor Model of Interest Rates](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9965.1996.tb00123.x) | Duffie & Kan · 1996 | Math. Finance 6(4) 379–406 · paper | PRICING → the affine TSM fair-value engine | paywalled · **Y** | Foundational affine-model paper |
| [A No-Arbitrage VAR of Term Structure Dynamics](https://www.sciencedirect.com/science/article/abs/pii/S0304393203000321) | Ang & Piazzesi · 2003 | JME 50(4) 745–87 · paper | CONTEXT → macro-driven curve shape | paywalled · **Y** | High-citation; links macro drivers to curve fair value |
| [Bond Risk Premia](https://www.aeaweb.org/articles?id=10.1257/0002828053828581) | Cochrane & Piazzesi · 2005 | AER 95(1) 138–60 · paper | EXPRESSION → curve carry/value (forward-rate factor) | paywalled · **Y** | Top-5 journal; canonical bond-return predictability |
| [A Preferred-Habitat Model of the Term Structure of Interest Rates](https://www.nber.org/papers/w15487) | Vayanos & Vila · 2021 | Econometrica 89(1) 77–112 · paper | PRICING → bond supply/demand shock → continuous term-premium shift (model asset-supply shocks mathematically, not observationally) | preprint open · **Y** | Canonical preferred-habitat model; the supply→risk-premium transmission for QE / central-bank-balance-sheet shocks *(PDF in `research/preferred-habitat/`)* |

## 7. Macro regimes → feeds `CONTEXT` (driver extraction)

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [A New Approach to the Economic Analysis of Nonstationary Time Series](https://www.jstor.org/stable/1912559) | Hamilton · 1989 | Econometrica · paper | CONTEXT → regime state as a scenario driver | paywalled · **Y** | The canonical regime-switching reference |
| [Nowcasting: The Real-Time Informational Content of Macroeconomic Data](https://ideas.repec.org/a/eee/moneco/v55y2008i4p665-676.html) | Giannone, Reichlin & Small · 2008 | JME 55(4) 665–76 · paper | CONTEXT → real-time regime/driver state | paywalled · **Y** | Foundational nowcasting paper, now central-bank standard *(PDF in `research/nowcasting/`)* |
| [Measuring Uncertainty](https://www.aeaweb.org/articles?id=10.1257/aer.20131193) | Jurado, Ludvigson & Ng · 2015 | AER 105(3) 1177–216 · paper | CONTEXT → uncertainty/risk-appetite driver | paywalled · **Y** | Top-5 journal; rigorous uncertainty measurement |
| [International Asset Allocation With Regime Shifts](https://academic.oup.com/rfs/article-abstract/15/4/1137/1568247) | Ang & Bekaert · 2002 | RFS 15 1137–87 · paper | CONTEXT → crisis-regime scenario weighting | paywalled · **Y** | Peer-reviewed evidence regimes matter for allocation |
| [New Indicators for Tracking Growth in Real Time](https://www.imf.org/external/pubs/ft/wp/2011/wp1143.pdf) | Matheson · 2011 | IMF WP 11/43 · paper | CONTEXT → global growth-tracking driver | **open** · Y | IMF working paper; multi-country real-time growth indicators *(PDF in `research/nowcasting/`)* |
| [An Aggregative Theory for a Closed Economy](https://kilthub.cmu.edu/articles/journal_contribution/An_Aggregative_Theory_for_a_Closed_Economy/6703592) | Brunner & Meltzer · 1976 | in *Monetarism* (ed. Stein), Ch. 2, 69–103 · book chapter | CONTEXT/CAUSAL → flow-of-funds transmission matrix; split a macro input into stock vs flow channels (asset substitution when balance sheets turn) | open (CMU archive) · **Y** | Foundational monetarist asset-substitution framework behind the balance-sheet→risk-premium pair *(PDF in `research/preferred-habitat/`)* |

## 8. Portfolio & sizing → `DOWNSTREAM` (reference only; the engine stops at a memo)

| Title | Authors · Yr | Venue · Type | Stage → primitive | Access · Canon | Why it clears the bar |
|---|---|---|---|---|---|
| [The Properties of Equally Weighted Risk Contribution Portfolios](https://www.pm-research.com/content/iijpormgmt/36/4/60) | Maillard, Roncalli & Teïletche · 2010 | J. Portfolio Mgmt · paper | DOWNSTREAM → risk-parity sizing | paywalled · Y | Peer-reviewed formalization of risk parity |
| [A New Interpretation of Information Rate (Kelly)](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1956.tb03809.x) | Kelly · 1956 | Bell System Tech. J. · paper | DOWNSTREAM → Kelly / fractional-Kelly sizing | paywalled · **Y** | Origin of growth-optimal sizing |
| [Systematic Trading](https://www.systematicmoney.org/systematic-trading) | Carver · 2015 | Harriman House · book | DOWNSTREAM → vol-targeting/cost-aware sizing (the `Sizing` rules) | paywalled · Y | Method-sound, widely used — **practitioner book; use the framework, not a backtest** |

---

## Repositories & data

**Code repos**
| Name | Provides | License | Link | Why |
|---|---|---|---|---|
| DoWhy | causal graph modeling, identification, refutation tests | MIT | [py-why/dowhy](https://github.com/py-why/dowhy) | PyWhy/Microsoft; refutation tests operationalize assumption-checking |
| EconML | heterogeneous treatment effects (CATE), DML/causal forests | MIT | [microsoft/EconML](https://github.com/microsoft/EconML) | Microsoft Research; estimator layer composing with DoWhy |
| statsmodels | regression, time series, state-space, Markov-switching | BSD-3 | [statsmodels](https://github.com/statsmodels/statsmodels) | Hamilton regime-switching + TSM building blocks |
| QuantLib | curve bootstrapping, option pricing, CDS | BSD-style | [lballabio/QuantLib](https://github.com/lballabio/QuantLib) | Reference open-source quant library for curve/option/CDS mechanics |
| PyMC | Bayesian inference, priors → posteriors | Apache-2.0 | [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | Principled probability layer for the Q4 step |

**Paper collections / preprint sources**
| Source | Access | Link | Why |
|---|---|---|---|
| NBER Working Papers | mostly open | [nber.org](https://www.nber.org/papers) | Reputable institution; canonical-author preprints |
| SSRN (FEN) | mixed | [ssrn.com](https://www.ssrn.com/) | Primary finance preprint repository |
| arXiv q-fin | open | [arxiv.org/list/q-fin](https://arxiv.org/list/q-fin/recent) | Open — **un-refereed, treat as preprint** |
| BIS Working Papers | open | [bis.org](https://www.bis.org/wpapers.htm) | Reputable institution; macro-finance + spread literature |
| Fed working papers (FRB SF/Chicago) | open | [frbsf.org](https://www.frbsf.org/economic-research/publications/working-papers/) | Central-bank source for rates/regime method |
| now-casting.com research index | open | [now-casting](https://www2.now-casting.com/resources/research) | Reichlin et al. nowcasting paper index (US/Global PDFs pulled to `research/nowcasting/`) |

**Open datasets**
| Dataset | Terms | Link | Why |
|---|---|---|---|
| FRED | free, non-commercial/educational | [fred.stlouisfed.org](https://fred.stlouisfed.org/) | St. Louis Fed; standard free macro/rates source |
| Kenneth French Data Library | free for research | [French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) | Reference factor-return library |
| OFR Financial Stress Index | free (US Treasury/OFR) | [financialresearch.gov](https://www.financialresearch.gov/financial-stress-index/) | Ready-made stress/regime driver |
| Chicago Fed NFCI | free | [chicagofed.org/nfci](https://www.chicagofed.org/research/data/nfci/current-data) | Central-bank FCI for driver extraction |

---

## Top-10 to convert to skills first

| # | Item | The one primitive it yields |
|---|---|---|
| 1 | Pearl, *Causality* / *Book of Why* | the causal ladder — narrative → assoc/intervene/counterfactual with an identifying assumption per edge |
| 2 | Meadows, *Thinking in Systems* | the stock/flow + R/B-loop + delay vocabulary the System Mapper writes |
| 3 | Cover & Thomas, *Information Theory* | min-relative-entropy → priced-in q from (prior, market price) |
| 4 | Stutzer 1996 (+ Buchen-Kelly 1996) | entropy/option-constrained q → residual edge = ⟨p−q, X⟩ |
| 5 | Collin-Dufresne et al. 2001 (+ Elton et al. 2001) | the standing risk-premium confounder: spread ≠ mispricing → `edge_basis=gross_of_risk_premium` |
| 6 | Shleifer & Vishny 1997 | the balancing-loop limit → crowding-reversal diagnosis (Trap Detector) |
| 7 | Gneiting & Raftery 2007 | the Q4 probability-justification primitive: score/calibrate p_s, don't assert it |
| 8 | Imbens & Rubin 2015 (+ Angrist-Pischke) | the identification-strategy chooser: name what makes the effect estimable |
| 9 | Merton 1974 (+ O'Kane 2008) | structural credit-vs-equity link + CDS/basis mechanics → credit expression families |
| 10 | Cieslak-Povala 2015 (+ Cochrane-Piazzesi 2005) | rates fair-value `g` + forward-rate predictor → curve-shape routing |
