"""Falsifier C3-0 (magnitude): how much of the local-vs-early H0 gap can
pre-recombination new physics (EDE-led) carry, given fits made WITHOUT a
ladder prior?  Units: H0 in km/s/Mpc, f_EDE dimensionless, ages in Gyr.

C3's own dominance criterion (candidates.md): true global H0 above the midpoint
of 67.19 (CMB-SPA LCDM) and 73.264 (H0DN), i.e. early shift > half the gap,
with the residual ladder offset smaller than the r_d-driven shift.
Inputs are dossier numbers D-20, D-22, D-44, D-49, D-52, D-53, D-55, D-94 and
the lens background mapping H0(f_EDE) (calc/lens-constraints_early.py.log,
verified as M-CONSTRAINTS-07).
"""
import math
from scipy.stats import norm

H_SPA, H_DN, H_SH0ES = 67.19, 73.264, 73.49
H_ACT_LCDM = 68.2  # ACT P-ACT-LB LCDM baseline (D-52)
gap = H_DN - H_SPA
mid = 0.5 * (H_SPA + H_DN)
mid_sh = 0.5 * (H_SPA + H_SH0ES)
mid_act = 0.5 * (H_ACT_LCDM + H_DN)
print(f"A. gap(H0DN - SPA) = {gap:.3f} km/s/Mpc; midpoint = {mid:.3f}; "
      f"midpoint vs SH0ES = {mid_sh:.3f}; midpoint from ACT own LCDM 68.2 = {mid_act:.3f}")

def p_above(m, mu, sp, sm):
    """P(X > m) for a split-normal with mode mu, upper sigma sp, lower sigma sm."""
    if m >= mu:
        return (sp / (sp + sm)) * 2 * (1 - norm.cdf((m - mu) / sp))
    return 1 - (sm / (sp + sm)) * 2 * norm.cdf((m - mu) / sm)

# sanity: symmetric case equals the normal tail; split-normal integrates to 1 at -inf
assert abs(p_above(1.0, 0.0, 1.0, 1.0) - (1 - norm.cdf(1.0))) < 1e-12
assert abs(p_above(-50, 0.0, 0.8, 1.5) - 1.0) < 1e-9 and abs(p_above(50, 0.0, 0.8, 1.5)) < 1e-9
assert abs(p_above(0.0, 0.0, 0.8, 1.5) - 0.8 / 2.3) < 1e-12  # mass above mode = sp/(sp+sm)

# ---------------- B. f_EDE needed to reach the midpoint ----------------
# lens background mapping, Omega_m fixed, z_c = 3500 (log rows)
bg = [(0.00, 67.21), (0.05, 69.48), (0.07, 70.45), (0.10, 71.98), (0.12, 73.05)]
def f_for(H, table):
    for (f1, h1), (f2, h2) in zip(table, table[1:]):
        if h1 <= H <= h2:
            return f1 + (f2 - f1) * (H - h1) / (h2 - h1)
    return float('nan')
f_mid_bg = f_for(mid, bg)
# full-Boltzmann calibration: line through the LCDM baseline (f=0, 67.19) and
# each no-ladder-prior full fit (Poulin f=0.09 -> 71.0; eROSITA f=0.10 -> 71.4)
slopes = {"Poulin profile": (71.0 - H_SPA) / 0.09, "eROSITA+ext": (71.4 - H_SPA) / 0.10}
print("\nB. f_EDE needed for the dominance midpoint", f"{mid:.2f}")
print(f"   background mapping (Omega_m fixed, z_c=3500): f_mid = {f_mid_bg:.4f}; full closure f = {f_for(H_DN, bg):.4f}")
for k, s in slopes.items():
    print(f"   full-fit calibration via {k}: dH0/df = {s:.1f} km/s/Mpc per unit f -> f_mid = {(mid-H_SPA)/s:.4f}, full closure f = {gap/s:.4f}")
f_mid_lo = min(f_mid_bg, *[(mid - H_SPA) / s for s in slopes.values()])
f_mid_hi = max(f_mid_bg, *[(mid - H_SPA) / s for s in slopes.values()])
print(f"   => dominance threshold f_EDE ~ {f_mid_lo:.3f}-{f_mid_hi:.3f}")
for name, fb in [("Planck NPIPE", 0.061), ("SPT+ACT+Planck", 0.070), ("P-ACT-LB", 0.12)]:
    print(f"   95% upper bound {name}: f < {fb:.3f}  -> bound/threshold = {fb/f_mid_lo:.2f}-{fb/f_mid_hi:.2f}")

# ---------------- C. dominance probability for each no-ladder fit ----------------
print("\nC. Fits without a ladder prior: share of gap (from 67.19 to 73.264), P(H0 > midpoint), ladder residual vs early shift")
fits = [
    ("ACT P-ACT EDE (Bayes)",          69.3, 0.9, 1.5),
    ("ACT P-ACT-LB EDE (Bayes)",       69.9, 0.8, 1.5),
    ("ACT P-ACT-LB mod. recomb.",      69.6, 1.0, 1.0),
    ("ACT P-ACT-LB PMF",               69.1, 0.5, 0.5),
    ("Poulin 2026 EDE (profile)",      71.0, 1.1, 1.1),
    ("eROSITA+ext EDE (Bayes)",        71.4, 1.4, 1.4),
]
for name, mu, sp, sm in fits:
    share = (mu - H_SPA) / gap
    p = p_above(mid, mu, sp, sm)
    p_act = p_above(mid_act, mu, sp, sm)
    early, resid = mu - H_SPA, H_DN - mu
    print(f"   {name:30s} H0={mu:5.2f}: share={100*share:5.1f}%  P(H0>{mid:.2f})={p:.2f}  "
          f"P(H0>{mid_act:.2f} [ACT baseline])={p_act:.2f}  early shift={early:.2f} vs ladder residual={resid:.2f} "
          f"-> {'early dominant' if early > resid else 'NOT dominant'}")
# Planck NPIPE 95% interval 66.9 < H0 < 69.5
print(f"   Planck NPIPE EDE: 95% interval 66.9-69.5 -> midpoint {mid:.2f} lies {mid-69.5:.2f} km/s/Mpc ABOVE the 95% upper edge")

print("\n   f_EDE posteriors including DESI DR2 (split-normal), P(f > threshold):")
for name, mu, sp, sm in [("SPT+ACT+Planck+DESI DR2", 0.055, 0.024, 0.047), ("SPT+DESI DR2", 0.081, 0.037, 0.052),
                         ("Poulin profile", 0.09, 0.03, 0.03), ("eROSITA+ext", 0.10, 0.04, 0.03)]:
    print(f"   {name:26s} f={mu:.3f}: P(f>{f_mid_lo:.3f})={p_above(f_mid_lo, mu, sp, sm):.2f}  "
          f"P(f>{f_mid_hi:.3f})={p_above(f_mid_hi, mu, sp, sm):.2f}; implied H0 (bg map) = {67.21 + (mu/0.05)*(69.48-67.21) if mu<=0.05 else (69.48 + (mu-0.05)/0.02*(70.45-69.48) if mu<=0.07 else 70.45 + (mu-0.07)/0.03*(71.98-70.45)):.2f}")

# ---------------- D. r_d-free H0: C3 predicts these read the true H0 (>= 71, and > midpoint) ----------------
print("\nD. r_d-free H0 (bypass r_d, so under C3 they should read the true, high H0)")
rsfree = [("Zaborowski CMBlens x unWISE", 69.2, 1.3, 1.4), ("Zaborowski DES Y3 6x2pt", 70.3, 1.4, 1.2),
          ("Zaborowski CMBlens + DES Y5", 69.6, 1.3, 1.8), ("2411.16677 DESY5", 66.7, 1.7, 1.9),
          ("2411.16677 Pantheon+", 67.9, 1.9, 2.1), ("2411.16677 Union3", 67.8, 2.0, 2.2),
          ("Philcox equality (BAO-lensing)", 70.6, 3.7, 5.0)]
for name, mu, sp, sm in rsfree:
    z71 = (71.0 - mu) / sp
    print(f"   {name:32s} {mu:5.1f}: P(H0>{mid:.2f})={p_above(mid, mu, sp, sm):.2f}  P(H0>71.0)={p_above(71.0, mu, sp, sm):.2f}  "
          f"(71 lies {z71:.2f} upper-sigma above)")
# combine the three Zaborowski values as if fully correlated (take the best-constrained single) and as if independent (upper bound on power)
ws = [(m, 0.5 * (a + b)) for _, m, a, b in rsfree[:3]]
wsum = sum(1 / s**2 for _, s in ws)
mean = sum(m / s**2 for m, s in ws) / wsum
sig_ind = wsum ** -0.5
for lab, sig in [("independent (too strong)", sig_ind), ("fully correlated (conservative)", 1.32)]:
    print(f"   Zaborowski combined, {lab}: {mean:.2f} +- {sig:.2f} -> P(H0>{mid:.2f})={1-norm.cdf((mid-mean)/sig):.2f}, "
          f"P(H0>71)={1-norm.cdf((71-mean)/sig):.2f}")

# ---------------- E. age at the dominance threshold ----------------
print("\nE. Age: EDE leaves the late-time history alone, so at fixed Omega_m t0 scales as 1/H0 (13.803 Gyr at 67.19, M-CONSTRAINTS-06)")
for H in [mid, 71.0, 71.4, H_DN]:
    t0 = 13.803 * H_SPA / H
    print(f"   H0={H:6.2f}: t0={t0:.2f} Gyr, {(13.81 - t0)/math.hypot(0.25, 0.23):.2f} sigma below GC age 13.81 +- 0.34")
