# data/ — raw challenge data (not committed)

Place the challenge files here, or point `BBO_DATA_DIR` at another folder.
Two layouts are accepted by `pipeline/04_consolidate_data.ipynb`:

1. **Tidy CSVs** — `f1_data.csv` … `f8_data.csv` with columns `point, x1..xd, y`.
2. **Per-function .npy folders** — `function_1/ … function_8/`, each containing
   `initial_inputs.npy` and `initial_outputs.npy`.

Plus the cumulative weekly files (one row per week, 8 entries per row,
functions 1→8, Python-repr format):

- `weekly_inputs.txt`
- `weekly_outputs.txt`

`tutorials/03` additionally looks for the original `initial_data/` folder here
(override with `BBO_INITIAL_DATA`).
