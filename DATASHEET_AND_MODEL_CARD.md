# Datasheet and Model Card: BBO Capstone Project

**Project** · You Sank My Function — Black-Box Optimisation Capstone
**Institution** · Imperial College Business School · Bayesian Optimisation Challenge
**Author** · Eduardo Wizentier · [wizentier@gmail.com](mailto:wizentier@gmail.com)
**Date** · 30 August 2026
**Status** · Campaign complete — 13 weekly rounds, weeks 0–13, 279 observations, 33 records set
**Repository** · see [`README.md`](README.md) for the full map and reading order

This document contains **two complete, independent artefacts**:

| | Section | Framework | Covers |
|---|---|---|---|
| **Part 1** | [**Datasheet**](#part-1-datasheet-for-the-bbo-capstone-data-set) | Gebru et al., *Datasheets for Datasets* | Motivation · composition & schema · collection · preprocessing · uses · distribution · maintenance |
| **Part 2** | [**Model card**](#part-2-model-card-for-the-bbo-optimisation-approach) | Mitchell et al., *Model Cards for Model Reporting* | Model details · intended use · factors · metrics · data · results · limitations · ethics · caveats |

---

## Part 1: Datasheet for the BBO Capstone Data Set

### Motivation

**Why was the data set created?** To support the Imperial College Business School Bayesian Optimisation Challenge, which presents eight hidden black-box functions and permits one query per function per week. The data set is the accumulated query history: every input tried and every response returned. It exists because the challenge gives no other information — there is no functional form, no gradient, and no oracle beyond the weekly scalar.

**What task does it support?** Maximising each function's normalised best-ever score. Concretely it provides the evidence needed to fit local surrogate models, classify each function into a pathology archetype, estimate a performance ceiling, and audit each proposed query before it is spent.

**Who created it, and who funded the work?** Created and maintained by Eduardo Wizentier as sole author, as coursework for the capstone. No external funding, no sponsoring organisation, no third-party contributors.

### Composition

**What does an instance represent?** One function evaluation: an input vector $x \in [0,1]^d$ and the scalar response $y$ returned for it. There is exactly one instance per evaluation and no other instance type.

**How many instances are there?** **279 observations** across the eight functions: 175 initial design points supplied at week 0, plus 104 weekly queries (8 functions × 13 weeks).

| F | dim | initial design | weekly queries | total |
|---|-----|----------------|----------------|-------|
| F1 | 2 | 10 | 13 | 23 |
| F2 | 2 | 10 | 13 | 23 |
| F3 | 3 | 15 | 13 | 28 |
| F4 | 4 | 30 | 13 | 43 |
| F5 | 4 | 20 | 13 | 33 |
| F6 | 5 | 20 | 13 | 33 |
| F7 | 6 | 30 | 13 | 43 |
| F8 | 8 | 40 | 13 | 53 |
| | | **175** | **104** | **279** |

**What does each instance contain?** `consolidated_observations.csv` has the schema:

| Column | Type | Meaning |
|---|---|---|
| `function` | int 1–8 | Which hidden function |
| `dim` | int 2–8 | That function's dimensionality |
| `week` | int | 0 for the initial design, 1–13 for the weekly rounds |
| `source` | str | `initial` or `weekly` |
| `x1`…`x8` | float | Input coordinates, NaN-padded beyond that function's `dim` |
| `y` | float | The returned scalar response |

**Is any information missing?** The NaN padding in `x1`…`x8` is structural, not missing data: a 2-D function has no `x3`. No response is missing; every query issued returned a value.

**Are there errors, noise, or redundancies?** Yes, and the distinction is load-bearing. Three functions are **noisy** (F2, F3, F6) and five are **deterministic** (F1, F4, F5, F7, F8), established empirically from near-exact resamples rather than assumed. The clearest evidence is F2: its Week-3 replicate at the seed input returned 0.5580 against a seed best of 0.6112, which is why F2's seed "best" is treated as an upward draw rather than a location. Deliberate redundancy also exists — F7 and F8 were solved early, so their later weekly points are exploitation probes *at* the optimum. Those repeated near-identical readings bias naive global fits toward the plateau, and structure for those two functions should be read off the initial space-filling design instead.

**Does the data set contain personal, confidential, or sensitive data?** **No.** It consists entirely of numeric coordinates chosen by the author and scalar values returned by an automated challenge portal. There is no personal data, no human-subject data, no data relating to identifiable individuals, and nothing of a confidential or sensitive nature. No consent, anonymisation, or ethical review process applies.

**Are there identifiable gaps or biases?** Yes, severe, and they are the single most important caveat attached to this data set. The design suffers **spatial undersampling** and **exploitation bias**: acquisition functions favour exploiting known peaks, so vast tracts of each domain are never sampled at all. F1's observations are tightly clustered near `[0.628, 0.628]`. F5's best observations are pinned exactly at the bounds of the unit cube. At 23–53 observations in 2 to 8 dimensions, any claim about global structure is a hypothesis rather than a finding — a point `A4_clustering_unsupervised` and `A5_pca_dimensionality` each demonstrate from opposite directions.

### Collection process

**How was the data acquired?** Week 0 designs were **supplied by the challenge**, not chosen by the author: space-filling initial designs of 10 to 40 points per function. Weeks 1–13 were author-chosen, one query per function per week, submitted to the challenge portal with a one-week turnaround before the response returned.

**What sampling strategy was used?** From Week 7 onward, queries were generated by `pipeline/05_suggest_engine_v2.ipynb` under a "diagnose first, then choose the method" policy: structural signatures in the existing data (magnitude cascade, rank-correlation fingerprints, separability checks, noise-regime estimates from resamples) determine a pathology archetype, and the archetype selects the strategy that emits the candidate. Before Week 7 the process was equivalent but hand-run. This is emphatically **not** random or space-filling sampling after week 0, which is the origin of the exploitation bias documented above.

**Who was involved?** The author alone. No crowdworkers, contractors, or third parties. No compensation applies.

**Over what timeframe?** Weeks 0 through 13 of the campaign: the supplied initial design at week 0, followed by thirteen weekly rounds.

**Was an ethical review conducted?** Not applicable — no human subjects and no personal data.

**Raw capture format.** `inputs.txt` and `outputs.txt` accumulate one line per week, each line a Python list repr of eight vectors and eight scalars respectively. `04_consolidate_data.ipynb` parses these, asserts that input dimensionality matches each function's declared `dim`, asserts input/output week alignment, and fails loudly on mismatch rather than coercing.

### Preprocessing, cleaning, and labelling

**What preprocessing was done?** `04_consolidate_data.ipynb` normalises two accepted raw layouts (`function_N/initial_inputs.npy` + `initial_outputs.npy`, or tidy `fN_data.csv`), strips `np.float64(...)` and `array([...])` wrappers from the weekly reprs, validates integrity, and emits the single long table. No values are imputed, smoothed, clipped, or dropped.

**Are transforms baked into the stored data?** No. Variance-stabilising transforms are applied downstream at the point of modelling, never to the stored observations: a log transform $z = \log(-y)$ for F3 with the Jacobian carried so predictive densities remain comparable in $y$-units, and log-scale pricing for F5's large dynamic range. The stored `y` is always the raw portal response.

**Is the raw data retained?** Yes, unaltered. `consolidated_observations.csv` is fully derived and regenerable from it, which is why the pipeline reads the derived table and never hand-maintained notes.

**Are labels stored?** **No — and this is deliberate.** Pathology archetype labels are not a column in the data set. They are re-derived from scratch every week by `05_suggest_engine_v2`, because archetypes are states rather than identities and a function can legitimately change label as evidence accumulates. Hand-written hypothesis and status strings do exist in two convenience locations: an inlined `FUNCTION_META` table in `diagnostics/A1_svm_analysis.ipynb`, and a `FUNCTION_META` dictionary inside `04_consolidate_data.ipynb` that propagates a `status` column into `function_summary.csv`. Both are hand-maintained and can drift from the weekly classifier; see the model card's limitations.

**Software used.** Python with pandas and numpy. See `requirements.txt`.

### Uses

**What has the data been used for?** Testing routing hypotheses for black-box optimisation; fitting Gaussian process and neural surrogates; estimating per-function ceilings in `07_ceiling_estimator`; and pricing candidate probes through the `08_anti_hallucination_check` critic. It is also the substrate for the diagnostics and neural tracks, which apply supervised, unsupervised, dimensionality-reduction and deep-learning methods to the same observations as a study exercise, without ever selecting a query.

**Are there recommended splits?** There is no conventional train/test split and one should not be manufactured. Every observation cost a week and was immediately folded back into the model, so evaluation is necessarily **walk-forward**: `08_anti_hallucination_check` scores each staged submission against only the data available before that result returned, with calibration resting on nine walk-forward weeks per function. Random k-fold splits across weeks leak future information into the past and will overstate performance.

**What should the data set NOT be used for?** It should not be used to characterise the global landscape of these functions, to benchmark optimisers against one another, or to support any claim requiring an unbiased sample of the domain. The sample is small and the sampling is deliberately biased toward local regions and early successes. Fitting a global model and reporting high $R^2$ is specifically misleading here: `Preliminary_Pattern_Analysis` shows a global quadratic explaining roughly 99% of F4's variance while placing its own maximum *below* points already observed.

### Distribution

**Is the data publicly available?** The raw challenge data is **private** under the academic rules of the capstone. It is kept in a local `data/` folder, is not committed to the repository, and is not hosted externally.

**Is external hosting required?** No. The data set is 279 observations across eight functions — a few tens of kilobytes. There is no large-file storage or external-hosting requirement, and no external link is withheld. The derived `consolidated_observations.csv` is committed in full, together with the result CSVs, submission strings and figures, so the repository demonstrates its results without the private inputs.

**Licence and terms of use.** Code, notebooks and documentation are released under the **MIT Licence** (see [`LICENSE`](LICENSE)). Data is **not** covered by that licence: the raw challenge data is constrained by the academic rules of the capstone challenge and may not be redistributed, and the derived `consolidated_observations.csv` — together with the result CSVs and submission strings under `pipeline/` — is included solely so the reported results can be reproduced and inspected. It remains subject to the same academic terms and is not licensed for redistribution or reuse.

**IP or fees?** None.

### Maintenance

**Who maintains it?** Eduardo Wizentier — [wizentier@gmail.com](mailto:wizentier@gmail.com).

**How was it updated?** During the campaign, weekly: append one row to `inputs.txt` and one to `outputs.txt` — the only manual step in the loop — then re-run `04_consolidate_data.ipynb`, which rebuilds `consolidated_observations.csv` and `function_summary.csv` from scratch. Nothing downstream depends on a hand-edited record.

**Will it continue to be updated?** No. The campaign closed at Week 13 and the data set is final. The pipeline remains runnable on new rows should the challenge reopen.

**How can errors be reported?** By email to the address above, or via issues on the repository.

**Will older versions be retained?** The raw `inputs.txt` / `outputs.txt` are append-only and therefore constitute their own version history; every intermediate state is recoverable by truncation.

---

## Part 2: Model Card for the BBO Optimisation Approach

### Model details

| | |
|---|---|
| **Name** | Pathology-Aware BBO Suggestion Engine |
| **Type** | Gated two-tier diagnostic router feeding a pathology-routed Bayesian optimisation framework, with a single noise-aware referee surrogate pricing all candidates |
| **Version** | v2 — introduced Week 7, in service through Week 13 (campaign close) |
| **Card date** | 30 August 2026 |
| **Author / contact** | Eduardo Wizentier · [wizentier@gmail.com](mailto:wizentier@gmail.com) |
| **Licence** | MIT for code and documentation; data excluded — see [Part 1, Distribution](#distribution) |
| **Implementation** | `pipeline/05_suggest_engine_v2.ipynb` (classify → generate → price → constrain → submit), with `pipeline/06_diagnose.ipynb` (router), `pipeline/07_ceiling_estimator.ipynb` (denominators) and `pipeline/08_anti_hallucination_check.ipynb` (pre-submission critic) |

### Intended use

**Suitable tasks.** Optimising expensive, noisy, low-to-moderate-dimensional black-box functions under extremely tight query budgets — settings where a single query costs enough to justify spending real analysis effort deciding *what kind of problem you are facing* before choosing a method.

**Unsuitable tasks.** High-dimensional global optimisation; noiseless problems where analytical or gradient methods apply directly; settings requiring large batch queries; and any setting where a wrong query is cheap enough that diagnosis is not worth its cost.

**Out of scope entirely.** This engine does not generalise beyond the eight challenge functions without re-derivation. The archetype definitions were induced from these functions' own data. They are a working taxonomy for this problem, not a general taxonomy of optimisation landscapes.

### Factors

Performance varies systematically along four axes, and results should be read disaggregated by them rather than pooled.

| Factor | Range in this campaign | Why it matters |
|---|---|---|
| **Dimensionality** | 2-D to 8-D | Determines how badly the design undersamples the domain |
| **Noise regime** | Deterministic (F1, F4, F5, F7, F8) vs noisy (F2, F3, F6) | Determines whether a single high draw is signal or luck; only deterministic functions permit exact replicate verification |
| **Pathology archetype** | Six labels (below) | Directly selects the strategy module |
| **Data density** | 23–53 observations per function | Below roughly 30 observations, surrogate variance dominates and most structure claims are unfalsifiable |

**Archetypes are states, not identities.** The classifier is re-run from scratch every week, and functions do change label as evidence accumulates: F3 moved from `stochastic_capped` to `local_peak` after Week 9, and F6 passed through `plateau` in Weeks 4–6. §7 of `05_suggest_engine_v2` backtests the labels against the campaign's own history.

| Archetype | Signature in the data | Strategy | Members |
|---|---|---|---|
| `needle` | Magnitude cascade ≥6 decades, ≥50% background | Log-quadratic vertex fit + micro trust region | F1 |
| `stochastic_capped` | Best-ever is an early draw; nearby re-reads never re-attain it | Lottery: near-incumbent re-reads + maximin exploration | F2, F3 (to W9) |
| `local_peak` | New best-ever from a small step — a verified gradient | TuRBO-lite: continue ×1.5 on success, reverse-halve on failure | F2, F3, F4, F6 |
| `boundary_climb` | Incumbent pinned at bounds, strong monotone trends | Coordinate scans with capped extrapolation, priced on log scale | F5 |
| `plateau` | No new best for ≥3 weeks, not flat, not solved | Price escape hypotheses: separable optimum, anti-correlated pairs | F6 (W4–W6) |
| `solved_lock` | Analytic identity confirmed | ε-perturbation on the least-sensitive dimension | F7, F8 |

Every candidate is priced under one noise-aware referee GP using expected improvement and P(beat best-ever), with a global no-repeat guard applied before the submission string is built. Human overrides are supported and **logged** to `engine_provenance.csv`, never silent, so the engine's alternative remains in the record beside the human pick.

### Metrics

The primary and only headline metric is the **normalised best-ever score**:

$$\text{score} = \frac{f(x^*) - f_{\text{initial best}}}{f_{\text{true max}} - f_{\text{initial best}}}$$

**Percentage-of-ceiling is deliberately not reported.** It is a different quantity from the score above, and it is undefined for the three functions whose best values are negative: F6's −0.23475 against a ceiling of −0.2247 cannot meaningfully be expressed as a percentage of attainment. Every figure below is a normalised score.

**The denominator is estimated, not known.** $f_{\text{true max}}$ is unavailable, so `07_ceiling_estimator` supplies one estimator per archetype with `low = best-ever` always and an explicit uncertainty band. The basis for each ceiling is stated per function in the results table and surfaced in figure FR1 as a visible uncertainty whisker rather than buried in the arithmetic. A pathology-blind GP-UCB column is retained as a contrast: it hallucinates headroom precisely where the pathology-aware estimators say the game is over.

### Training and evaluation data

Both draw on the same source: `consolidated_observations.csv`, 279 observations across eight functions, weeks 0–13, rebuilt by `04_consolidate_data.ipynb` on every run. Full specification, provenance, sampling biases and known gaps are in Part 1.

There is no held-out test set, and manufacturing one would be wrong here — every observation cost a week and was immediately folded back into the model. Evaluation is therefore **walk-forward**: `08_anti_hallucination_check` scores each staged submission against data available *before* the result returned, with Axis C calibration resting on nine walk-forward weeks per function. This is the honest protocol for the setting and also a genuine weakness: nine points per function makes the calibration estimates themselves wide.

### Quantitative analyses — final results

| F | dim | kind | initial best | final best | found | records | ceiling (basis) | score |
|---|-----|------|--------------|------------|-------|---------|-----------------|-------|
| F1 | 2 | deterministic | ~0 | **1.99995** | W11 | 7 | 2.0 · hypothesised | 0.99998 |
| F2 | 2 | noisy | 0.6112 | **0.65048** | W10 | 2 | 0.70 · speculative | 0.4424 * |
| F3 | 3 | noisy | −0.03484 | **−0.00037** | W12 | 4 | 0.0 · hard cap | 0.98938 |
| F4 | 4 | deterministic | −4.0255 | **0.65487** | W13 | 6 | 0.6549 · best-ever | 0.99999 |
| F5 | 4 | deterministic | 1088.86 | **8662.48** | W9 | 6 | 8662.48 · corner | 1.00000 |
| F6 | 5 | noisy | −0.71426 | **−0.23475** | W10 | 3 | −0.2247 · low conf. | 0.97948 |
| F7 | 6 | deterministic | 1.36497 | **3.32237** | W1 | 3 | 3.32237 · analytic | 1.00000 |
| F8 | 8 | deterministic | 9.59848 | **10.00000** | W2 | 2 | 10.0 · analytic | 1.00000 |

**Mean normalised score 0.9955** across the seven functions with defensible ceilings.

\* **F2 is scored separately and must not be pooled into the mean.** Its true maximum cannot be usefully bounded: the seed "best" was itself an upward draw, and its own Week-3 replicate at the same input returned 0.5580. Its ceiling is marked speculative, so F2 carries a wide uncertainty whisker in FR1 (0.283–0.805) rather than being silently dropped or averaged in.

**Disaggregation by mechanism.** The score did not come from one method. Six distinct mechanisms produced it, which is the central finding of the project rather than an inconvenience:

| Function | What actually won it |
|---|---|
| F7, F8 | *Recognising* the function rather than searching it — analytic identities locked at W1 and W2 |
| F5 | Testing an axis that had been assumed rather than measured |
| F1 | A parametric model that extrapolated correctly four times running |
| F4 | A step that moved every coordinate at once, against the working prescription at the time |
| F3 | Banking a lucky draw and refusing to redraw it |
| F2 | Abandoning the seed region for one reading three sigma better |
| **F6** | **Not won.** Stalled after W3; its local geometry was never recovered. FR3's near-empty panel says so plainly |

**Detector calibration.** `08_anti_hallucination_check` reports Spearman ρ ≈ +0.45 (p ≈ 1.4e-5, n = 88) between its pre-result risk proxy and realised surprise. That is a positive but moderate association: the critic is informative, not decisive, and is documented throughout as a request for a second look rather than a veto.

### Assumptions and limitations

**The archetype taxonomy may be inadequate.** The routing system assumes six predefined pathology archetypes adequately capture these landscapes. They were induced from the data they now classify, so the assumption is not independently tested. A function whose behaviour falls between archetypes will be forced into the nearest one.

**Extreme data sparsity is the binding constraint.** At 23–53 observations in 2–8 dimensions, models are highly vulnerable to the optimiser's curse and to signal aliasing. The recurring finding across the entire neural track — `08_neural_surrogates_edu`, `09_neural_surrogates_F6`, `10_neural_surrogates_engine` — is that at this density the bottleneck is data, not model capacity, which is why the GP and structured pipeline remained the production route throughout despite deep-learning alternatives being built and benchmarked against it.

**Worked failure mode — F2 aliasing.** Ten initial points sampled across roughly 3.5 cycles of a candidate wave folded structure into apparent noise, misleading the strategy for weeks. `09_harmonic_study_F2` diagnosed this as an aliased sinusoid with an unsampled fourth peak near `x1 ≈ 0.98`, and stated in advance that a draw below ~0.45 there would falsify the harmonic reading outright. **The Week-11 probe returned 0.1885. The criterion fired and the harmonic reading was retired.** F2's banked best remains the Week-10 region-switch draw of 0.65048. The study is retained in the repository *because* it was wrong: a pre-registered criterion that fires against its own author is stronger evidence of method than one that is never tested.

**Known metadata drift — three sources, one authority.** Per-function metadata (dimension, hypothesis, status, log-scale flag) exists in three places: an inlined `FUNCTION_META` table in `diagnostics/A1_svm_analysis.ipynb`; a `FUNCTION_META` dictionary inside `04_consolidate_data.ipynb`, which propagates a `status` column into `function_summary.csv`; and the weekly classifier in `05_suggest_engine_v2`, which re-labels every function from scratch. The first two are hand-maintained and can go stale. **Where they disagree, the weekly classifier is authoritative.** An external reviewer should treat both hand-written tables as descriptive convenience, not as pipeline state. Note that `A1_svm_analysis` still attempts `from bbo_meta import FUNCTIONS` before falling back to its inlined copy; that module was folded into the notebooks and no longer exists, so the fallback is always the path taken.

**Label propagation.** Pathology labels are inherited from `05_suggest_engine_v2` by `08_anti_hallucination_check`, so any misclassification in the engine propagates uncorrected into the critic meant to audit it. The critic cannot catch the one class of error it shares with its subject.

**The risk score is a judgement call, not a fitted quantity.** `WEIGHTS` in `08_anti_hallucination_check` is exposed specifically so it can be argued with. Axis G returns `UNVERIFIABLE` for every claim shape it was not taught, which means *unchecked*, not clean.

**Ceilings are the softest numbers on the board.** F4's band is the widest: its vertex is not bracketed above, so the geometric asymptote is an extrapolation rather than a fit. F2's and F3's are latent-*mean* ceilings, which only lucky draws can exceed — and the scoring rule banks lucky draws.

### Ethical considerations and transparency

**No personal or human-subject data.** The data set consists entirely of numeric queries and machine-returned scalar responses. No personal, confidential or human-subject data is involved at any stage, and no individual can be identified from any part of it.

**Hallucination is treated as the primary integrity risk.** `08_anti_hallucination_check` scores each staged submission on seven axes — support, model agreement, calibration, headroom, stability, resolvability, rationale — each printing its own evidence. Decision flags are held deliberately *outside* the risk score, so that buying information is never penalised as an error.

**Overrides are logged, never silent.** Any human departure from the engine's suggestion is written to `engine_provenance.csv` alongside the machine alternative it displaced, so the record always shows what the engine would have done.

**Contradictions between notebooks are preserved deliberately.** This repository documents a learning process, so studies later overturned are retained rather than deleted or quietly corrected. The clearest case is the F2/F3 arc: `08_casino_case_study_v2` reaches a conclusion, and each of the two `09` studies overturns it on the same data plus later weeks, for reasons stated precisely enough to check. `09_transform_retrial_F3` rejected the earlier "log-transform is a trap" verdict — judged by out-of-sample predictive density in $y$-units with the Jacobian carried, the multiplicative-noise model beat the additive one by roughly 11.6 nats, making F3 a ~19:1 signal-to-noise function with banded structure rather than a flat casino. It named a low-toxicity corridor and priced the final probe as a free option; Week 12 set a record inside that corridor. **Readers meeting an apparent contradiction between notebooks should take the later-numbered study as the standing verdict and the earlier one as preserved reasoning, not as an uncorrected error.**

### Caveats and recommendations

**What this card does not license you to conclude.** These are eight observations of a method, not a benchmark. The mean of 0.9955 is computed over seven functions with *estimated* ceilings, each carrying a stated basis and band. F6 was not won, and no aggregate should be read as though it were.

**Recommended reading for anyone auditing the numbers.** Figure FR1 for the scoreboard with whiskers; FR3 for what the campaign's own observations imply about each landscape, as opposed to `A3_landscape_gallery`, which draws the *hypothesised* textbook benchmarks from published formulas; and `07_ceiling_estimator` for the fit behind every denominator.

**Known incomplete work.** The planned LLM strategist — a notebook reading the diagnostics (06), engine records (05) and ceilings (07) to propose each week's query with a written rationale — is intentionally not built. The hook exists: Axis G of `08_anti_hallucination_check` already accepts prose and returns each claim as `SUPPORTED`, `CONTRADICTED` or `UNVERIFIABLE`.
