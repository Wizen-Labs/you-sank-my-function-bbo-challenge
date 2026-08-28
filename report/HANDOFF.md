# Handoff brief — BBO Capstone repository cleanup

**Project** · You Sank My Function — Black-Box Optimisation Capstone
**Author** · Eduardo Wizentier · wizentier@gmail.com
**Purpose of this file** · Paste or upload into a new chat to continue the cleanup without re-deriving anything.

---

## 1 · Original audit verdicts

| Criterion | Verdict at audit | Status now |
|---|---|---|
| Code clear, commented, easy to run, reproducible | Largely met — fixable defects | **Defects still open** (§3) |
| Datasheet complete and in repository | Partially met — stale | ✅ **Resolved** |
| Model card complete and in repository | Not met — contradicted own results | ✅ **Resolved** |
| README ~100-word non-technical write-up | Not met — absent | ✅ **Resolved** |
| Repository organisation | Largely met — files missing from map | ✅ **Resolved** |

Four of five criteria are closed. Everything remaining sits under criterion 1 and is notebook-level.

---

## 2 · Already done — do not redo

Three files were rewritten and are final:

- **`README.md`** — added `## In plain English` (103 words); corrected campaign totals; corrected F4 scoreboard row; added `LICENSE`, `DATASHEET_AND_MODEL_CARD.md`, `diagnostics/figures/` to the repo map; softened the false "same navigation banner" claim; rewrote *Reproducing* around the fact that 17 of 19 notebooks run from committed CSVs; added *Data availability* and *Licence* sections.
- **`DATASHEET_AND_MODEL_CARD.md`** — Part 1 rebuilt on Gebru structure (real schema, per-function counts, no-personal-data statement, walk-forward-only warning, distribution/maintenance). Part 2 rebuilt on Mitchell structure (factors, metrics, disaggregated results, limitations, ethics, caveats). Navigation table at top with working anchors.
- **`LICENSE`** — MIT, text unmodified so GitHub detects it, with a trailing scope note excluding all data.

Also settled: MIT chosen over Apache/CC; single combined datasheet+model-card file confirmed as fine; project name "You Sank My Function" confirmed safe for academic use (no Hasbro marks appear anywhere in the repo — verified by scan).

---

## 3 · Remaining work

### Priority 1 — Navigation banners (affects all 19 notebooks)

**3.1 · Broken link in 11 notebooks.** Every banner links to `../pipeline/05_suggest_engine.ipynb`. The actual file is **`05_suggest_engine_v2.ipynb`**. Clicking through the repo's own navigation 404s on the most important notebook.

**3.2 · Two incompatible banner versions.** Ten notebooks carry the A/B/C/D banner; nine carry an older "Weekly pipeline" banner with no section letters and no Neural (D) row.

| Banner | Notebooks |
|---|---|
| **A/B/C/D** (keep) | `00_final_capstone_report`, `07_run_week_and_report`, `08_neural_surrogates_edu`, `09_neural_surrogates_F6`, `10_neural_surrogates_engine`, `A1`–`A5` |
| **Legacy** (replace) | `04_consolidate_data`, `05_suggest_engine_v2`, `06_diagnose`, `07_ceiling_estimator`, `08_anti_hallucination_check`, `08_casino_case_study_v2`, `09_harmonic_study_F2`, `09_transform_retrial_F3`, `Preliminary_Pattern_Analysis` |

**3.3 · Legacy banners state the loop order backwards.** They read `04 → 05 Suggest → 06 Diagnose`. The correct order — per the README, the mermaid diagram and `07_run_week_and_report` itself — is **04 → 06 → 05**.

**3.4 · Wrong section label.** `00_final_capstone_report` self-labels as section **(E)**, which does not exist. It belongs to **(B) Pipeline**.

*Suggested approach: one script that rewrites the first markdown cell of all 19 notebooks from a single template, bolding the current notebook's own entry. Fixes 3.1–3.4 in one pass.*

### Priority 2 — Output filename collision

`tournament_F3.csv` is written by **two** notebooks:

- `08_casino_case_study_v2.ipynb`, cell 23 — inside `for f in STUDY_FUNCTIONS:` where `STUDY_FUNCTIONS = [2, 3]`
- `09_transform_retrial_F3.ipynb`, cell 26 — `TOURN.to_csv("tournament_F3.csv", index=False)`

Whichever runs second silently overwrites the first. Rename one (e.g. `tournament_F3_casino.csv`). Their summary files do **not** collide.

### Priority 3 — Hardcoded machine path

`04_consolidate_data.ipynb`, cell 3:

```python
DATA_DIR = os.environ.get("BBO_DATA_DIR", os.path.join("..", "D:\Capstone Challange\initial_data"))
```

The fallback is an absolute Windows path from the author's machine joined onto `..`, and it is unusable anywhere else. Replace with `os.path.join("..", "data")`. (The README currently works around this by telling readers to set `BBO_DATA_DIR`; once fixed, that caveat can be softened.)

Related: the saved output shows `Wrote: C:\Users\USER\consolidated_observations.csv` — `OUT_DIR = "."` resolved to the home directory in that run, so the CSV landed outside the repo. Worth confirming the committed copy is the right one.

### Priority 4 — Metadata drift (documented, not fixed)

Per-function metadata exists in **three** places:

1. Inlined `FUNCTION_META` table in `A1_svm_analysis` cell 3 (it still tries `from bbo_meta import FUNCTIONS` first; that module no longer exists, so the fallback always runs)
2. `FUNCTION_META` dict inside `04_consolidate_data.ipynb` cell 5 — propagates a `status` column into `function_summary.csv`
3. The weekly classifier in `05_suggest_engine_v2` — re-derives labels every week

The model card already documents this and names the weekly classifier as authoritative. Optional code fix: delete the dead `from bbo_meta import FUNCTIONS` attempt in `A1` cell 3, and have `04` and `A1` share one table.

### Priority 5 — Minor

- Empty trailing cell in `08_neural_surrogates_edu.ipynb` (cell 20) — the only unrun cell in the repository.
- Numbering collisions: two `07_`, three `08_`, two `09_`; `Preliminary_Pattern_Analysis` breaks the numeric convention despite sitting inside the weekly loop. Renaming would invalidate banner links, so do it **with** the banner rewrite or not at all.
- `07_ceiling_estimator` puts F4's central ceiling at **0.6625** while `00_final_capstone_report` scores F4 against **0.6549** (best-ever basis). Disclosed via F4's score band (0.986–0.99999), but a reviewer may ask.
- `07_ceiling_estimator` labels F1 `local_peak`; the README archetype table says `needle`. Defensible under "archetypes are states, not identities", but inconsistent on its face.

---

## 4 · Open items awaiting external input

- **Raw-data publication** — email sent to module lead asking whether the per-function initial designs and `inputs.txt` / `outputs.txt` may be published. **If approved:** update the datasheet's *Distribution* section, the `LICENSE` scope note, and the README repo map + *Data availability*. **If declined:** no change needed; current wording already assumes private.
- **`CITATION.cff`** — offered, not yet created. Adds a "Cite this repository" button on GitHub with BibTeX/APA. Pairs with a short "Citing this work" README section.
- **Copyright year** — `LICENSE` says 2026. Change if you'd prefer 2025 or 2025–2026.
- **Unverified files** — these appear in the repo map but were never uploaded, so nothing has been checked about them: `tutorials/01`–`03`, `REFERENCES.md`, `REVIEW_NOTES.md`, `requirements.txt`, `svm_analysis.py`.

---

## 5 · Verified reference numbers

Taken from `00_final_capstone_report` cell 27's computed output — authoritative, do not re-derive.

**Campaign** · 13 weekly rounds, weeks 0–13 · 279 observations (175 initial + 104 weekly) · 33 records · mean normalised score **0.9955** across the seven functions with defensible ceilings.

| F | dim | kind | initial best | final best | found | records | ceiling (basis) | score |
|---|-----|------|--------------|------------|-------|---------|-----------------|-------|
| F1 | 2 | deterministic | ~0 | 1.99995 | W11 | 7 | 2.0 · hypothesised | 0.99998 |
| F2 | 2 | noisy | 0.6112 | 0.65048 | W10 | 2 | 0.70 · speculative | 0.4424 (band 0.283–0.805) |
| F3 | 3 | noisy | −0.03484 | −0.00037 | W12 | 4 | 0.0 · hard cap | 0.98938 |
| F4 | 4 | deterministic | −4.0255 | 0.65487 | W13 | 6 | 0.6549 · best-ever | 0.99999 |
| F5 | 4 | deterministic | 1088.86 | 8662.48 | W9 | 6 | 8662.48 · corner | 1.00000 |
| F6 | 5 | noisy | −0.71426 | −0.23475 | W10 | 3 | −0.2247 · low conf. | 0.97948 |
| F7 | 6 | deterministic | 1.36497 | 3.32237 | W1 | 3 | 3.32237 · analytic | 1.00000 |
| F8 | 8 | deterministic | 9.59848 | 10.00000 | W2 | 2 | 10.0 · analytic | 1.00000 |

Per-function observation counts: F1 23 · F2 23 · F3 28 · F4 43 · F5 33 · F6 33 · F7 43 · F8 53 (range **23–53**).

Initial design sizes: F1 10 · F2 10 · F3 15 · F4 30 · F5 20 · F6 20 · F7 30 · F8 40.

`consolidated_observations.csv` schema: `function`, `dim`, `week`, `source` (`initial`/`weekly`), `x1`–`x8` (NaN-padded beyond each function's `dim`), `y`.

**Generated artefacts:** 88 total across 16 of 19 notebooks — 60 PNG, 26 CSV, 1 TXT, 1 MD. Full per-notebook inventory is in `REPORTS_AND_FILES_INVENTORY.md`. The three neural notebooks write nothing.

---

## 6 · What to upload to the new chat

Required: the 19 `.ipynb` files (for the banner rewrite).
Helpful: this brief, plus `README.md`, `DATASHEET_AND_MODEL_CARD.md`, `LICENSE`, and `REPORTS_AND_FILES_INVENTORY.md`.

**Opening line to use:** *"Continuing a repository cleanup — the attached handoff brief lists what's done and what's left. Start with Priority 1, the notebook navigation banners."*
