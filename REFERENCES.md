# References — Technical Foundations

This table records the methods, algorithms, and libraries behind my Black-Box Optimisation (BBO) capstone, with the paper or source that each one is grounded in. Methods are routed per function: I do not force a single approach across all eight functions.

## Methods and algorithms — core routing

| # | Method / Tool | Where I use it | Reference |
|---|---------------|----------------|-----------|
| 1 | **TuRBO** (Trust Region Bayesian Optimization) | F4 — local trust-region search after a global gradient overshot; generalised into the `local_peak` strategy module in `05_suggest_engine_v2` | Eriksson, D., Pearce, M., Gardner, J., Turner, R. D., & Poloczek, M. (2019). *Scalable Global Optimization via Local Bayesian Optimization.* Advances in Neural Information Processing Systems (NeurIPS) 32, 5496–5507. |
| 2 | **qNEI** (q-Noisy Expected Improvement) | F2 — noise-aware query selection on a noisy function | Letham, B., Karrer, B., Ottoni, G., & Bakshy, E. (2019). *Constrained Bayesian Optimization with Noisy Experiments.* Bayesian Analysis, 14(2), 495–519. |
| 3 | **ZoMBI** (Zooming Memory-Based Initialization) | F1 — needle-in-a-haystack search by iteratively zooming the bounds | Siemenn, A. E., Ren, Z., Li, Q., & Buonassisi, T. (2023). *Fast Bayesian optimization of needle-in-a-haystack problems using zooming memory-based initialization (ZoMBI).* npj Computational Materials, 9(1), 79. |
| 4 | **GP-BO** (Gaussian Process Bayesian Optimization) — core surrogate framework, with RBF and Matérn 5/2 kernels and ARD | All well-sampled functions — surrogate + acquisition for query selection; ARD relevance drives the `x2`-is-inert finding on F2 and the anisotropy finding on F3 | Rasmussen, C. E., & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning.* MIT Press. |
| 5 | **CMA-ES** (Covariance Matrix Adaptation Evolution Strategy) | F6 — probing interaction effects once a separable model was falsified | Hansen, N., & Ostermeier, A. (2001). *Completely Derandomized Self-Adaptation in Evolution Strategies.* Evolutionary Computation, 9(2), 159–195. |

## Methods added in the Week 8–11 phase

These support the generalised engine (`05_suggest_engine_v2`), the ceiling estimator (`07`), the anti-hallucination critic (`08`), and the two single-function retrials (`09`).

| # | Method / Tool | Where I use it | Reference |
|---|---------------|----------------|-----------|
| 6 | **Expected Improvement** (EGO) | the referee acquisition that prices every candidate from every strategy module in `05`, and the `latent_EI` arm of both tournaments | Jones, D. R., Schonlau, M., & Welch, W. J. (1998). *Efficient Global Optimization of Expensive Black-Box Functions.* Journal of Global Optimization, 13(4), 455–492. |
| 7 | **GP-UCB** | the `UCB` tournament arm, and the pathology-blind ceiling reference in `07` against which the pathology-aware estimates are contrasted | Srinivas, N., Krause, A., Kakade, S. M., & Seeger, M. (2010). *Gaussian Process Optimization in the Bandit Setting: No Regret and Experimental Design.* ICML 27, 1015–1022. |
| 8 | **Thompson sampling** | the `thompson` arm — sample a function from the posterior, optimise it | Thompson, W. R. (1933). *On the Likelihood that One Unknown Probability Exceeds Another in View of the Evidence of Two Samples.* Biometrika, 25(3/4), 285–294. |
| 9 | **The optimizer's / winner's curse** | the root-cause verdict in `08_casino_case_study_v2` (F2) and the quantified curse at F3's replicated incumbent in `09_transform_retrial_F3` §4 | Smith, J. E., & Winkler, R. L. (2006). *The Optimizer's Curse: Skepticism and Postdecision Surprise in Decision Analysis.* Management Science, 52(3), 311–322. |
| 10 | **Maximin-distance designs** | the "emptiest part of the map" exploration candidates in `05`, and the `maximin` tournament arm | Johnson, M. E., Moore, L. M., & Ylvisaker, D. (1990). *Minimax and Maximin Distance Designs.* Journal of Statistical Planning and Inference, 26(2), 131–148. |
| 11 | **Leave-one-out predictive density for model comparison** | tempered LOO ensemble weights in `08`/`09`, and the decisive additive-vs-multiplicative test in `09_transform_retrial_F3` | Vehtari, A., Gelman, A., & Gabry, J. (2017). *Practical Bayesian Model Evaluation Using Leave-One-Out Cross-Validation and WAIC.* Statistics and Computing, 27(5), 1413–1432. |
| 12 | **Variance-stabilising transforms and the change-of-variables term** | F3's `z = log(−y)`; the Jacobian is what makes the two likelihoods comparable in y-units rather than on incomparable scales | Box, G. E. P., & Cox, D. R. (1964). *An Analysis of Transformations.* Journal of the Royal Statistical Society: Series B, 26(2), 211–252. |
| 13 | **Input-dependent (heteroscedastic) noise in GP regression** | the multiplicative-noise model for F3 — the reason a homoscedastic likelihood gave the two catastrophic reads ~20× the leverage they deserved | Goldberg, P. W., Williams, C. K. I., & Bishop, C. M. (1998). *Regression with Input-Dependent Noise: A Gaussian Process Treatment.* Advances in Neural Information Processing Systems (NIPS) 10, 493–499. |
| 14 | **Least-squares (Lomb–Scargle) periodogram** | the frequency scan that recovered F2's 7π sinusoid, and the band structure along F3's `x3` | Scargle, J. D. (1982). *Studies in Astronomical Time Series Analysis. II.* Astrophysical Journal, 263, 835–853. Practical treatment: VanderPlas, J. T. (2018). *Understanding the Lomb–Scargle Periodogram.* Astrophysical Journal Supplement Series, 236(1), 16. |
| 15 | **Sampling theorem / aliasing** | the F2 diagnosis: 10 initial points across 3.5 cycles folds a deterministic wave into apparent noise | Shannon, C. E. (1949). *Communication in the Presence of Noise.* Proceedings of the IRE, 37(1), 10–21. |
| 16 | **AICc** (small-sample corrected AIC) | the model-form tournament in `09_harmonic_study_F2` — at n ≈ 21 the uncorrected AIC under-penalises parameters | Hurvich, C. M., & Tsai, C.-L. (1989). *Regression and Time Series Model Selection in Small Samples.* Biometrika, 76(2), 297–307. |
| 17 | **BBOB / COCO landscape taxonomy** | the signature-level landscape classification in `Preliminary_Pattern_Analysis` §9 — a *family*, explicitly not an identification | Hansen, N., Auger, A., Ros, R., Mersmann, O., Tušar, T., & Brockhoff, D. (2021). *COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting.* Optimization Methods and Software, 36(1), 114–144. |

## Libraries and frameworks

| # | Library | Role in the project | Reference |
|---|---------|---------------------|-----------|
| 18 | **BoTorch** (built on PyTorch) | Provides the qNEI and TuRBO implementations — production, noise-aware and trust-region acquisition | Balandat, M., Karrer, B., Jiang, D. R., Daulton, S., Letham, B., Wilson, A. G., & Bakshy, E. (2020). *BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization.* NeurIPS 33, 21524–21538. |
| 19 | **scikit-learn** | GP surrogate, RBF/Matérn kernels, Ridge regression, SVM/logistic regression for diagnostics, and the random-forest / k-NN members of the `08` model-agreement ensemble | Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research, 12, 2825–2830. |
| — | **SciPy** | Statistical tests (rank correlations, χ², Shapiro–Wilk), `least_squares` for the harmonic fits, and acquisition-function maths | Virtanen, P., et al. (2020). *SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.* Nature Methods, 17, 261–272. |
| — | **NumPy / pandas / matplotlib** | Data handling and figures | NumPy: Harris, C. R., et al. (2020), *Nature* 585, 357–362. pandas: McKinney, W. (2010), *Proc. 9th Python in Science Conf.* matplotlib: Hunter, J. D. (2007), *Computing in Science & Engineering* 9(3), 90–95. |

## Notes

- **Headline citations (rubric anchors):** TuRBO, qNEI, and ZoMBI (rows 1–3) are the academic papers that directly shaped specific design decisions in this project. From the later phase, Smith & Winkler (row 9), Vehtari et al. (row 11) and the Lomb–Scargle pair (row 14) carry the same weight: each is the source of a *verdict that changed a probe*, not background reading.
- **qNEI attribution:** the *method* (Noisy Expected Improvement) originates with Letham et al. (2019); the *q-batch Monte-Carlo version I actually run* is the BoTorch implementation (row 18). Both are cited so the idea and the software are each properly credited.
- **What is mine rather than cited:** the pathology classifier and its archetype set, the referee-prices-every-module architecture, the ceiling estimator's per-archetype library, and the seven-axis hallucination critic are constructions of this project. They compose the cited primitives; they are not drawn from a paper, and the write-up should not imply otherwise.
- **Where a technique is used outside its home field:** the periodogram (astronomy) and the multiplicative-noise model (assay/potency data) are borrowed deliberately, and both are validated in-repo before being trusted — the periodogram by an independent GP with a periodic kernel, the noise model by out-of-sample predictive density. The citation licenses the tool; the notebook earns the conclusion.
- **Supporting depth:** rows 4–5 and the library rows document the wider toolchain. They are not required by the rubric but show the full technical foundation.
