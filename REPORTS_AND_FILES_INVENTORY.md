# File Inventory — "You Sank My Function" Capstone

**Generated artefact manifest for the 19 Jupyter notebooks + `README.md`.**

This document lists every file written to disk by the notebooks in this repository: which notebook creates it, what it contains, and any conditions attached to it. It is an inventory derived from the `savefig` / `to_csv` / `open(...,"w")` calls in each notebook's code cells — no code behaviour was analysed beyond identifying the write targets.

| | |
|---|---|
| Source files catalogued | 20 (1 `README.md` + 19 `.ipynb`) |
| Notebooks that write files | 16 of 19 |
| Notebooks that write nothing | 3 (the entire neural track) |
| Total generated artefacts | **88** |
| — PNG figures | 60 |
| — CSV tables | 26 |
| — TXT submission strings | 1 |
| — Markdown reports | 1 |

---

## 1 · Source files catalogued

### 1.1 · Documentation

| File | Type | Role | Generates |
|---|---|---|---|
| `README.md` | Markdown | Repository front page — scoreboard, repo map, methodology, pathology archetype table, weekly-loop mermaid diagram, reproduction instructions, reading order. Hand-maintained, not notebook-generated. | — (input/reference only) |

### 1.2 · Notebooks — Pipeline (B)

| Notebook | Role | Outputs |
|---|---|---|
| `00_final_capstone_report.ipynb` | Campaign retrospective — five A3 landscape sheets | 6 |
| `04_consolidate_data.ipynb` | Raw sources → single tidy observation table | 2 |
| `Preliminary_Pattern_Analysis.ipynb` | Label-blind re-read of all eight functions | 2 |
| `06_diagnose.ipynb` | Gated two-tier diagnostic router + method audit | 1 |
| `05_suggest_engine_v2.ipynb` | Pathology → strategy → referee → submission string | 3 |
| `07_ceiling_estimator.ipynb` | Predicted maximum per function, with bands | 4 |
| `08_anti_hallucination_check.ipynb` | Seven-axis critic of the staged submission | 4 |
| `07_run_week_and_report.ipynb` | Orchestrator (04→06→05) + weekly figures B1–B5 | 5 direct (+ inherits 04/06/05 outputs) |
| `08_casino_case_study_v2.ipynb` | F2/F3 winner's-curse forensics + policy tournament | 11 |
| `09_harmonic_study_F2.ipynb` | F2 aliasing retrial | 14 |
| `09_transform_retrial_F3.ipynb` | F3 multiplicative-noise retrial | 9 |

### 1.3 · Notebooks — Diagnostics (C)

| Notebook | Role | Outputs |
|---|---|---|
| `A1_svm_analysis.ipynb` | SVR/SVC learnability, relevance, direction | 7 |
| `A2_logistic_regression.ipynb` | Top-vs-rest separability cross-check | 1 |
| `A3_landscape_gallery.ipynb` | 2-D slices of hypothesised benchmarks | 1 |
| `A4_clustering_unsupervised.ipynb` | K-Means · Ward · DBSCAN, scored against `y` | 6 |
| `A5_pca_dimensionality.ipynb` | PCA · PLS · active subspaces · intrinsic dimension | 12 |

### 1.4 · Notebooks — Neural (D)

| Notebook | Role | Outputs |
|---|---|---|
| `08_neural_surrogates_edu.ipynb` | MLP / deep ensembles / DNGO / CNN vs GP (educational) | **0** |
| `09_neural_surrogates_F6.ipynb` | Build-and-ship nets for F6 (TF/Keras) | **0** |
| `10_neural_surrogates_engine.ipynb` | Config-driven NN engine (F2 · F4 · F5) | **0** |

All three read `consolidated_observations.csv` and render figures inline only — no `savefig`, no `to_csv`, no model checkpoints persisted.

---

## 2 · Generated files by notebook

### `00_final_capstone_report.ipynb` — 6 files

Writes into `OUT_DIR`, which is `$BBO_FIGURE_DIR` or `.` if unset. The directory is created with `os.makedirs(..., exist_ok=True)`.

| File | Type | Purpose |
|---|---|---|
| `FR1_final_scoreboard.png` | PNG · 140 dpi | Headline numbers; normalised score per function with ceiling-uncertainty whiskers |
| `FR2_campaign_evolution.png` | PNG · 140 dpi | Running best as a fraction of each ceiling, week by week + ledger of every query that paid |
| `FR3_best_design_gallery.png` | PNG · 140 dpi | One landscape panel per function; surrogate sliced through the winning design. Dark-background figure (`facecolor=DARK_BG`) — the only one in the set |
| `FR4_best_designs_evidence.png` | PNG · 140 dpi | Winning input vector for all eight functions beside replicate evidence (deterministic vs noisy) |
| `FR5_lessons.png` | PNG · 140 dpi | Strengths, deviations, lessons — every claim measured from the data |
| `final_campaign_summary.csv` | CSV | The scoreboard as a table; the numeric backing for FR1 |

### `04_consolidate_data.ipynb` — 2 files

The hub of the pipeline. Regenerated on every weekly run so downstream state is always derived from data.

| File | Type | Purpose |
|---|---|---|
| `consolidated_observations.csv` | CSV | **The single tidy observation table** — initial designs + all weekly rows, all 8 functions. Read by nearly every other notebook in the repo. Path overridable via `$BBO_CONSOLIDATED_CSV` |
| `function_summary.csv` | CSV | Per-function roll-up (counts, best-ever, dimensionality). Rewritten every run — the project's state-of-play snapshot |

### `05_suggest_engine_v2.ipynb` — 3 files

`N_WEEKS` is read from the data (`OBS.week.max()`), so the submission filename is dynamic — a full 13-round campaign yields `week13_engine_submission.txt`.

| File | Type | Purpose |
|---|---|---|
| `week{N+1}_engine_submission.txt` | TXT | The official portal submission string for the upcoming week. Filename increments each run |
| `engine_summary.csv` | CSV | Per-function archetype, chosen strategy, candidate and its price under the referee GP |
| `engine_provenance.csv` | CSV | Provenance log — every candidate's origin string, plus any human override (logged, never silent) |

### `06_diagnose.ipynb` — 1 file

| File | Type | Purpose |
|---|---|---|
| `diagnosis_report.csv` | CSV | Tier-0/Tier-1 verdict per function, including `redirect` flags where fresh data contradicts the standing method. "Insufficient evidence — keep current method" is a first-class value |

### `07_ceiling_estimator.ipynb` — 4 files

| File | Type | Purpose |
|---|---|---|
| `ceiling_evidence_gallery.png` | PNG · 130 dpi | The fit behind each ceiling number, one panel per function |
| `ceiling_convergence.png` | PNG · 130 dpi | How each ceiling estimate moved as observations accumulated |
| `ceiling_headroom.png` | PNG · 130 dpi | Remaining headroom per function — feeds probe allocation |
| `ceiling_estimates.csv` | CSV | Predicted maximum per function with low/high band; `low = best-ever` always. Retains a pathology-blind GP-UCB column as contrast. **Consumed by `08_anti_hallucination_check`** |

### `07_run_week_and_report.ipynb` — 5 files (direct)

Pure orchestration: it runs the real 04/06/05 in fixed order and reads their file outputs, holding no per-function metadata of its own. Running it therefore also produces everything listed under 04, 06 and 05 above.

| File | Type | Purpose |
|---|---|---|
| `figure_B1_output_progression.png` | PNG · 130 dpi | Output progression across weeks |
| `figure_B2_ranking_evolution.png` | PNG · 130 dpi | Ranking evolution against initial best |
| `figure_B3_dashboard.png` | PNG · 130 dpi | Weekly dashboard view |
| `figure_B4_scoreboard.png` | PNG · 130 dpi | Scoreboard with ceilings overlaid |
| `figure_B5_trajectories.png` | PNG · 130 dpi | Per-function trajectories, symlog y-scale |

### `08_anti_hallucination_check.ipynb` — 4 files

`TARGET_WEEK = N_WEEKS + 1`, so all four filenames carry the week number.

| File | Type | Purpose |
|---|---|---|
| `hallucination_audit_week{W}.png` | PNG · 130 dpi | Seven-axis audit visual for the staged submission |
| `hallucination_calibration_week{W}.png` | PNG · 130 dpi | Calibration of the pre-result risk proxy against realised surprise |
| `hallucination_audit_week{W}.csv` | CSV | Per-function axis scores and flags |
| `hallucination_audit_week{W}.md` | **Markdown** | Written narrative audit — summary table, per-function critique blocks, detector self-check (Spearman ρ), and standing caveats. Written with explicit `encoding="utf-8"` because the report contains ρ, κ and σ, which Windows `cp1252` cannot represent |

### `08_casino_case_study_v2.ipynb` — 11 files

`STUDY_FUNCTIONS = [2, 3]`; the Section-9 forward-policy block is F2 only (`F_T = 2`).

| File | Type | Purpose |
|---|---|---|
| `f2_ledger.png` | PNG · 120 dpi | F2 observation ledger |
| `f2_ensemble.png` | PNG · 120 dpi | Ensemble posterior over F2 |
| `f2_winners_curse.png` | PNG · 120 dpi | Winner's-curse forensics — why the seed best was an upward draw |
| `f2_cap.png` | PNG · 120 dpi | Cap / ceiling reading for F2 |
| `f2_tournament.png` | PNG · 120 dpi | Policy tournament results |
| `f2_forward_policy.png` | PNG · 120 dpi | Forward policy plan (Section 9 stress tests) |
| `tournament_F2.csv` | CSV | Full policy-tournament results, F2 |
| `tournament_F3.csv` | CSV | Full policy-tournament results, F3 |
| `tournament_summary_F2.csv` | CSV | Aggregated tournament summary, F2 (written with index) |
| `tournament_summary_F3.csv` | CSV | Aggregated tournament summary, F3 (written with index) |
| `forward_policy_F2.csv` | CSV | Week-by-week forward plan for F2 |

### `09_harmonic_study_F2.ipynb` — 14 files

The study whose pre-registered falsification criterion fired against its own hypothesis.

| File | Type | Purpose |
|---|---|---|
| `f2h_ledger.png` | PNG · 120 dpi | F2 ledger, harmonic-study framing |
| `f2h_x2_irrelevance.png` | PNG · 120 dpi | Evidence that `x2` carries no signal |
| `f2h_frequency_scan.png` | PNG · 120 dpi | Frequency scan behind the aliasing hypothesis |
| `f2h_model_tournament.png` | PNG · 120 dpi | Competing model forms compared |
| `f2h_fit.png` | PNG · 120 dpi | The fitted `a + b·x1 + A·sin(ω·x1 + φ)` model |
| `f2h_gp_confirmation.png` | PNG · 120 dpi | Independent GP cross-check of the harmonic reading |
| `f2h_backtest.png` | PNG · 120 dpi | Walk-forward back-test of the model |
| `f2h_decision.png` | PNG · 120 dpi | Decision curve — E[draw] and P(beat) across `x1` |
| `f2h_forward_policy.png` | PNG · 120 dpi | Probe plan across the bootstrap CI for the peak location |
| `forward_policy_F2_harmonic.csv` | CSV | Per-week plan: `x1`, `x2`, `E_draw`, `P_beat`, rationale string |
| `model_F2_harmonic.csv` | CSV | Fitted parameters — a, b, A, φ, ω, period, RMSE, R², σ_noise, `x2_relevant` |
| `decision_curve_F2.csv` | CSV | The decision curve as a table |
| `model_tournament_F2.csv` | CSV | Model-form tournament scores |
| `backtest_F2.csv` | CSV | Back-test rows behind the extrapolation-bias estimate |

Cell 34 re-checks all nine PNGs on disk with `os.path.exists` and prints `ok` / `MISSING` per file.

### `09_transform_retrial_F3.ipynb` — 9+ files

| File | Type | Purpose |
|---|---|---|
| `f3_noise_model.png` | PNG · 120 dpi | Additive vs multiplicative noise model comparison |
| `f3_structure.png` | PNG · 120 dpi | Banded structure recovered under the log transform |
| `f3_ensemble.png` | PNG · 120 dpi | Ensemble posterior over F3 |
| `f3_tournament.png` | PNG · 120 dpi | Policy tournament results |
| `f3_forward_policy.png` | PNG · 120 dpi | Low-toxicity corridor and the priced final probe |
| `forward_policy_F3.csv` | CSV | Week-by-week forward plan for F3 |
| `candidates_F3.csv` | CSV | The full candidate portfolio considered |
| `tournament_F3.csv` | CSV | Full tournament results (note: same filename as one written by `08_casino_case_study_v2` — see §5) |
| `tournament_summary_F3_w{w}.csv` | CSV | **One file per horizon** — the loop iterates `SUMMARY.items()`, keyed on `REMAINING_WEEKS` and `3`. Written with index |

### `A1_svm_analysis.ipynb` — 7 files

The only notebook that writes into a subdirectory: cell 4 runs `os.makedirs("figures", exist_ok=True)` and the plot cells target `figures/`. CSVs land in the notebook directory.

| File | Type | Purpose |
|---|---|---|
| `figures/svr_learnability.png` | PNG · 130 dpi | SVR learnability per function |
| `figures/importance_heatmap.png` | PNG · 130 dpi | Per-dimension relevance heatmap |
| `figures/direction_heatmap.png` | PNG · 130 dpi | Per-dimension direction of effect |
| `figures/svc_decision_2d.png` | PNG · 130 dpi | SVC decision boundary, 2-D functions |
| `figures/svc_f8_projection.png` | PNG · 130 dpi | F8 projection under the classifier |
| `svm_diagnostics.csv` | CSV | Learnability / relevance summary, all 8 functions |
| `svm_directional_summary.csv` | CSV | Per-dimension directional summary, concatenated F1–F8 with `function` and `dim_name` columns prepended |

### `A2_logistic_regression.ipynb` — 1 file

| File | Type | Purpose |
|---|---|---|
| `logistic_regression_analysis.png` | PNG | Top-vs-rest separability cross-check — the notebook's single composite figure |

### `A3_landscape_gallery.ipynb` — 1 file

| File | Type | Purpose |
|---|---|---|
| `benchmark_functions.png` | PNG · 150 dpi | 2-D slices of the hypothesised benchmark landscapes, drawn from published formulas. The counterpart to FR3, which draws what the campaign's own data implies |

### `A4_clustering_unsupervised.ipynb` — 6 files

All PNG · 140 dpi. Each save is followed by a `✓ Saved …` confirmation print.

| File | Type | Purpose |
|---|---|---|
| `clustering_fig1_elbow_silhouette.png` | PNG | K-selection: geometric elbow + silhouette |
| `clustering_fig2_cluster_profiles.png` | PNG | Cluster profiles against `y` |
| `clustering_fig3_pca_gallery.png` | PNG | Partitions viewed in PCA space |
| `clustering_fig4_dendrograms.png` | PNG | Ward hierarchical clustering + cophenetic correlation |
| `clustering_fig5_leakage_experiment.png` | PNG | §6's deliberate worked mistake — clustering on `[X | y]` is circular |
| `clustering_fig6_dbscan.png` | PNG | DBSCAN with swept `eps`; noise label marks thin design regions |

### `A5_pca_dimensionality.ipynb` — 12 files

All PNG · 120 dpi, all written with an explicit `facecolor=BG`. The largest single figure set in the repository.

| File | Type | Purpose |
|---|---|---|
| `pca_fig1_y_transforms.png` | PNG | Effect of `y` transforms |
| `pca_fig2_geometry_2d.png` | PNG | Hand-derived PCA geometry on F2 |
| `pca_fig3_scree_gallery.png` | PNG | Scree plots + retention under four rules and Horn's parallel analysis |
| `pca_fig4_design_vs_search.png` | PNG | §6 — separates the design's own anisotropy from the optimiser's footprint |
| `pca_fig5_loadings.png` | PNG | Bootstrap intervals on loadings; sparse PCA |
| `pca_fig6_variance_vs_relevance.png` | PNG | Variance direction vs the directions that matter |
| `pca_fig7_active_subspace.png` | PNG | PLS and active subspaces — the methods that use `y` on purpose |
| `pca_fig8_kernel_pca_circles.png` | PNG | Kernel PCA on a synthetic control |
| `pca_fig9_kernel_gamma_sweep.png` | PNG | Kernel γ sensitivity sweep |
| `pca_fig10_embedding_gallery.png` | PNG | Isomap / MDS / t-SNE benchmarked against a random projection |
| `pca_fig11_curse_of_dimensionality.png` | PNG | Intrinsic dimension, Two-NN estimator |
| `pca_fig12_downstream.png` | PNG | §8 — classifies each PC1–`y` association as genuine, search-induced, or inconclusive |

### `Preliminary_Pattern_Analysis.ipynb` — 2 files

Both written **with** the index (function ID is the index).

| File | Type | Purpose |
|---|---|---|
| `preliminary_pattern_analysis.csv` | CSV | Landscape fingerprint joined to cross-validated closed-form screen results (`cv_`-prefixed columns) |
| `benchmark_classification.csv` | CSV | Classification + evidence per function: nearest benchmark family, confidence, BBOB-style descriptor. The notebook is explicit that the family *name* is a signature-level annotation, not an identification |

---

## 3 · Consumed inputs (read, never written)

| File | Read by | Notes |
|---|---|---|
| `inputs.txt` / `outputs.txt` | `04`, `07_run_week_and_report` | Cumulative weekly portal results, one row per week. The only manual step in the loop. `weekly_inputs.txt` / `weekly_outputs.txt` accepted as an alternate naming |
| `function_N/initial_inputs.npy`, `initial_outputs.npy` | `04` | Per-function initial designs, layout A |
| `f{N}_data.csv` | `04` | Per-function initial designs, layout B — both layouts supported |
| `consolidated_observations.csv` | `00`, `05`, `06`, `07`×2, `08`×3, `09`×2, `10`, `A1`, `A2`, `A4`, `A5`, `Preliminary` | Written by `04`. **The hub** — 16 notebooks read it |
| `consolidated_observations_F2_W10_extra.csv` | `09_harmonic_study_F2` | Supplementary F2 rows |
| `consolidated_observations_F3_W9_Extra.csv` | `09_transform_retrial_F3` | Supplementary F3 rows |
| `ceiling_estimates.csv` | `08_anti_hallucination_check` | Written by `07_ceiling_estimator` |
| `week*_engine_submission.txt` | `08_anti_hallucination_check` | Written by `05` — the staged string under audit |
| `diagnosis_report.csv`, `function_summary.csv` | `07_run_week_and_report` | Written by `06` and `04` |
| `submission.txt` | `07_run_week_and_report` | Read **only if present**; the code comments note "used only if 05 writes one". No notebook in this set writes it — `05` writes the week-numbered variant instead |

The raw sources (`inputs.txt`, `outputs.txt`, initial designs) are private and live outside the repository, located via `$BBO_DATA_DIR`.

---

## 4 · Path conventions & environment overrides

All paths are relative, with environment-variable overrides:

| Variable | Default | Affects |
|---|---|---|
| `BBO_DATA_DIR` | `<pipeline>/../data` | Where raw initial designs and cumulative weekly files are read from |
| `BBO_CONSOLIDATED_CSV` | `consolidated_observations.csv` | Location of the consolidated table |
| `BBO_FIGURE_DIR` | `.` | `OUT_DIR` for `00_final_capstone_report` only |
| `BBO_DATA_FILE` | `consolidated_observations.csv` | Used by the `A2`/`A4`/`A5` diagnostics notebooks |
| `BBO_PIPELINE_DIR` | auto-discovered | Used by `07_run_week_and_report` to locate the pipeline |

Every notebook except `00` and `A1` writes flat into its own working directory. `00` honours `BBO_FIGURE_DIR`; `A1` creates and writes into a `figures/` subdirectory.

---

## 5 · Notes and collisions worth flagging

**`tournament_F3.csv` is written by two notebooks.** Both `08_casino_case_study_v2.ipynb` (via its `STUDY_FUNCTIONS = [2, 3]` loop) and `09_transform_retrial_F3.ipynb` write a file of this exact name. If both are run in the same directory, the second to run silently overwrites the first. The same is *not* true of the summaries: `08` writes `tournament_summary_F3.csv` while `09` writes week-suffixed `tournament_summary_F3_w{w}.csv`.

**Three filenames are dynamic** and depend on the data present at run time:

- `week{N_WEEKS+1}_engine_submission.txt` — `N_WEEKS = OBS.week.max()`
- `hallucination_audit_week{TARGET_WEEK}.*` — `TARGET_WEEK = N_WEEKS + 1` (four files)
- `tournament_summary_F3_w{w}.csv` — one file per key in `SUMMARY`, i.e. per distinct horizon in `TOURN.weeks`

**The neural track (D) is read-only.** `08_neural_surrogates_edu`, `09_neural_surrogates_F6` and `10_neural_surrogates_engine` load `consolidated_observations.csv` and produce inline figures only. No PNGs, no CSVs, and no persisted model weights — no `.h5`, `.keras`, `.npy`, `.pkl` or `.joblib` artefacts anywhere in the repository.

**Only one Markdown file is notebook-generated:** `hallucination_audit_week{W}.md`. `README.md`, `REFERENCES.md`, `REVIEW_NOTES.md` and `DATASHEET_AND_MODEL_CARD.md` are hand-maintained.

**Everything regenerates.** Per the README, the result CSVs, submission strings and figures under `pipeline/` are committed deliberately so the repository shows its results without the private raw data — and all of them are reproduced on re-execution.
