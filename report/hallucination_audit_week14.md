# Anti-hallucination audit — week 14

Submission: `week14_engine_submission.txt`  ·  observations through week 13
Engine baseline: ok

Detector self-check: Spearman ρ = +0.467 (p = 5.94e-07, n = 104) between the pre-result risk proxy and realised surprise.

## Summary

| F   | pathology      |   risk | verdict   |   A · support |   B · model agreement |   C · calibration |   D · headroom coherence |   E · strategy stability |   F · resolvability |   flags |
|:----|:---------------|-------:|:----------|--------------:|----------------------:|------------------:|-------------------------:|-------------------------:|--------------------:|--------:|
| F1  | local_peak     |   47   | ELEVATED  |          0.45 |                  0.7  |              0.19 |                     0.64 |                     0.45 |                   0 |       2 |
| F2  | plateau        |   35.4 | MODERATE  |          0.2  |                  0.62 |              0.05 |                     0.43 |                     0.75 |                   0 |       2 |
| F3  | local_peak     |   25.6 | MODERATE  |          0.15 |                  0.4  |              0.08 |                     0.43 |                     0.3  |                   0 |       2 |
| F4  | local_peak     |   28.5 | MODERATE  |          0    |                  0.67 |              0.05 |                     0.56 |                     0    |                   0 |       0 |
| F5  | boundary_climb |   35.3 | MODERATE  |          0.32 |                  0.62 |              0    |                     0.6  |                     0.15 |                   0 |       2 |
| F6  | plateau        |   19.3 | LOW       |          0    |                  0.18 |              0.04 |                     0.43 |                     0.75 |                   0 |       2 |
| F7  | solved_lock    |    7.1 | LOCK      |          0    |                  0.24 |              0.04 |                     0    |                     0    |                   0 |       1 |
| F8  | solved_lock    |    0.4 | LOCK      |          0    |                  0.02 |              0    |                     0    |                     0    |                   0 |       1 |

## Per-function critique

```
F1 — local_peak — risk 47/100 (ELEVATED)
  query: 0.644156-0.601884
  what drives the score:
    [0.70] B · model agreement: surrogate spread is 0.64 sd of the response — the models do not agree on what happens here; no surrogate in the ensemble predicts this point beats best-ever
    [0.64] D · headroom coherence: the ceiling for this function has been broken by the next week's probe in 7/12 backtests — treat any 'no headroom' claim here as weak evidence
    [0.45] E · strategy stability: label changed at the most recent week (needle -> local_peak); the strategy module that generated this pick is 1 flips old
    [0.45] A · support: no observation within the fitted length scale (0.026) of this point; lies 0.0266 beyond the on-line range along x2 — extrapolation, not interpolation
    [0.19] C · calibration: 5/13 past weeks landed outside a 2-sigma band; worst surprise was week 3 at 158.3 sigma
  decision flags (not scored as hallucination):
    - DOMINATED — the referee predicts 1.016, below the banked 2; this week buys information, not score
    - no surrogate in the ensemble expects a new best here
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F2 — plateau — risk 35/100 (MODERATE)
  query: 0.785400-0.232500
  what drives the score:
    [0.75] E · strategy stability: label changed at the most recent week (local_peak -> plateau); the strategy module that generated this pick is 1 flips old
    [0.62] B · model agreement: no surrogate in the ensemble predicts this point beats best-ever
    [0.43] D · headroom coherence: the ceiling for this function has been broken by the next week's probe in 2/12 backtests — treat any 'no headroom' claim here as weak evidence
    [0.20] A · support: query sits inside well-sampled territory
    [0.05] C · calibration: intervals have been roughly honest over 13 weeks
  decision flags (not scored as hallucination):
    - DOMINATED — the referee predicts 0.5958, below the banked 0.6505; this week buys information, not score
    - no surrogate in the ensemble expects a new best here
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F3 — local_peak — risk 26/100 (MODERATE)
  query: 0.306054-0.540484-0.529115
  what drives the score:
    [0.43] D · headroom coherence: the ceiling for this function has been broken by the next week's probe in 2/12 backtests — treat any 'no headroom' claim here as weak evidence
    [0.40] B · model agreement: no surrogate in the ensemble predicts this point beats best-ever
    [0.30] E · strategy stability: 0 flip(s) in the last 4 weeks
    [0.15] A · support: query sits inside well-sampled territory
    [0.08] C · calibration: worst surprise was week 3 at 4.1 sigma
  decision flags (not scored as hallucination):
    - DOMINATED — the referee predicts -0.02265, below the banked -0.0003699; this week buys information, not score
    - no surrogate in the ensemble expects a new best here
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F4 — local_peak — risk 28/100 (MODERATE)
  query: 0.439084-0.421578-0.306838-0.465977
  what drives the score:
    [0.67] B · model agreement: ensemble scatter is 9.6x the referee GP's own error bar (the referee is more confident than the evidence warrants); 1/6 models predict an improvement — the pick's whole case is model-dependent
    [0.56] D · headroom coherence: every ceiling estimate says the headroom here is spent, yet the pick is priced on a gain — one of the two is wrong; the ceiling for this function has been broken by the next week's probe in 5/12 backtests — treat any 'no headroom' claim here as weak evidence
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F5 — boundary_climb — risk 35/100 (MODERATE)
  query: 1.000000-1.000000-1.000000-0.800000
  what drives the score:
    [0.62] B · model agreement: no surrogate in the ensemble predicts this point beats best-ever
    [0.60] D · headroom coherence: the ceiling for this function has been broken by the next week's probe in 6/12 backtests — treat any 'no headroom' claim here as weak evidence
    [0.32] A · support: only 2 on-line point(s) along x4, the axis this pick moves most — the shape there is assumed, not measured; lies 0.2000 beyond the on-line range along x4 — extrapolation, not interpolation
    [0.15] E · strategy stability: 0 flip(s) in the last 4 weeks
  decision flags (not scored as hallucination):
    - DOMINATED — the referee predicts 2593, below the banked 8662; this week buys information, not score
    - no surrogate in the ensemble expects a new best here
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F6 — plateau — risk 19/100 (LOW)
  query: 0.246126-0.321303-0.612008-0.717899-0.000000
  what drives the score:
    [0.75] E · strategy stability: label changed at the most recent week (local_peak -> plateau); the strategy module that generated this pick is 1 flips old
    [0.43] D · headroom coherence: the ceiling for this function has been broken by the next week's probe in 2/12 backtests — treat any 'no headroom' claim here as weak evidence
    [0.18] B · model agreement: no surrogate in the ensemble predicts this point beats best-ever
  decision flags (not scored as hallucination):
    - DOMINATED — the referee predicts -0.3166, below the banked -0.2347; this week buys information, not score
    - no surrogate in the ensemble expects a new best here
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F7 — solved_lock — risk 7/100 (LOCK)
  query: 0.201689-0.150011-0.476874-0.275333-0.311652-0.657301
  what drives the score:
    [0.24] B · model agreement: no surrogate in the ensemble predicts this point beats best-ever
  decision flags (not scored as hallucination):
    - LOCK — an epsilon re-probe of a banked optimum; nothing is being claimed
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

```
F8 — solved_lock — risk 0/100 (LOCK)
  query: 0.100000-0.150000-0.130000-0.150000-0.800000-0.500001-0.200000-0.600000
  what drives the score:
    nothing above threshold on any axis
  decision flags (not scored as hallucination):
    - LOCK — an epsilon re-probe of a banked optimum; nothing is being claimed
  blind spots: this check cannot see the true function, cannot value information-gathering probes, and inherits 05b's pathology labels.
```

## Standing caveats

- The risk score is a weighted judgement call, not a fitted quantity; `WEIGHTS` is exposed so it can be argued with.
- Axis C rests on nine walk-forward weeks per function.
- Axis G reports `UNVERIFIABLE` for every claim shape it was not taught; that is *unchecked*, not clean.
- Pathology labels are inherited from 05b, so 05b's misclassifications propagate here.
- A high score is a request for a second look, not a veto.