"""Falsifier C6-2 (bounds): what the null/hybrid C6 must contain once the
candidates' own 'dominant = more than half the gap' rule and independent bounds
are imposed.

Units: H0 in km/s/Mpc; r_d in Mpc; magnitudes in mag; ages in Gyr.
Inputs (dossier IDs): H0DN-corrected 73.264 +- 0.806 [D-22]; CMB-SPA 67.19 +- 0.38,
r_d = 147.00 Mpc [D-44]; DESI BAO+BBN 68.50 +- 0.58 [D-45]; inverse ladder
67.19 +0.66/-0.64 and 67.67 +0.69/-0.68 [D-48]; N_eff (ACT DR6) 2.86 +- 0.13 [D-52, D-74];
pure-N_eff equivalent 4.21 for a 7.0% r_d cut [D-56]; EDE / early-physics H0 posteriors
without SH0ES prior [D-52, D-53, D-94]; GC age 13.81 +- 0.25 +- 0.23 Gyr [D-55].
"""
import numpy as np
from scipy.integrate import quad

L, sL = 73.264, 0.806   # ladder pole (H0DN corrected)
E, sE = 67.19, 0.38     # early pole (CMB-SPA)
G = L - E
half = G / 2
print(f"gap G = {G:.3f} km/s/Mpc, half = {half:.3f}, midpoint = {E+half:.3f}")

# Model: L = T + S_L + F_L ; E = T - S_E + F_E, with 0 <= S_L, S_E <= G/2
# (no single cause above half the gap = C6 by the slate's boundary rule),
# F_L ~ N(0, sL), F_E ~ N(0, sE) are pure statistical fluctuations.
def min_chi2(T):
    # S_L = L - T - F_L in [0, half]  ->  F_L in [L-T-half, L-T]
    lo, hi = L - T - half, L - T
    FL = 0.0 if lo <= 0 <= hi else (lo if lo > 0 else hi)
    # S_E = T - E + F_E in [0, half]  ->  F_E in [E-T, E-T+half]
    lo, hi = E - T, E - T + half
    FE = 0.0 if lo <= 0 <= hi else (lo if lo > 0 else hi)
    SL = L - T - FL
    SE = T - E + FE
    return (FL / sL) ** 2 + (FE / sE) ** 2, SL, SE, FL, FE

print("\n(A) C6 window: true H0 T at which no cause exceeds half the gap, cost in fluctuation chi2")
Ts = np.arange(67.0, 73.01, 0.01)
res = [min_chi2(T) for T in Ts]
for thr, lab in [(1.0, "1 sigma (dchi2<=1)"), (4.0, "2 sigma (dchi2<=4)"), (9.0, "3 sigma (dchi2<=9)")]:
    ok = [T for T, r in zip(Ts, res) if r[0] <= thr]
    print(f"  {lab}: T in [{min(ok):.2f}, {max(ok):.2f}] km/s/Mpc")
for T in [68.5, 69.0, 69.5, 70.0, 70.2, 70.5, 71.0]:
    c, SL, SE, FL, FE = min_chi2(T)
    print(f"  T = {T:.2f}: min fluct chi2 = {c:6.2f}; ladder systematic S_L = {SL:.2f} ({SL/G:.0%}),"
          f" early coherent shift S_E = {SE:.2f} ({SE/G:.0%}); F_L = {FL:+.2f}, F_E = {FE:+.2f}")

# Over the 2-sigma window, the minimum early coherent shift the hybrid needs
win = [(T, r) for T, r in zip(Ts, res) if r[0] <= 4.0]
# at each T, the early shift can be traded against F_E at chi2 cost; find min S_E with total chi2<=4
best = None
for T in Ts:
    for SE in np.arange(0, half + 1e-9, 0.01):
        FE = SE - (T - E)
        SLmax = half
        # choose F_L to minimise cost given S_L in [0, half]
        lo, hi = L - T - half, L - T
        FL = 0.0 if lo <= 0 <= hi else (lo if lo > 0 else hi)
        c = (FL / sL) ** 2 + (FE / sE) ** 2
        if c <= 4.0:
            if best is None or SE < best[1]:
                best = (T, SE, c)
            break
print(f"\n  minimum early coherent shift anywhere in the 2-sigma C6 window: S_E = {best[1]:.2f} km/s/Mpc"
      f" at T = {best[0]:.2f} (chi2 {best[2]:.2f}); i.e. {best[1]/G:.0%} of the gap")
SE_mid = 70.2 - E
print(f"  at the midpoint T = 70.2 with no fluctuation: S_E = {SE_mid:.2f} km/s/Mpc ({SE_mid/G:.0%})")

# (B) Can the early shift be fluctuation in the r_s group? Residuals of each r_s-route at T if r_d standard
print("\n(B) r_s-route residuals if the true H0 is T and r_d is standard (no early physics)")
routes = {"CMB-SPA": (67.19, 0.38), "BAO+BBN (DESI DR2)": (68.50, 0.58),
          "inverse ladder (cosmography)": (67.19, 0.66), "inverse ladder (flat LCDM)": (67.67, 0.69)}
for T in [69.5, 70.2, 70.9]:
    s = ", ".join(f"{k} {(T-v)/e:.1f}sig" for k, (v, e) in routes.items())
    print(f"  T = {T}: {s}")
# joint chi2 for the three (approx. independent: CMB-SPA, BAO+BBN, inverse ladder) at T=70.2
for T in [69.5, 70.2]:
    chi = sum(((T - v) / e) ** 2 for k, (v, e) in routes.items() if k != "inverse ladder (flat LCDM)")
    print(f"  T = {T}: summed chi2 of CMB-SPA + BAO+BBN + inverse ladder = {chi:.1f} for 3 dof")

# (C) Required r_d reduction (H0*r_d fixed by BAO+SN, inverse-ladder anchor 67.43)
print("\n(C) r_d the hybrid needs (H0 r_d held at the inverse-ladder value)")
Hinv = 0.5 * (67.19 + 67.67)
for T in [best[0], 69.5, 70.2, 70.9]:
    rd = 147.00 * Hinv / T
    print(f"  T = {T:.2f}: r_d = {rd:.1f} Mpc, reduction {1 - rd/147.00:.1%}")

# (D) Variant bounds. Pure N_eff route: D-56 maps a 7.0% r_d cut to N_eff = 4.21 (from 3.044).
slope = (4.21 - 3.044) / 7.0   # N_eff per percent of r_d cut (linear, conservative near 0)
print(f"\n(D) Dark-radiation route: dN_eff per 1% r_d cut = {slope:.3f}")
for cut in [100 * (1 - Hinv / best[0]), 100 * (1 - Hinv / 69.5), 100 * (1 - Hinv / 70.2)]:
    Neff = 3.044 + slope * cut
    print(f"  r_d cut {cut:.1f}% -> N_eff = {Neff:.2f}, vs ACT DR6 2.86 +- 0.13: {(Neff-2.86)/0.13:.1f} sigma;"
          f" vs 2.89 +- 0.11 (with He, D): {(Neff-2.89)/0.11:.1f} sigma")

# EDE-like / recombination posteriors (no SH0ES prior): is the C6 window inside them?
post = {
    "P-ACT-LB EDE 69.9 +0.8/-1.5 [D-52]": (69.9, 0.8, 1.5),
    "P-ACT EDE 69.3 +0.9/-1.5 [D-52]": (69.3, 0.9, 1.5),
    "ACT-alone EDE 67.5 +0.9/-1.7 [D-52]": (67.5, 0.9, 1.7),
    "Poulin 2026 profile EDE 71.0 +-1.1 [D-53]": (71.0, 1.1, 1.1),
    "eROSITA+CMB+BAO EDE 71.4 +-1.4 [D-94]": (71.4, 1.4, 1.4),
    "modified recombination 69.6 +-1.0 [D-52]": (69.6, 1.0, 1.0),
    "PMF 69.1 +-0.5 [D-52]": (69.1, 0.5, 0.5),
}
print("\n  early-physics posteriors vs the C6 window (T above the posterior uses the + error)")
for k, (m, up, dn) in post.items():
    s = ", ".join(f"T={T}: {((T-m)/(up if T>m else dn)):+.1f}sig" for T in [69.5, 70.2, 70.9])
    print(f"  {k}: {s}")
print("  Planck NPIPE EDE: 66.9 < H0 < 69.5 (95%) [D-53] -> C6 midpoint 70.2 lies outside this 95% range;"
      " the C6 2-sigma window lower end is compared above")

# (E) Age bound: flat LCDM t0 for T and Omega_m = 0.3175 (CMB-SPA), radiation ignored
def t0(H0, Om):
    Hs = H0 / 977.792  # 1/Gyr per km/s/Mpc
    f = lambda a: 1.0 / (a * np.sqrt(Om / a**3 + 1 - Om))
    return quad(f, 1e-8, 1)[0] / Hs
print("\n(E) age check (flat LCDM, Omega_m = 0.3175; check t0(67.19) vs CMB-SPA 13.805 Gyr)")
print(f"  t0(67.19) = {t0(67.19, 0.3175):.3f} Gyr")
sg = np.hypot(0.25, 0.23)
for T in [69.5, 70.2, 70.9, 73.26]:
    tt = t0(T, 0.3175)
    print(f"  T = {T}: t0 = {tt:.2f} Gyr; GC 13.81 +- {sg:.2f}: {(tt-13.81)/sg:+.1f} sigma")

# (F) Sub-hypothesis (b): ladder-only diffuse shift needed for 2-sigma consistency [lens-constraints_void_null]
for shift, lab in [(4.29, "vs CMB-SPA"), (2.78, "vs BAO+BBN")]:
    print(f"\n(F) (b) unmodelled common ladder shift {shift} km/s/Mpc {lab} = {shift/G:.0%} of the gap"
          f" -> {'above' if shift/G > 0.5 else 'below'} the half-gap 'dominant' threshold")
