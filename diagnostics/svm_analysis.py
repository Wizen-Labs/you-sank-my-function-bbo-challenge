"""
svm_analysis.py
================
Support Vector Machine (SVM) toolkit for the "You Sank My Function"
Bayesian-Optimisation capstone.

>>> IMPORTANT SCOPE NOTE <<<
This module is an AUXILIARY / DIAGNOSTIC tool only. It is used for analysis,
demonstration and to extract supporting intelligence about each black-box
function (which dimensions matter, in which direction, how "learnable" the
landscape is). It is deliberately NOT part of the competition strategy: the
weekly queries are chosen by the Bayesian-optimisation pipeline, not by any
SVM here. Nothing in this file proposes or selects a query point.

What it does
------------
For each function it can:
  1. Fit a Support Vector *Regressor* (SVR) surrogate with cross-validated
     hyper-parameters -> gives an R^2 / RMSE "learnability" score that acts as
     a proxy for landscape smoothness / signal-to-noise.
  2. Fit a Support Vector *Classifier* (SVC) that separates the top-performing
     points from the rest -> the decision geometry shows where the good region
     is; a linear SVC gives interpretable per-dimension weights (direction).
  3. Compute permutation importance on the SVR -> dimension relevance ranking.
  4. Combine the above into a per-dimension directional summary
     ("push high" / "push low" / "weak"), which corroborates (or challenges)
     the hand-built directional hypotheses WITHOUT driving the strategy.

Data source
-----------
As of the consolidation step this module reads a SINGLE input file,
``consolidated_observations.csv`` (one tidy row per observation, all eight
functions stacked), located in the directory the notebook/script runs from.
Each row carries ``function``, ``dim``, ``week``, ``source`` and ``x1..x8`` /
``y``; ``load_function`` slices out one function and keeps only its active
``x1..x{dim}`` columns plus ``y`` so the rest of the pipeline is unchanged.
The ``source`` column distinguishes the original space-filling design
(``initial``) from the points added by the live Bayesian-optimisation loop
(``weekly``); by default every observation is used.

Severe-data caveat
------------------
The designs are still small: the initial space-filling sets (10-40 points in up
to 8 dimensions) plus six weekly Bayesian-optimisation points per function.
Every metric below is therefore high-variance and is reported with
cross-validation spread. Treat all numbers as soft evidence, never as ground
truth.
"""

from __future__ import annotations

import os
import os as _os
import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR, SVC, LinearSVC
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    RepeatedKFold,
    StratifiedKFold,
    cross_val_predict,
    cross_val_score,
)
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import permutation_importance

RNG = 42

# Single consolidated input file. The whole pipeline now reads one tidy CSV
# (all eight functions stacked) that lives in the directory the notebook/script
# is run from. Override in three ways (highest priority first):
#   1. pass data_dir=... to load_function / SVMFunctionAnalyzer / analyze_all
#   2. set the BBO_DATA_DIR / BBO_DATA_FILE environment variables before import
#   3. fall back to "consolidated_observations.csv" in the current directory
DEFAULT_DATA_DIR = os.environ.get("BBO_DATA_DIR", ".")
CONSOLIDATED_FILENAME = os.environ.get("BBO_DATA_FILE", "consolidated_observations.csv")


# --------------------------------------------------------------------------- #
# Per-function metadata. `log_y` flags objectives with a huge positive dynamic
# range where modelling log1p(y) is more sensible for the SVR surrogate.
# --------------------------------------------------------------------------- #
# Per-function metadata now lives in the repo-root single source of truth (bbo_meta.py),
# so this diagnostic module can never drift from the pipeline's hypotheses again.
import sys as _sys
_repo_root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _repo_root not in _sys.path:
    _sys.path.insert(0, _repo_root)
try:
    from bbo_meta import FUNCTIONS as FUNCTION_META   # dim / hypothesis / status / log_y
except Exception:
    # Standalone fallback so this diagnostic notebook still runs without the
    # repo-root bbo_meta.py. The hypothesis strings mirror the hand-built
    # directional notes; when bbo_meta.py IS importable it takes precedence.
    FUNCTION_META = {
        1: dict(dim=2, hypothesis="background radiation: ~zero everywhere bar one point (negative control)", log_y=False),
        2: dict(dim=2, hypothesis="noisy six-hump; promising corner at high x1 / high x2",                  log_y=False),
        3: dict(dim=3, hypothesis="Hartmann-3: sharply peaked, severely under-sampled",                     log_y=False),
        4: dict(dim=4, hypothesis="smooth basin; x1 dominant (push x1 low)",                                log_y=False),
        5: dict(dim=4, hypothesis="huge positive dynamic range; model log1p(y)",                            log_y=True),
        6: dict(dim=5, hypothesis="Styblinski-Tang style wells; low x5 / high x4",                          log_y=False),
        7: dict(dim=6, hypothesis="Hartmann-6: under-sampled; lean on literature optimum",                  log_y=False),
        8: dict(dim=8, hypothesis="Ackley with broad bowl; low x1 / low x3",                                log_y=False),
    }


def _resolve_data_path(data_dir: str = DEFAULT_DATA_DIR) -> str:
    """Return the path to the consolidated CSV.

    ``data_dir`` may be a directory (the file name is appended) or a direct
    path to a ``.csv`` file. This keeps backwards compatibility with callers
    that still pass ``data_dir=...``.
    """
    if data_dir and data_dir.lower().endswith(".csv"):
        return data_dir
    return os.path.join(data_dir or ".", CONSOLIDATED_FILENAME)


# Tiny cache so the eight per-function loads don't re-read the same file eight
# times. Keyed by (absolute path, mtime) so an edited file is picked up.
_CONSOLIDATED_CACHE: dict[tuple, pd.DataFrame] = {}


def load_consolidated(data_dir: str = DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Load the full consolidated observations table (all functions stacked)."""
    path = _resolve_data_path(data_dir)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find '{path}'. Place consolidated_observations.csv in the "
            f"directory you run from, pass data_dir=..., or set BBO_DATA_DIR / "
            f"BBO_DATA_FILE."
        )
    key = (os.path.abspath(path), os.path.getmtime(path))
    if key not in _CONSOLIDATED_CACHE:
        _CONSOLIDATED_CACHE[key] = pd.read_csv(path)
    return _CONSOLIDATED_CACHE[key]


def load_function(func_id: int, data_dir: str = DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Load one function's observations from the consolidated CSV.

    Returns a tidy DataFrame with exactly the function's active ``x1..x{dim}``
    columns plus ``y`` (same shape the rest of the pipeline expects), using
    every available observation (initial design + weekly BO points).
    """
    full = load_consolidated(data_dir)
    sub = full[full["function"] == func_id]
    if sub.empty:
        raise ValueError(f"No rows for function {func_id} in the consolidated file.")
    dim = int(sub["dim"].iloc[0])
    x_cols = [f"x{i}" for i in range(1, dim + 1)]
    return sub[x_cols + ["y"]].reset_index(drop=True)


@dataclass
class SVMResult:
    """Container for everything the analyzer learns about one function."""
    func_id: int
    dim: int
    n: int
    hypothesis: str
    # regression
    svr_best_params: dict = field(default_factory=dict)
    svr_r2_mean: float = np.nan
    svr_r2_std: float = np.nan
    svr_rmse_mean: float = np.nan
    log_y: bool = False
    # classification (top-quartile vs rest)
    svc_auc_mean: float = np.nan
    svc_auc_std: float = np.nan
    svc_acc_mean: float = np.nan
    # interpretability
    perm_importance: pd.Series = None          # mean permutation importance per dim
    spearman: pd.Series = None                  # monotone corr of each x with y
    linsvc_weights: pd.Series = None            # linear-SVC weight per dim
    directional_summary: pd.DataFrame = None    # combined verdict per dim


class SVMFunctionAnalyzer:
    """Fit SVR + SVC diagnostics for a single function."""

    def __init__(self, func_id: int, df: pd.DataFrame | None = None,
                 data_dir: str = DEFAULT_DATA_DIR, top_quantile: float = 0.75):
        self.func_id = func_id
        self.meta = FUNCTION_META[func_id]
        self.dim = self.meta["dim"]
        self.hypothesis = self.meta["hypothesis"]
        self.log_y = self.meta["log_y"]
        self.top_quantile = top_quantile

        if df is None:
            df = load_function(func_id, data_dir)
        self.df = df.reset_index(drop=True)
        self.x_cols = [f"x{i}" for i in range(1, self.dim + 1)]
        self.X = self.df[self.x_cols].to_numpy(dtype=float)
        self.y = self.df["y"].to_numpy(dtype=float)
        self.n = len(self.y)

        # objective used for the SVR surrogate (optionally log1p compressed)
        if self.log_y:
            # shift so the minimum maps to >0, then log1p
            self._y_shift = -min(0.0, self.y.min()) + 1e-9
            self.y_model = np.log1p(self.y + self._y_shift)
        else:
            self.y_model = self.y.copy()

        self.result = SVMResult(func_id=func_id, dim=self.dim, n=self.n,
                                hypothesis=self.hypothesis, log_y=self.log_y)
        self.svr_ = None
        self.svc_ = None

    # ----------------------------- regression ----------------------------- #
    def fit_regressor(self):
        """Cross-validated SVR surrogate. Returns the fitted GridSearchCV."""
        n_splits = 5 if self.n >= 15 else 3
        cv = RepeatedKFold(n_splits=n_splits, n_repeats=5, random_state=RNG)

        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("svr", SVR(kernel="rbf")),
        ])
        grid = {
            "svr__C": [0.1, 1, 10, 100],
            "svr__gamma": ["scale", 0.05, 0.2, 0.5, 1.0],
            "svr__epsilon": [0.01, 0.1, 0.2],
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            search = GridSearchCV(pipe, grid, cv=cv, scoring="r2",
                                  n_jobs=-1, refit=True)
            search.fit(self.X, self.y_model)
        self.svr_ = search

        # honest out-of-fold scores at the chosen params
        oof_cv = KFold(n_splits=n_splits, shuffle=True, random_state=RNG)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r2_scores = cross_val_score(search.best_estimator_, self.X,
                                        self.y_model, cv=cv, scoring="r2")
            oof_pred = cross_val_predict(search.best_estimator_, self.X,
                                         self.y_model, cv=oof_cv)
        rmse = float(np.sqrt(mean_squared_error(self.y_model, oof_pred)))

        self.result.svr_best_params = search.best_params_
        self.result.svr_r2_mean = float(np.mean(r2_scores))
        self.result.svr_r2_std = float(np.std(r2_scores))
        self.result.svr_rmse_mean = rmse
        return search

    # --------------------------- classification --------------------------- #
    def _labels(self) -> np.ndarray:
        """Top-quantile points -> 1 (promising), rest -> 0."""
        thr = np.quantile(self.y, self.top_quantile)
        return (self.y >= thr).astype(int)

    def fit_classifier(self):
        """Cross-validated RBF-SVC separating promising vs ordinary points."""
        y_cls = self._labels()
        if y_cls.sum() < 2 or (len(y_cls) - y_cls.sum()) < 2:
            # too few in a class to cross-validate
            return None

        n_splits = min(5, int(y_cls.sum()), int(len(y_cls) - y_cls.sum()))
        n_splits = max(2, n_splits)
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RNG)

        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("svc", SVC(kernel="rbf", probability=False,
                        class_weight="balanced")),
        ])
        grid = {
            "svc__C": [0.1, 1, 10, 100],
            "svc__gamma": ["scale", 0.1, 0.5, 1.0],
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            search = GridSearchCV(pipe, grid, cv=cv, scoring="roc_auc",
                                  n_jobs=-1, refit=True)
            search.fit(self.X, y_cls)
            auc = cross_val_score(search.best_estimator_, self.X, y_cls,
                                  cv=cv, scoring="roc_auc")
            acc = cross_val_score(search.best_estimator_, self.X, y_cls,
                                  cv=cv, scoring="accuracy")
        self.svc_ = search
        self.result.svc_auc_mean = float(np.mean(auc))
        self.result.svc_auc_std = float(np.std(auc))
        self.result.svc_acc_mean = float(np.mean(acc))
        return search

    # --------------------------- interpretability -------------------------- #
    def interpret(self):
        """Permutation importance + Spearman + linear-SVC weights -> direction."""
        # 1. permutation importance on the SVR surrogate
        if self.svr_ is None:
            self.fit_regressor()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pi = permutation_importance(self.svr_.best_estimator_, self.X,
                                        self.y_model, n_repeats=50,
                                        random_state=RNG, scoring="r2")
        perm = pd.Series(pi.importances_mean, index=self.x_cols)

        # 2. monotone (Spearman) correlation of each x with the RAW objective
        rho = {}
        for j, c in enumerate(self.x_cols):
            r, _ = spearmanr(self.X[:, j], self.y)
            rho[c] = 0.0 if np.isnan(r) else float(r)
        spear = pd.Series(rho)

        # 3. interpretable linear-SVC weights (on standardised features)
        y_cls = self._labels()
        weights = pd.Series(0.0, index=self.x_cols)
        if y_cls.sum() >= 2 and (len(y_cls) - y_cls.sum()) >= 2:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                lin = Pipeline([
                    ("scale", StandardScaler()),
                    ("lsvc", LinearSVC(C=1.0, class_weight="balanced",
                                       max_iter=20000, dual="auto")),
                ]).fit(self.X, y_cls)
            weights = pd.Series(lin.named_steps["lsvc"].coef_.ravel(),
                                index=self.x_cols)

        # 4. combined directional verdict
        summary = pd.DataFrame({
            "perm_importance": perm,
            "spearman_rho": spear,
            "linsvc_weight": weights,
        })
        # importance rank (higher = more relevant)
        summary["relevance"] = summary["perm_importance"].rank(ascending=False).astype(int)

        def verdict(row):
            # direction comes from Spearman (robust) backed by linear-SVC sign
            strong = abs(row["spearman_rho"]) >= 0.35
            if not strong:
                return "weak / unclear"
            return "push HIGH (x->1)" if row["spearman_rho"] > 0 else "push LOW (x->0)"

        summary["direction"] = summary.apply(verdict, axis=1)
        summary = summary.sort_values("perm_importance", ascending=False)

        self.result.perm_importance = perm
        self.result.spearman = spear
        self.result.linsvc_weights = weights
        self.result.directional_summary = summary
        return summary

    # ------------------------------- driver -------------------------------- #
    def run_all(self) -> SVMResult:
        self.fit_regressor()
        self.fit_classifier()
        self.interpret()
        return self.result


def analyze_all(data_dir: str = DEFAULT_DATA_DIR, top_quantile: float = 0.75
                ) -> dict[int, SVMFunctionAnalyzer]:
    """Run the full SVM diagnostic suite on all eight functions."""
    out = {}
    for fid in range(1, 9):
        az = SVMFunctionAnalyzer(fid, data_dir=data_dir, top_quantile=top_quantile)
        az.run_all()
        out[fid] = az
    return out


def learnability_label(r2: float) -> str:
    """Qualitative read of the cross-validated SVR R^2."""
    if not np.isfinite(r2) or r2 < 0:
        return "none (noise-dominated)"
    if r2 >= 0.7:
        return "high (smooth)"
    if r2 >= 0.3:
        return "moderate"
    return "low"


def results_table(analyzers: dict[int, SVMFunctionAnalyzer]) -> pd.DataFrame:
    """Tidy one-row-per-function summary of the SVM diagnostics."""
    rows = []
    for fid, az in analyzers.items():
        r = az.result
        top_dims = list(r.directional_summary.index[:2]) if r.directional_summary is not None else []
        # R^2 is unbounded below; clip for a readable table but keep the label honest
        r2_disp = float(np.clip(r.svr_r2_mean, -1.0, 1.0)) if np.isfinite(r.svr_r2_mean) else -1.0
        rows.append({
            "function": f"F{fid}",
            "dim": r.dim,
            "n_points": r.n,
            "svr_r2_cv": round(r2_disp, 3),
            "learnability": learnability_label(r.svr_r2_mean),
            "svr_rmse_cv": round(r.svr_rmse_mean, 4),
            "svc_auc_cv": round(r.svc_auc_mean, 3),
            "top_dims": ", ".join(top_dims),
            "log_y": r.log_y,
            "hypothesis": r.hypothesis,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    analyzers = analyze_all()
    table = results_table(analyzers)
    pd.set_option("display.width", 160)
    pd.set_option("display.max_columns", None)
    print(table.to_string(index=False))
