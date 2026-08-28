# Review notes — scope of this submission

**Version** · v1.0
**Author** · Eduardo Wizentier · [wizentier@gmail.com](mailto:wizentier@gmail.com)
**Date** · 30 August 2026

---

## What is being reviewed

**v1.0 is the reviewed state of this project.** Everything in the repository at this tag
is intended for assessment and is current as of campaign close.

Work from the beta phase — earlier engine versions, superseded prototypes and
intermediate drafts of the documentation — is **not** part of this review. It exists in
the commit history for provenance, not as material to be marked. Where an earlier
approach mattered to the reasoning, it survives as a completed study in the repository
rather than as loose history.

## In scope

| Area | Where |
|---|---|
| The campaign result and its evidence | `pipeline/00_final_capstone_report.ipynb` |
| The production loop | `pipeline/` — 04 → 06 → 05, with 07 and 08 |
| Auxiliary analysis | `diagnostics/` — A1 to A5 |
| Deep-learning track | `neural/` — 08, 09, 10 |
| Dataset and model documentation | `DATASHEET_AND_MODEL_CARD.md` |
| Generated-file inventory | `REPORTS_AND_FILES_INVENTORY.md` |

All nineteen notebooks are committed in an executed state with outputs saved, so every
result can be read without running anything.

## One thing worth knowing before you read

**Some notebooks contradict each other, and that is deliberate.** This repository
documents a learning process, so studies that were later overturned are retained rather
than deleted or quietly corrected. The clearest case is the F2/F3 arc:
`08_casino_case_study_v2` reaches a conclusion, and each of the two `09` studies
overturns it on the same data plus later weeks, for reasons stated precisely enough to
check.

**Where two notebooks disagree, the later-numbered study is the standing verdict and
the earlier one is preserved reasoning — not an uncorrected error.**

The same principle applies to `09_harmonic_study_F2`, which stated a falsification
criterion in advance and was killed by its own criterion when the Week-11 probe
returned 0.1885. It is kept because it was wrong.

## Deferred work

A small number of housekeeping items remain. **None of them affects the results, the
reproducibility of any notebook, or the correctness of any reported number** — they are
navigation and naming defects. They are listed, with exact locations, in
[`/Report/HANDOFF.md`](Report/HANDOFF.md).

They are recorded rather than silently carried because knowing what is left is part of
knowing where a project stands. They are scheduled for v1.1.

## Where to start

`pipeline/00_final_capstone_report.ipynb` — the whole campaign on five A3 sheets.

Full reading order, by audience, is in [`README.md`](README.md).
