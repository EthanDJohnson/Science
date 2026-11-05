"""Falsifier C1-1 (evidence angle): do H0 probes that bypass the SN Ia calibration step
agree with C1's claimed true global H0 of 67-68.5 km/s/Mpc?

Units: H0 in km/s/Mpc (astronomical units, not SI). Errors 1-sigma.
Inputs (all quoted in the run dossier or fetched by this falsifier):
  SBF (Jensen 2025, arXiv:2502.15935): 73.8 +- 0.7 stat +- 2.3 sys -> 2.40 total; no Cepheids, no SNe Ia
  Tully-Fisher (Boubel 2024, D-30): 73.3 +- 2.1 +- 3.5 -> 4.08; Cepheid/TRGB zero point, no SNe Ia
  SNe II (de Jaeger 2022, arXiv:2203.08974): 75.4 +3.8/-3.7 stat, sys 1.5 -> lower side 3.99; no SNe Ia
  TDCOSMO-2026 (D-31): 71.1 +2.4/-2.3; no ladder at all
  Megamasers (Stiskalek 2026 reanalysis, D-32): 71.6 +- 3.7 (stat only)
  GW sirens GWTC-5.0 (D-33): 71.7 +9.4/-7.5
  H0DN no-SNe Ia variant (D-23): 73.434 +- 1.795 (contains SBF, TF?, masers; used in a separate set)
Model under C1: true H0 = 67.0, 67.75, 68.5. For a measurement above the model the lower-side
error is used (the likelihood at a model value below the measurement).
Correlation: SBF, TF and SNe II share the primary-distance zero point (NGC 4258 / Cepheid / TRGB);
a common fractional anchor term of 1.5% in distance (in H0) is added as covariance among them
(and 0% / 3% as brackets). SN-step sub-hypotheses of C1 do not move any of these probes.
"""
import numpy as np
from math import erfc, sqrt
from scipy import stats

def gls(x, C):
    Ci = np.linalg.inv(C)
    one = np.ones(len(x))
    var = 1.0 / (one @ Ci @ one)
    mu = var * (one @ Ci @ x)
    return mu, sqrt(var)

def chi2_at(x, C, h):
    r = x - h
    return float(r @ np.linalg.inv(C) @ r)

def sig_from_p(p):
    # two-sided Gaussian-equivalent sigma
    return stats.norm.isf(p / 2)

sets = {
    "A: SBF, TF, SNII, TD, masers, sirens": (
        ["SBF", "TF", "SNII", "TD", "maser", "siren"],
        np.array([73.8, 73.3, 75.4, 71.1, 71.6, 71.7]),
        np.array([2.40, 4.08, 3.99, 2.30, 3.70, 7.50]),
        [0, 1, 2]),
    "B: H0DN no-SNe, SNII, TD, sirens": (
        ["H0DN-noSN", "SNII", "TD", "siren"],
        np.array([73.434, 75.4, 71.1, 71.7]),
        np.array([1.795, 3.99, 2.30, 7.50]),
        [0, 1]),
    "C: one-step only (TD, masers, sirens)": (
        ["TD", "maser", "siren"],
        np.array([71.1, 71.6, 71.7]),
        np.array([2.30, 3.70, 7.50]),
        []),
    "D: SN-Ia-free ladders only (SBF, TF, SNII)": (
        ["SBF", "TF", "SNII"],
        np.array([73.8, 73.3, 75.4]),
        np.array([2.40, 4.08, 3.99]),
        [0, 1, 2]),
}

for anchor in [0.0, 0.015, 0.03]:
    print(f"\n===== common anchor term {anchor*100:.1f}% (in H0) among ladder-based entries =====")
    for name, (labels, x, s, corr_idx) in sets.items():
        C = np.diag(s**2)
        for i in corr_idx:
            for j in corr_idx:
                if i != j:
                    C[i, j] += (anchor * x[i]) * (anchor * x[j])
        mu, sm = gls(x, C)
        chi_free = chi2_at(x, C, mu)
        n = len(x)
        print(f"{name}: GLS mean = {mu:.2f} +- {sm:.2f} km/s/Mpc; chi2 about own mean = {chi_free:.2f} for {n-1} dof")
        for h in [67.0, 67.75, 68.5]:
            z = (mu - h) / sm
            p = erfc(abs(z) / sqrt(2))
            print(f"   vs C1 true H0 = {h:5.2f}: GLS offset {mu-h:+.2f} = {z:.2f} sigma (two-sided p = {p:.2e})")
        # midpoint of the gap 70.2 (C1 needs the true value below it)
        z = (mu - 70.2) / sm
        print(f"   vs gap midpoint 70.2: {z:+.2f} sigma")

# How much would the SN-Ia-free set need to be biased high (common fractional shift)
# for C1 (true H0 = 68.5) to be within 1 sigma? (for set A, 1.5% anchor)
labels, x, s, ci = sets["A: SBF, TF, SNII, TD, masers, sirens"]
C = np.diag(s**2)
for i in ci:
    for j in ci:
        if i != j:
            C[i, j] += (0.015 * x[i]) * (0.015 * x[j])
mu, sm = gls(x, C)
print(f"\nSet A (1.5% anchor): mean {mu:.2f} +- {sm:.2f}; shortfall vs 68.5 = {mu-68.5:.2f} km/s/Mpc = "
      f"{5*np.log10(mu/68.5):.3f} mag")
# Ladder-only part of set A: the SN-Ia-free ladders must each be high by the same SN-independent amount
mu_d, sm_d = gls(x[:3], C[:3, :3])
print(f"SN-Ia-free ladders (SBF,TF,SNII) mean {mu_d:.2f} +- {sm_d:.2f}: required non-SN bias to reach 68.5 = "
      f"{5*np.log10(mu_d/68.5):.3f} mag ({100*(mu_d/68.5-1):.1f}% in distance)")
# Limit check: zero anchor + diag gives inverse-variance mean
w = 1 / s**2
print(f"check: inverse-variance mean set A (no corr) = {np.sum(w*x)/np.sum(w):.3f} +- {1/np.sqrt(np.sum(w)):.3f}")
