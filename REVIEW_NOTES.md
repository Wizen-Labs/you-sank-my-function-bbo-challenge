# Review notes

Structural decisions and their rationale, plus the known limitations of the repository as
shipped. Newest first. No pass recorded here has ever changed an optimisation result —
they are structure, consistency and hygiene only.

---

# Final pass — campaign closed (weeks 0–12)

The campaign finished at Week 12: 271 observations, 96 weekly queries, 32 records. This
pass brought the documentation layer in line with the finished project and simplified the
repository root. **No notebook was edited.**

## Repository layout — what changed

- **`README.md` rewritten as a single entry point.** It now opens on the final scoreboard,
  routes assessors to `pipeline/00_final_capstone_report` first, and catalogues every
  notebook under its A/B/C/D section, including the three added at the end
  (`00_final_capstone_report`, `A4_clustering_unsupervised`, `A5_pca_dimensionality`).
- **`tools/` retired.** `pipeline/04_consolidate_data.ipynb` writes `function_summary.csv`
  on every run, so the project state is derived from the data rather than rendered into a
  separate document.
- **`STATE.md` deleted.** It existed only because `tools/render_state.py` kept it honest.
  Without the renderer it would have been a hand-maintained file duplicating
  `function_summary.csv` — precisely the drift the renderer was introduced to prevent.
  Read the CSV instead.
- **`bbo_meta.py` dropped from the documented layout.** A grep across all thirteen notebooks
  returns **zero imports**. Each notebook carries its own metadata: `04`, `07_run_week`, and
  `00` hold inline `FUNCTION_META`; `06` holds `PRIORS`; `05`, `07_ceiling`, both `08`s,
  `Preliminary` and `A5` derive `DIMS` from the CSV plus `LOCK_PRIOR`. The module is either
  dead or used only by `diagnostics/svm_analysis.py` — see limitation 5.
- **`report/` removed** from the documented layout; the figure notebooks write beside
  themselves unless `BBO_FIGURE_DIR` is set.
- **`data/` no longer part of the repository.** The raw challenge data is private and stays
  outside it entirely, located via `BBO_DATA_DIR`. This replaces the previous arrangement of
  a committed `data/README.md` behind an ignore rule, and removes a real hazard: the old
  `.gitignore` used `data/` with a `!data/README.md` negation, which cannot work — git does
  not descend into an excluded directory, so the negation never fires and `data/README.md`
  was silently excluded.
- **`.gitignore` reduced to four rules** (`.ipynb_checkpoints/`, `__pycache__/`, `.DS_Store`,
  `Thumbs.db`). With the data outside the repository there is nothing else to exclude; the
  checkpoint rule remains because Jupyter creates those folders automatically and would
  otherwise commit a duplicate copy of every notebook.
- **`REFERENCES.md` extended** with the methods introduced after Week 7 — EI, GP-UCB,
  Thompson sampling, the optimizer's curse, maximin designs, LOO predictive density,
  Box–Cox, heteroscedastic GPs, Lomb–Scargle, the sampling theorem, AICc and the BBOB/COCO
  taxonomy — plus a note separating cited primitives from the constructions that are
  original to this project.

## Resolved since the previous pass

- **F2's harmonic study was falsified by its own criterion, as intended.**
  `09_harmonic_study_F2` stated in advance that a draw below ~0.45 near `x1 ≈ 0.98` would
  kill the harmonic reading. The Week-11 probe returned **0.1885**. The criterion fired, the
  reading was retired, and `00_final_capstone_report` labels F2 a noisy ridge with its banked
  Week-10 best of 0.65048. This is no longer an open contradiction — it is the pre-registered
  test working, and the write-up should present it that way.
- **F3's transform retrial was vindicated.** `09_transform_retrial_F3` named a low-toxicity
  corridor and priced the final probe as a free option; Week 12 set a record inside that
  corridor, taking F3 from −0.0151 to **−0.00037** against a hard cap of 0.
- **F2 and F3 are no longer "contested".** Both were settled by data rather than by argument,
  which is the outcome the pre-registered criteria were there to produce.

---

## Known limitations of the repository as shipped

Ordered by how much each would cost if an assessor found it first. None affects a reported
score; all are internal-consistency issues in the committed notebooks.

1. **Three different sources for the ceilings, and they disagree.** F4 is 0.68 in
   `07_ceiling_estimator` and 0.6549 in `00_final_capstone_report`; F6 is −0.234 versus
   −0.2247. `07_run_week_and_report` carries a third, badly stale hardcoded `CEILINGS` dict
   — F1 at 1.00 against a final best of ~2.0, F5 at 5000 against 8662 — so figure B4's
   normalised scores are wrong. `00`'s values are the ones quoted in the README and the
   report. B4 should read `ceiling_estimates.csv` rather than holding its own copy.

2. **The two `09` studies narrate data the committed CSV does not contain.** The harmonic
   study's prose rests on two resample pairs and σ ≈ 0.027; its executed output finds one
   pair, σ = 0.0376, and `patch sd = nan`. The F3 retrial prints its own banner warning that
   the three-read cluster pinning the winner's-curse estimate is absent, and §4 falls back to
   a single-read estimate. Re-run both against the final export, or adjust the narratives to
   the data that ships.

3. **Windows absolute paths in `04`.** `DATA_DIR = os.path.join("..", "D:\Capstone
   Challange\initial_data")` — a malformed join, the long-standing "Challange" typo, and
   `C:\Users\USER\` in saved cell outputs. `BBO_DATA_DIR` is documented as the override, so
   the default should be a relative path.

4. **`04`'s inline `FUNCTION_META` is stale.** It still labels F3 `near_ceiling` and F2
   `uncertain`. F3 finished at −0.00037 against a cap of 0, and `05`'s data-driven classifier
   calls both `local_peak`. `07_run_week_and_report` reads this field to set the confidence
   column in its figures, so the staleness propagates.

5. **`bbo_meta.py` has no verified consumer.** Zero notebook imports. Grep
   `diagnostics/svm_analysis.py`; if that does not import it either, delete the module. If it
   does, the honest description is "metadata for the SVM diagnostics" rather than a project-
   wide source of truth.

6. **Navigation banners are stale.** They link to `05_suggest_engine.ipynb` and
   `05b_suggest_engine_v2.ipynb`, neither of which exists — the file is
   `05_suggest_engine_v2.ipynb`. `00_final_capstone_report`'s banner lists only A1–A3 under
   Diagnostics, omitting A4 and A5. Note also that the `_v2` suffix contradicts the earlier
   rule that filenames carry no version suffix because git holds the history; pick one
   convention and apply it.

7. **Numbering collides inside `pipeline/`:** two `07`s, two `08`s, two `09`s — and `neural/`
   independently holds `08`–`10`. Either renumber the deep-dive studies or move them to a
   `studies/` folder. The README groups them by role to compensate, which works for a reader
   but not for anyone running files by number.

8. **`REMAINING_WEEKS` disagrees across notebooks:** 5 (`07_ceiling_estimator`), 3
   (`08_casino`), 1 (`09_harmonic`), 1 (`09_transform`), against a 13-week season. Every
   option-pricing and lucky-draw allowance in those notebooks scales with this number. The
   campaign is closed so no decision depends on it now, but the figures those notebooks
   committed were produced under inconsistent assumptions and the values should be
   reconciled — or each notebook should state the week it was run.

9. **`08_anti_hallucination_check` keeps a verbatim copy of `05`'s classifier**, deliberately
   and with the trade-off documented in the notebook. Kept as a note rather than a defect: if
   `05`'s rules are ever changed, they must be changed in both places, or the audit critiques
   a strategy nobody used.

---

## Honesty notes for the write-up

- **The `09` notebooks overturn `08`, and that arc is the strongest methodological evidence
  in the repository.** Present it as a sequence — a conclusion, then the specific measurement
  that broke it — rather than shipping only the later verdict. "The exact-resample pair was
  the tiebreaker" and "the guard was a heuristic, the back-test is a measurement" are the two
  sentences that carry it.
- **Keep the study that turned out to be wrong.** `09_harmonic_study_F2` reached a conclusion
  the data then refuted. A pre-registered criterion that fires against its own author is
  better evidence of method than one that is never tested, and removing it would discard the
  clearest demonstration of the approach in the repository.
- **F2's score is reported separately for a stated reason.** Its ceiling is speculative — the
  seed "best" was itself an upward draw, and its own Week-3 replicate at the same input
  returned 0.5580 — so 0.4424 sits outside the headline mean of 0.9951 with a wide whisker
  rather than being quietly dropped. Say so explicitly; it is the most attackable number in
  the report and the defence is already in the notebook.
- **F6 was not won.** It stalled after W3 and its local geometry was never recovered. FR3's
  near-empty panel shows this honestly and the write-up should not smooth it over.
- **The `08` critic's self-check reports ρ ≈ +0.45 (p ≈ 1.4e-5, n = 88)** between the
  pre-result risk proxy and realised surprise. Real signal, modest effect, small n. The
  notebook labels itself a beta; keep that label.

---

# Earlier passes (historical)

## Week-7 release cleanup

- **Merged the two `07` notebooks** into `pipeline/07_run_week_and_report.ipynb` — the
  orchestrator followed by the report figures — and fixed its stale reference to
  `05_suggest_engine_v4-w4.ipynb`. *(The duplicate-`07` numbering has since returned; see
  limitation 7.)*
- **De-duplicated the suggestion engine.** Kept one canonical engine, deleted the Week-4
  fossil, restored its navigation banner.
- **Renamed** `10_neural_surrogates_engine_F2_F4_F6.ipynb` →
  `neural/10_neural_surrogates_engine.ipynb`: its `CONFIG` covers F2 · F4 · F5.
- **Added `bbo_meta.py`** to centralise per-function metadata, replacing hard-coded tables
  that still named refuted hypotheses. *(Superseded — no notebook imports it; see
  limitation 5.)*
- **Added `tools/render_state.py`** to rebuild `STATE.md` from `function_summary.csv`.
  *(Superseded — `tools/` and `STATE.md` are both gone; `04` writes the CSV directly.)*
- **Hygiene:** a common A/B/C/D navigation banner on every notebook, and Windows absolute
  paths scrubbed from committed outputs. *(Both regressed; see limitations 3 and 6.)*
