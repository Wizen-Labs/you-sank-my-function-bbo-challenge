# Datasheet and Model Card: BBO Capstone Project

## Part 1: Datasheet for the BBO Capstone Data Set

### Motivation
* **Why was it created?** This data set was created for the Imperial College Business School Bayesian Optimisation Challenge to track iterative query history and function evaluations across eight hidden black-box functions.
* **What task does it support?** It supports the task of maximizing each function's normalized best-ever score by providing the historical evidence needed to train local surrogate models, identify pathology archetypes, and estimate performance ceilings.

### Composition
* **What does it contain?** It contains the historical queries (inputs mapped to a unit cube $[0,1]^d$, ranging from 2-D to 8-D) and their corresponding noisy scalar responses.
* **Size and format:** As of Week 11, the dataset size ranges from 21 to 51 observations per function. The data is structured into `consolidated_observations.csv`, which is built from raw `inputs.txt` and `outputs.txt` logs.
* **Are there any gaps?** Yes, the data suffers from severe spatial undersampling and exploitation bias. Because the acquisition functions naturally favor exploiting known peaks, vast tracts of the search space remain completely unexplored. For example, F1's data is tightly clustered near `[0.628, 0.628]`, and F5's best observations are pinned exactly at the bounds of the unit cube.

### Collection Process
* **How were queries generated?** Queries were generated at a strict rate of one query per function per week, with a one-week turnaround for the noisy scalar responses from the challenge portal.
* **What strategy was used?** The collection strategy followed a "diagnose first, then choose the method" philosophy. Data signatures (like magnitude cascades or rank-correlation fingerprints) informed the pathology archetype, which then dictated the specific query strategy.
* **Time frame:** The data collection spans from Week 1 to Week 11 (with Week 12 currently staged).

### Preprocessing and Uses
* **Transformations applied:** Some functions required variance-stabilizing transforms to make the data usable. For example, a log-transform ($z = \log(-y)$) was applied to F3, carrying the Jacobian to properly handle multiplicative noise.
* **Intended uses:** The data is intended to test hypotheses for BBO routing, train Gaussian Process (GP) surrogates, and run the `08_anti_hallucination_check` critic to price candidate probes.
* **Inappropriate uses:** It would be highly inappropriate to use this data set to definitively characterize the global landscape of these functions. The sample size is simply too small, and the sampling method is heavily biased toward local regions and early successes.

### Distribution and Maintenance
* **Where is it available?** The raw challenge data is kept private in a local `data/` folder and is intentionally not committed to the repository.
* **Terms of use:** Constrained by the academic rules of the capstone challenge.
* **Maintenance:** The data set is maintained by the author. It is updated weekly through the `04_consolidate_data.ipynb` notebook, which appends new rows from the portal to the consolidated CSV.

---

## Part 2: Model Card for the BBO Optimisation Approach

### Overview
* **Name:** Pathology-Aware BBO Suggestion Engine
* **Type:** Gated two-tier diagnostic router and Bayesian Optimization framework.
* **Version:** v2 (introduced in Week 7, updated through Week 11).

### Intended Use
* **Suitable tasks:** Optimizing expensive, noisy, low-dimensional black-box functions constrained by extremely tight query budgets.
* **Unsuitable tasks:** High-dimensional global optimization, noiseless functions where pure analytical gradient methods apply, or scenarios that require large batch queries.

### Details
* **Strategy across ten rounds:** The approach evolved significantly over the rounds. Initially reliant on hand-written records, Week 7 introduced an automated generalized routing engine (`05_suggest_engine_v2`). The engine classifies each function into one of six pathology archetypes (`needle`, `stochastic_capped`, `local_peak`, `boundary_climb`, `plateau`, `solved_lock`) using the weekly data.
* **Techniques used:** The assigned archetype routes the function to a specific strategy module—utilizing methods like TuRBO-lite, coordinate scans, micro trust regions, and harmonic least-squares periodograms. Finally, every candidate probe is priced by a single referee surrogate using Expected Improvement (EI) and the probability of beating the best-ever score, while enforcing a global no-repeat guard.

### Performance
* **Metrics:** The primary metric is the normalized best-ever score: `score = (f(x*) - f_initial_best) / (f_true_max - f_initial_best)`.
* **Results across eight functions:** As of Week 11, the engine has achieved 100% of the estimated ceiling for F1, F2, F3, F6, F7, and F8. For the remaining active functions, it has reached 91% of the estimated ceiling for F5 and 99% for F4. Notably, the analytic identities for F7 and F8 were locked early on (Week 1 and Week 2, respectively).

### Assumptions and Limitations
* **Assumptions:** The entire routing system relies on the assumption that the six predefined pathology archetypes adequately capture the true nature of the black-box search space.
* **Constraints and failure modes:** The most significant limitation is computational reality under extreme data sparsity. With only 21 to 51 observations per function, the models are incredibly vulnerable to the Optimizer's Curse and signal aliasing. A prime example of this failure mode is F2: 10 initial points sampled across 3.5 cycles of a wave folded a deterministic wave into apparent noise, misleading the optimization strategy for weeks before a harmonic analysis corrected it.

### Ethical Considerations & Transparency
* **Transparency and Reproducibility:** To ensure the process is credible, the pipeline features an `08_anti_hallucination_check` critic. This notebook explicitly scores how much of a proposed strategy is backed by hard data rather than a model asserting things the data does not actually say. Furthermore, any human overrides to the engine's suggestions are explicitly logged so the automated alternative remains permanently in the record.
* **Improving the Model Card:** While the current model card structure successfully captures the high-level logic, documenting codebase discrepancies improves its usefulness for an external reviewer. Explicitly noting metadata drift (e.g., between the static `bbo_meta.py` file and the dynamic classifier) or noting hardcoded artifacts prevents auditors from being confused by internal contradictions.
