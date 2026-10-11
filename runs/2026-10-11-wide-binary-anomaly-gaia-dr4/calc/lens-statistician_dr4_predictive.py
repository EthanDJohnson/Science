"""Statistician lens: conditional DR4 predictive distributions of the reported gamma per estimator family.

gamma = G_eff/G (dimensionless), scoring bin per brief (contains g_N = 1e-10 m s^-2).
Model for each family f and hypothesis H in {Newton, MOND}:
  gamma_DR4 = truth_H + persistence of the family's DR3 offset (anchored on its published DR3 value)
              + N(0, sigma_stat_DR4) + N(0, sigma_analyst)
Rationale: DR4 re-observes the same stars with the same estimators; under either hypothesis one camp's
DR3 result is a bias, and a bias tied to the estimator and the population persists in part.
Every input is printed. Monte Carlo with 400k draws per cell.
"""
import math
import numpy as np

rng = np.random.default_rng(20261011)
M = 400_000

# ---- sigma_stat scaling DR3 -> DR4: k = N_DR4/N_DR3 log-uniform in [2, 5] (Boufourou 3-5x [D-52];
#      ESA proper-motion gain ~2.4x [D-51] extends usable distance).
k = np.exp(rng.uniform(math.log(2), math.log(5), M))
sig_dr3 = {"F1": 0.095, "F2": 0.040, "F3": 0.025, "F4": 0.20}
# F1: Chae 2024b stat (sym) [D-22]. F2: between Boufourou global 0.0215 and deep 0.07 [D-31] (bin rule
# ambiguous for his deep bin, centre log g_N ~ -10.9). F3: Banik+24 converted [D-28]. F4: 36-pair Bayes
# [D-26]; DR4 does not add precise relative RVs (Gaia RVS ~1-6 km/s >> 0.1-0.5 km/s orbital) [D-13], so
# F4 sample growth is set by ground RVs: k4 log-uniform [1, 3].
k4 = np.exp(rng.uniform(0, math.log(3), M))
print("sigma_stat DR3 -> DR4 (median of k):")
for f, s in sig_dr3.items():
    kk = k4 if f == "F4" else k
    print(f"  {f}: DR3 {s:.3f} -> DR4 median {np.median(s/np.sqrt(kk)):.4f} [range {s/math.sqrt(kk.max()):.4f}-{s/math.sqrt(kk.min()):.4f}]")

# ---- truths
g_newton = np.ones(M)
# MOND truth in the scoring bin: generator bin-median 1.28-1.31 (bz18/chae, pseudo-Newtonian),
# Chae eq.22 1.333 at 1e-10 [D-44], BZ18 asymptote 1.42 [D-43], Pflamm-Altenburg two-body 1.2-1.3 [D-45]
g_mond = rng.normal(1.32, 0.05, M)

# ---- family offsets (multiplicative on truth) under each hypothesis
#   Under Newton:
#    F1 (Chae-style calibrated median): DR3 anchor 1.33 (F1 GLS mean, rho=0.5, finding 4) is an artefact of
#       size 0.33; DR4 epoch astrometry/acceleration solutions remove part: persistence pi ~ U(0.4, 1.0).
#    F2 (tail-truncated, Boufourou-type): DR3 1.045 global / 1.11 deep; own injection 1.05-1.12 -> offset
#       N(0.06, 0.03).
#    F3 (mixture): DR3 0.99 (Banik) / 1.05 (Boufourou E3); own injection 1.01-1.04 -> N(0.02, 0.025).
#    F4 (Bayes 3D): first DR4 paper from Chae camp with geometric deprojection with prob 0.65 (they published
#       2025 and 2026 [D-25, D-26]); offset Chae-type N(0.35, 0.15) (1.48-1.60 on DR3, 2 escape-speed
#       systems [D-26]); Saad&Ting-type N(0.0, 0.05).
#   Under MOND (truth g_mond):
#    F1: own injection 0.95-1.10 x truth -> factor N(1.02, 0.04).
#    F2, F3: DR3 values 1.045/0.99 must be suppression of a real boost by something absent from synthetic
#       tests (own and Boufourou's injections recover >= 0.94 x truth). Suppression s = recovered fraction of
#       (truth-1): DR3 implies s ~ 0.15-0.35; DR4 cleaner samples may reduce suppression: s ~ U(0.15, 0.8).
#    F4: Chae-type factor N(1.10, 0.10); Saad&Ting-type N(0.85, 0.10) (their 1.00 on DR3 would be low).
sa = {"F1": 0.05, "F2": 0.035, "F3": 0.035, "F4": 0.12}   # analyst-choice spread (cuts, f_multi priors, f(e))
print("analyst-choice spread:", sa)


def draw(f, H):
    kk = k4 if f == "F4" else k
    st = sig_dr3[f] / np.sqrt(kk) * rng.standard_normal(M)
    an = sa[f] * rng.standard_normal(M)
    if H == "Newton":
        if f == "F1":
            g = 1 + 0.33 * rng.uniform(0.4, 1.0, M)
        elif f == "F2":
            g = 1 + rng.normal(0.06, 0.03, M)
        elif f == "F3":
            g = 1 + rng.normal(0.02, 0.025, M)
        else:
            chae = rng.random(M) < 0.65
            g = np.where(chae, 1 + rng.normal(0.35, 0.15, M), 1 + rng.normal(0.0, 0.05, M))
    else:
        t = g_mond
        if f == "F1":
            g = t * rng.normal(1.02, 0.04, M)
        elif f in ("F2", "F3"):
            g = 1 + (t - 1) * rng.uniform(0.15, 0.8, M)
        else:
            chae = rng.random(M) < 0.65
            g = np.where(chae, t * rng.normal(1.10, 0.10, M), t * rng.normal(0.85, 0.10, M))
    return g + st + an


print("\nfamily | hypothesis | median | 68% interval | P(0.95<=g<=1.05) | P(g>1.25) | mean | sd")
res = {}
for f in ("F1", "F2", "F3", "F4"):
    for H in ("Newton", "MOND"):
        x = draw(f, H)
        q16, q50, q84 = np.quantile(x, [0.16, 0.5, 0.84])
        p1 = np.mean((x >= 0.95) & (x <= 1.05))
        p2 = np.mean(x > 1.25)
        res[(f, H)] = x
        print(f"{f} | {H:6s} | {q50:.3f} | [{q16:.3f}, {q84:.3f}] | {p1:.3f} | {p2:.3f} | {x.mean():.3f} | {x.std():.3f}")

# discrimination: how well does each family's DR4 value separate the hypotheses? (log Bayes factor at the
# median of each conditional, via histogram densities)
print("\nDiscriminating power: density ratio p(x|MOND)/p(x|Newton) evaluated at each conditional median")
bins = np.linspace(0.5, 2.2, 341)
for f in ("F1", "F2", "F3", "F4"):
    hN, _ = np.histogram(res[(f, "Newton")], bins, density=True)
    hM, _ = np.histogram(res[(f, "MOND")], bins, density=True)
    for H in ("Newton", "MOND"):
        m = np.median(res[(f, H)])
        i = np.searchsorted(bins, m) - 1
        print(f"  {f} at median|{H}: {m:.3f}  LR(M:N) = {hM[i]/max(hN[i],1e-9):.3g}")

# Example combination for the main session (illustrative weights, NOT the judge's): w_N = 0.75, w_M = 0.25
print("\nIllustrative combination with P(Newton)=0.75 (main session must substitute the judge's credences):")
for f in ("F1", "F2", "F3", "F4"):
    sel = rng.random(M) < 0.75
    x = np.where(sel, res[(f, "Newton")], res[(f, "MOND")])
    q16, q50, q84 = np.quantile(x, [0.16, 0.5, 0.84])
    print(f"  {f}: median {q50:.3f} 68% [{q16:.3f}, {q84:.3f}] P[0.95,1.05]={np.mean((x>=0.95)&(x<=1.05)):.3f} P(>1.25)={np.mean(x>1.25):.3f}")
