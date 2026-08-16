# Review notes

What changed at each release pass, and why. Newest first. Nothing in the optimisation
results has ever been changed by one of these passes — they are structure, consistency
and hygiene only.

---

# Week-11 pass — documentation resync

The pipeline moved substantially between Weeks 7 and 11: the suggestion engine was
generalised, four new notebooks were added, and `tools/` was removed. The Markdown layer
had not kept up. This pass updated the docs only; **no notebook was edited**.

## Documentation changes

- **`README.md` rewritten.** It described a Week-7 state: eight hand-written `RECORDS`, a
  status board seven weeks stale, and a `tools/` directory that no longer exists. It now
  documents the archetype router, the four new notebooks, and the Week-11 → Week-12 board.
- **`STATE.md` re-derived at Week 11** and re-labelled honestly. `tools/render_state.py` was
  what made it auto-generated; with `tools/` gone it is a hand-maintained snapshot of
  `pipeline/function_summary.csv`, and the header now says so. **Either refresh it on the
  same command as the weekly run, or delete it** — a stale state doc is precisely the drift
  the renderer was introduced to prevent.
- **`REFERENCES.md` extended** with the twelve methods introduced in the Week 8–11 notebooks
  (EI, GP-UCB, Thompson sampling, the optimizer's curse, maximin designs, LOO predictive
  density, Box–Cox, heteroscedastic GPs, Lomb–Scargle, the sampling theorem, AICc, and the
  BBOB/COCO taxonomy), plus a note distinguishing cited primitives from the constructions
  that are original to this project.

## What the pipeline gained since Week 7 (for the record)

- **`05_suggest_engine_v2`** replaces the per-function `RECORDS` with a classifier over six
  pathology archetypes, a strategy library, one referee surrogate that prices every
  candidate, and a global no-repeat guard. The classifier is re-run weekly and backtested
  against the campaign's own history in §7.
- **`07_ceiling_estimator`** estimates the *denominator of the grade* per archetype, with
  uncertainty bands and a naive GP-UCB contrast column.
- **`08_anti_hallucination_check`** audits the staged submission on seven axes before it goes
  to the portal, with decision flags kept deliberately out of the risk score.
- **`Preliminary_Pattern_Analysis`** re-reads all eight functions label-blind and flags where
  the prior looks like a story the numbers do not support.
- **`08_casino_case_study_v2`, `09_harmonic_study_F2`, `09_transform_retrial_F3`** — forensic
  treatments of F2 and F3, each `09` overturning `08` on the same data plus later weeks.

## Outstanding — notebook-side, not fixed here

Ordered by how much they would cost if an assessor found them first.

1. **F2's harmonic study contradicts its own falsification criterion.** §10 states in advance
   that "a draw below ~0.45 kills the harmonic altogether and reinstates notebook 08's
   reading." The Week-11 probe at `x1 = 0.975` returned **0.1885** against a predicted 0.8953
   — it is in the notebook's own §8 back-test table. The forward policy still recommends
   `x1 = 0.99`. Either revise the criterion with a stated reason, or revise the conclusion.
   Pre-registering falsification criteria only earns credit if they are honoured.
2. **Both `09` studies narrate data the committed CSV does not contain.** The harmonic study's
   prose rests on two resample pairs and σ ≈ 0.027; its executed output finds **one** pair,
   σ = 0.0376, and `patch sd = nan`. The F3 retrial prints its own banner warning that the
   three-read cluster pinning the winner's curse is absent, and §4 falls back to a
   single-read model estimate. Re-run both on the newer export, or rewrite the narratives to
   match the data that ships.
3. **Windows absolute paths are back in `04`.** `DATA_DIR = os.path.join("..", "D:\Capstone
   Challange\initial_data")` — a malformed join, the old "Challange" typo, and
   `C:\Users\USER\` in the saved outputs. The Week-7 pass scrubbed these; they have returned.
4. **`CEILINGS` in `07_run_week_and_report` is hardcoded and stale.** F1 at 1.00 against a best
   of ~2.0, F5 at 5000 against 8662, and a comment asserting F2 has no gain. Figure B4's
   normalised scores are therefore wrong. It should read `ceiling_estimates.csv` from
   `07_ceiling_estimator` instead of carrying its own copy — the same single-source-of-truth
   argument that motivated `bbo_meta.py`.
5. **`REMAINING_WEEKS` disagrees across notebooks:** 5 (`07_ceiling_estimator`), 3
   (`08_casino`), 1 (`09_harmonic`), 1 (`09_transform`). The season is described as 13 weeks
   in the report half of `07_run_week_and_report` and as running to week 15 in the F3 retrial.
   Every option-pricing and lucky-draw allowance in those notebooks depends on this number.
6. **Numbering collides.** `pipeline/` now holds two `07`s, two `08`s and two `09`s, and
   `neural/` independently holds `08`–`10`. Either renumber the deep-dive studies or move them
   to a `studies/` folder; the README currently groups them by role to compensate.
7. **Navigation banners are stale.** They link to `05_suggest_engine.ipynb` and
   `05b_suggest_engine_v2.ipynb`, neither of which exists — the real file is
   `05_suggest_engine_v2.ipynb`. None of the banners mention the four new notebooks. Note
   also that the `_v2` suffix contradicts the Week-7 rule that filenames carry no version
   suffix because git holds history; pick one convention.
8. **Metadata drift has re-opened.** `04`'s inline `FUNCTION_META` still labels F2 "uncertain"
   and F3 "near_ceiling" while `05`'s data-driven classifier calls both `local_peak`. `05_v2`
   no longer needs `bbo_meta.py` at all (it derives everything from the data plus
   `LOCK_PRIOR`), so decide whether `bbo_meta` remains canonical or is retired with the
   RECORDS it was built to mirror.
9. **`08_anti_hallucination_check` keeps a verbatim copy of `05`'s classifier**, by design and
   with the trade-off documented in the notebook. Worth a one-line reminder in the weekly
   checklist: if `05`'s rules change, change them there too, or the audit critiques a strategy
   nobody used.

## Honesty notes for the write-up

- **The `09` notebooks overturn `08`, and that arc is the strongest methodological evidence in
  the repository.** Present it as a sequence — a conclusion, then the specific measurement
  that broke it — rather than quietly shipping only the later verdict. "The exact-resample
  pair was the tiebreaker" and "the guard was a heuristic, the back-test is a measurement" are
  the two sentences that carry it.
- **F2 and F3 are contested between the engine and the studies.** The engine labels both
  `local_peak` and proposes trust-region clouds; the studies propose somewhere else entirely.
  State the disagreement rather than silently submitting one of them.
- **The `08` critic's self-check reports ρ ≈ +0.45 (p ≈ 1.4e-5, n = 88).** Real signal, modest
  effect, n small. The notebook already labels itself a beta; keep that label in the report.

---

# Week-7 pass — release cleanup (historical)

## Consolidated / removed
- **Merged the two `07` notebooks** into `pipeline/07_run_week_and_report.ipynb`: the
  orchestrator (runs 04→06→05, dashboard) followed by the report figures. Resolved the
  duplicate `07` numbering and fixed the orchestrator's stale reference to
  `05_suggest_engine_v4-w4.ipynb`. *(The duplicate-07 problem has since returned — see item 6
  above.)*
- **De-duplicated the engine.** Kept one canonical engine and deleted the Week-4 fossil.
  Restored its navigation banner. No `v#-w#` suffix in filenames — git holds history.
- **Renamed** `10_neural_surrogates_engine_F2_F4_F6.ipynb` →
  `neural/10_neural_surrogates_engine.ipynb`: its `CONFIG` covers F2 · F4 · F5.

## Single source of truth
- Added **`bbo_meta.py`** (dim · hypothesis · status · log_y per function) and wired
  `diagnostics/svm_analysis.py` to import it, replacing hard-coded metadata that still named
  hypotheses the pipeline had refuted.
- Added **`tools/render_state.py`** to rebuild `STATE.md` from `pipeline/function_summary.csv`.
  *(`tools/` has since been retired — `04` writes the CSV directly.)*

## Hygiene
- Gave every notebook the same complete navigation banner (A/B/C/D map).
- Scrubbed Windows absolute paths and the "Challange" typo from committed cell outputs.
  *(Regressed — see item 3 above.)*
- Added `.gitignore` (ignores `data/`), `requirements.txt`, `data/README.md`, and the `report/`
  deliverable folder. Result CSVs are committed under `pipeline/` **on purpose**, because the
  raw data is private and they let the repo show results without it.
