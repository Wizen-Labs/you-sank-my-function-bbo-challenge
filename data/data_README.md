# `data/` — raw challenge data (not committed)

The challenge data is private and is **not** in this repository. Only this file is
committed; the data files themselves are ignored.

**You do not need this folder to reproduce the published results.** Seventeen of the
nineteen notebooks read only the committed `consolidated_observations.csv` and run
as-is. This folder is required by two notebooks: `pipeline/04_consolidate_data.ipynb`
and `pipeline/07_run_week_and_report.ipynb`.

---

## Where to put it

Either drop the files here in `data/`, or keep them anywhere and point an environment
variable at that folder:

```bash
export BBO_DATA_DIR=/path/to/initial_data        # Linux / macOS
set BBO_DATA_DIR=D:\path\to\initial_data         # Windows
```

`04_consolidate_data` also searches upward from its working directory for a folder
containing the data, so if `data/` sits beside `pipeline/` it is usually found without
setting anything. The notebook prints the folder it resolved, and flags any missing
file, before it reads a single row.

---

## What goes in it

### 1 · Initial designs — one of two layouts

Both are supported; use whichever you have.

**(a) Per-function `.npy` folders**

```
data/
├── function_1/  initial_inputs.npy   initial_outputs.npy
├── function_2/  initial_inputs.npy   initial_outputs.npy
└── …            function_3 … function_8
```

`initial_inputs.npy` is shape `(n, d)`, `initial_outputs.npy` is shape `(n,)`.

**(b) Tidy CSVs**

```
data/
└── f1_data.csv … f8_data.csv        columns: point, x1 … xd, y
```

Expected shapes either way:

| F | dim | initial points |
|---|-----|----------------|
| F1 | 2 | 10 |
| F2 | 2 | 10 |
| F3 | 3 | 15 |
| F4 | 4 | 30 |
| F5 | 4 | 20 |
| F6 | 5 | 20 |
| F7 | 6 | 30 |
| F8 | 8 | 40 |
| | | **175** |

All inputs lie on the unit cube $[0,1]^d$.

### 2 · Cumulative weekly results

```
data/
├── inputs.txt
└── outputs.txt
```

> **Use exactly these names.** `04_consolidate_data` reads `inputs.txt` and
> `outputs.txt` only. `07_run_week_and_report` additionally accepts
> `weekly_inputs.txt` / `weekly_outputs.txt`, so the prefixed names will appear to
> work in one notebook and fail in the other. Stick to the unprefixed pair.

One row per week, appended after each portal result — this append is the only manual
step in the weekly loop. Each row holds **8 entries**, functions 1 → 8 in order, in
Python-repr format:

```
inputs.txt   → [[0.7026, 0.9266], [0.4831, 0.2044], [...], ...]   # 8 vectors, dims 2,2,3,4,4,5,6,8
outputs.txt  → [0.5580, 1.2431, -0.0151, ...]                     # 8 scalars
```

`04_consolidate_data` strips `np.float64(...)` and `array([...])` wrappers, asserts
that each vector's length matches its function's declared dimension, and asserts that
`inputs.txt` and `outputs.txt` have the same number of rows. It fails loudly on a
mismatch rather than silently coercing.

The completed campaign has **13** weekly rows, giving 175 + 104 = **279** observations.

---

## What it produces

Running `pipeline/04_consolidate_data.ipynb` rebuilds two files in `pipeline/`,
from scratch, every time:

- `consolidated_observations.csv` — the single tidy table every other notebook reads
- `function_summary.csv` — per-function state of play

Nothing downstream depends on a hand-maintained record.

---

## Keeping the data out of git *(optional)*

Not needed if you keep the data outside the repository and point `BBO_DATA_DIR` at
it — this folder then holds nothing but the file you are reading. If you do drop the
data in here, add this to `.gitignore` so it never gets committed:

```gitignore
data/*
!data/README.md
```

---

## Also looks here

`tutorials/03_capstone_eda_and_prototype.ipynb` expects the original `initial_data/`
folder inside `data/`. Override with `BBO_INITIAL_DATA` if you keep it elsewhere.

---

## Provenance and terms

The raw data is constrained by the academic rules of the Imperial College Business
School Bayesian Optimisation Challenge and may not be redistributed. Full
specification — composition, collection process, sampling biases, known gaps — is in
[`DATASHEET_AND_MODEL_CARD.md`](../DATASHEET_AND_MODEL_CARD.md), Part 1.
