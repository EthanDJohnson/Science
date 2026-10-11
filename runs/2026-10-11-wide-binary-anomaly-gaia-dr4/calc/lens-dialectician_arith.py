"""Dialectician lens, calc 3: arithmetic on published values and on the shape.py log numbers.
All gamma dimensionless. Inputs typed from dossier rows (D-22, D-31, D-90) and from
calc/lens-dialectician_shape.py.log (DR3/DR4 rows quoted below).
"""
import math

print("(1) Same-catalogue decomposition of the Chae-vs-Boufourou gap, in ln(gamma)")
chae, rob = 1.368, 1.045          # Chae 2024b Gamma=0.068 -> 1.368 (D-22); Boufourou E2 (D-31)
for fm in (1.12, 1.20):           # Boufourou's implied full-median on the same catalogue (D-31/D-90)
    tot = math.log(chae) - math.log(rob)
    est = math.log(fm) - math.log(rob)
    print(f"  implied full-median {fm:.2f}: estimator share {est/tot:.2f}, sample/template/calibration share {1-est/tot:.2f} (total ln-gap {tot:.3f})")

print("(2) Calibrated full-median residual, Newton + triples (DR3), low/high bin medians from shape.py log")
for f, lo, hi in ((0.1, 1.077, 1.034), (0.2, 1.166, 1.098), (0.3, 1.251, 1.143)):
    r = lo / hi
    print(f"  f_triple={f}: ratio {r:.3f}; residual per unit f {(r-1)/f:.3f}; leverage ratio (lo-1)/(hi-1) {(lo-1)/(hi-1):.2f}")
for f, lo, hi, lab in ((0.2, 1.133, 1.096, "Newton f=0.2"), (0.3, 1.171, 1.126, "Newton f=0.3"),
                       (0.2, 1.370, 1.093, "MOND chae2024 f=0.2")):
    print(f"  p=0.3 calibrated ratio {lab}: {lo/hi:.3f}")
print("  surrogate residual at Chae's self-calibrated f_multi values (linear in f, slope ~0.31): ",
      ", ".join(f"f={f}: +{0.31*f:.3f}" for f in (0.10, 0.18, 0.43, 0.65)))

print("(3) Veto-ladder intercepts (DR4): linear in surviving triple fraction, first and last rungs")
for lab, (f1, g1), (f2, g2), truth in (("Newton f=0.2", (0.201, 1.135), (0.026, 1.021), 1.0),
                                       ("Newton f=0.3", (0.300, 1.217), (0.044, 1.051), 1.0),
                                       ("MOND chae2024 f=0.2", (0.199, 1.396), (0.025, 1.278), 1.255),
                                       ("const 1.4 f=0.2", (0.201, 1.556), (0.027, 1.426), 1.364)):
    slope = (g1 - g2) / (f1 - f2)
    icpt = g2 - slope * f2
    print(f"  {lab:22s} slope {slope:.3f} per unit triple fraction; intercept {icpt:.3f}; no-triple same-seed-class truth {truth:.3f}")
