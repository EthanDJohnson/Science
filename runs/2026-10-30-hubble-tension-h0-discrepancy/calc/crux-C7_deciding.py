"""Crux C7: precision thresholds for the deciding observations.

Units: H0 in km/s/Mpc, magnitudes in mag (astronomical units, not SI).
Inputs (all from the dossier, the math checks or the C7 verdicts):
  anchor group 73.02 +- 0.78, r_d group 67.51 +- 0.29   [M-EXAMINER-06]
  H0DN 73.264 +- 0.806 [D-22], CMB-SPA 67.19 +- 0.38 [D-44]
  SH0ES 73.49 +- 0.93 [D-20]
  Najera et al. 2026 free legacy offset: dM = 0.0646 +- 0.0391 mag, H0 = 71.03 +- 1.99,
  legacy as published 67.98 +- 0.69 (quoted in verdict C7-0)
Uncorrelated Gaussian errors throughout (a simplification; NGC 4258 is shared by
SH0ES and any TRGB ladder, which would make the SH0ES-vs-independent split tests
more demanding, not less).
"""
from math import sqrt


def sig_needed(delta, nsig, sigma_pole):
    """Arbiter sigma such that delta / sqrt(s^2 + sigma_pole^2) = nsig; None if impossible."""
    v = (delta / nsig) ** 2 - sigma_pole ** 2
    return sqrt(v) if v > 0 else None


def fmt(x):
    return "impossible" if x is None else f"{x:.2f}"


print("== 1. Arbiter (anchor-free, r_d-free H0): landing at one pole, excluding the other ==")
for label, A, sA, R, sR in [("group means", 73.02, 0.78, 67.51, 0.29),
                            ("H0DN vs CMB-SPA", 73.264, 0.806, 67.19, 0.38)]:
    d = A - R
    print(f"{label}: separation {d:.3f} km/s/Mpc")
    for n in (3, 5):
        print(f"  arbiter at anchor pole excludes r_d pole at {n}sigma: sigma_arb <= {fmt(sig_needed(d, n, sR))}")
        print(f"  arbiter at r_d pole excludes anchor pole at {n}sigma: sigma_arb <= {fmt(sig_needed(d, n, sA))}")
    half = d / 2
    mid = (A + R) / 2
    print(f"  midpoint {mid:.2f}; C6-type midpoint excluding both poles at 3sigma: "
          f"sigma_arb <= {fmt(min(x for x in (sig_needed(half, 3, sA), sig_needed(half, 3, sR)) if x))}")

print()
print("== 1b. Arbiter values at sigma_arb = 1.2 that reach 3sigma from each pole ==")
s = 1.2
print(f"  3sigma above CMB-SPA 67.19+-0.38: >= {67.19 + 3*sqrt(s**2+0.38**2):.2f}")
print(f"  3sigma below H0DN 73.264+-0.806: <= {73.264 - 3*sqrt(s**2+0.806**2):.2f}")

print()
print("== 2. Najera et al. 2026 free-legacy-offset case ==")
H, sH = 71.03, 1.99
for name, P, sP in [("H0DN", 73.264, 0.806), ("CMB-SPA", 67.19, 0.38)]:
    print(f"  71.03+-1.99 vs {name}: {abs(H-P)/sqrt(sH**2+sP**2):.2f} sigma")
dM, sdM = 0.0646, 0.0391
print(f"  legacy offset significance now: {dM/sdM:.2f} sigma")
for n in (3, 5):
    print(f"  sigma(dM_legacy) to separate {dM} mag from 0 at {n}sigma: <= {dM/n:.4f} mag")
# the offset in magnitudes versus the full gap
gap_mag = 0.188
print(f"  offset as fraction of the 0.188 mag gap: {dM/gap_mag:.2f}")

print()
print("== 3. C8 test: independent full-sample TRGB/JAGB ladder vs SH0ES 73.49+-0.93 ==")
S, sS = 73.49, 0.93
for sig in (1.1, 0.8, 0.6):
    s = sqrt(sig**2 + sS**2)
    print(f"  sigma_ind={sig}: combined {s:.2f}; split 2sigma needs result <= {S-2*s:.2f}, 3sigma <= {S-3*s:.2f}")
    for val in (70.0, 71.0, 72.0):
        print(f"     result {val}: split {(S-val)/s:.2f} sigma from SH0ES")
# separation of C8 centre (71) from C7 anchor-group mean (73.02) by an independent ladder
d8 = 73.02 - 71.0
for n in (2, 3):
    print(f"  to tell 71.0 from 73.02 at {n}sigma (vs anchor-group error 0.78): sigma_ind <= {fmt(sig_needed(d8, n, 0.78))}")
    print(f"  to tell 71.0 from 73.02 at {n}sigma (pure measurement error): sigma_ind <= {d8/n:.2f}")
