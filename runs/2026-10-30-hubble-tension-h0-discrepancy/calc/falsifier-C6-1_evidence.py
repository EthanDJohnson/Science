"""Falsifier C6-1 (evidence angle): what the published early-side values leave for
the null's 'comparable partial contributions' under the slate's own boundary rule.

Units: H0 in km/s/Mpc (astronomical units, not SI). Fractions dimensionless.
Boundary rule (candidates.md conventions): a cause is dominant if it carries more
than half of the gap, i.e. moves the true global H0 across the midpoint.

Inputs (dossier IDs):
  H0DN corrected 73.264 +- 0.806 [D-22]; CMB-SPA 67.19 +- 0.38 [D-44]
  Early-side 'true H0' scenarios from published fits:
    CMB-only LCDM 67.19 [D-44]
    DESI BAO+BBN 68.50 [D-45]  (DESI-CMB Omega_m offset taken as an early-side bias)
    Planck NPIPE EDE 95% upper H0 69.5 [D-53]
    ACT P-ACT-LB EDE 69.9 [D-52]
    CMB-SPA+DESI EDE ~ (not quoted as H0; skipped)
    Poulin 2026 EDE profile 71.0 [D-53]
    eROSITA EDE 71.4 [D-94]
"""
import math

H_loc, s_loc = 73.264, 0.806
H_cmb, s_cmb = 67.19, 0.38
gap = H_loc - H_cmb
half = gap / 2.0
s_gap = math.hypot(s_loc, s_cmb)
print(f"gap = {gap:.3f} km/s/Mpc, half = {half:.3f}, sigma_gap (stat, uncorrelated) = {s_gap:.3f}")
print(f"midpoint true H0 = {H_cmb + half:.3f} km/s/Mpc")
print()

scen = [
    ("CMB-only LCDM (no early shift)", 67.19),
    ("DESI BAO+BBN (Omega_m offset as early bias)", 68.50),
    ("Planck NPIPE EDE 95% upper H0", 69.5),
    ("ACT P-ACT-LB EDE central", 69.9),
    ("Poulin 2026 EDE profile central", 71.0),
    ("eROSITA EDE central", 71.4),
]
print("early-side shift b_E = H_true - 67.19; ladder share if no fluctuation b_L = gap - b_E;")
print("min upward fluctuation eps needed so that b_L < half (C6 rather than C1): eps = gap - b_E - half")
print(f"{'scenario':48s} {'b_E':>6s} {'fracE':>6s} {'b_L(eps=0)':>10s} {'fracL':>6s} {'eps_min':>8s} {'eps/sig':>8s}  class")
for name, H in scen:
    bE = H - H_cmb
    fE = bE / gap
    bL0 = gap - bE
    fL0 = bL0 / gap
    eps = max(0.0, gap - bE - half)
    if fE > 0.5:
        cls = "C3 (early part > half)"
    elif eps > 0:
        cls = f"C6 only if eps >= {eps:.2f} ({eps/s_gap:.2f} sigma); else C1"
    else:
        cls = "C6 window open with eps = 0"
    print(f"{name:48s} {bE:6.2f} {fE:6.3f} {bL0:10.2f} {fL0:6.3f} {eps:8.2f} {eps/s_gap:8.2f}  {cls}")

print()
# Gaussian one-sided probability of an upward fluctuation >= eps of the measured gap
def p_up(z):
    return 0.5 * math.erfc(z / math.sqrt(2))
for name, H in scen[:4]:
    bE = H - H_cmb
    eps = max(0.0, gap - bE - half)
    print(f"P(fluct >= {eps:.2f} | {name}) = {p_up(eps/s_gap):.3g}")

print()
# Sub-hypothesis (a) as stated: 'best fits closing 30-67%'; classify the quoted fits
print("C6(a) cites early fits 'closing 30-67%'. Fractions of the H0DN-CMB-SPA gap:")
for H in (69.1, 69.5, 69.9, 70.5, 71.0, 71.4):
    f = (H - H_cmb) / gap
    print(f"  H_fit = {H:5.1f}: fraction {f:.3f} -> {'C3 by boundary rule' if f > 0.5 else 'within C6 early part'}")

print()
# Sub-hypothesis (b): common unmodelled ladder shift to bring H0DN within 2 sigma of CMB-SPA
S = gap - 2 * s_gap
print(f"C6(b) common ladder shift for 2 sigma: S = gap - 2*sigma_gap = {S:.2f} km/s/Mpc = {S/gap:.3f} of gap -> {'C1 by boundary rule' if S/gap > 0.5 else 'C6'}")
# ladder-side error inflation (all on local side) for 2 sigma
sl = math.sqrt((gap / 2) ** 2 - s_cmb ** 2)
print(f"C6(b) local error needed for 2 sigma: {sl:.3f} km/s/Mpc = x{sl/s_loc:.2f} of 0.806")
# compare with H0DN analysis-variant spread
print("H0DN variant-centre dispersion 0.400 km/s/Mpc [D-23]: ratio needed error / variant spread =", f"{sl/0.400:.1f}")
