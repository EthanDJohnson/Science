"""M-DIALECTICIAN-07: anchor-free one-step weighted mean (F6).

Inverse-variance mean of TDCOSMO 71.1 (+2.4/-2.3 -> 2.35), masers 71.6 +- 3.7 (stat), sirens 71.7
(+9.4/-7.5 -> 8.45) [D-31, D-32, D-33], errors symmetrised as (up+down)/2 (lens assumption).
Tensions vs CMB-SPA 67.19 +- 0.38, DESI BAO+BBN 68.50 +- 0.58, H0DN 73.264 +- 0.806. km/s/Mpc.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, units, finish
import sympy as sp

# limit-type check: with equal errors the weighted mean is the plain mean and sigma = s/sqrt(3)
x1, x2, x3, s = sp.symbols("x1 x2 x3 s", positive=True)
w = 1 / s**2
identity((w * x1 + w * x2 + w * x3) / (3 * w), (x1 + x2 + x3) / 3)
identity(1 / sp.sqrt(3 * w), s / sp.sqrt(3))

vals = [(71.1, 2.35), (71.6, 3.7), (71.7, 8.45)]
W = sum(1 / e**2 for _, e in vals)
m = sum(v / e**2 for v, e in vals) / W
sm = 1 / math.sqrt(W)
chi2 = sum((v - m) ** 2 / e**2 for v, e in vals)
print(f"mean = {m:.3f} +- {sm:.3f}; chi2 = {chi2:.4f} for 2 dof")
inequality(f"abs({m} - 71.27)", "<=", "0.005")
inequality(f"abs({sm} - 1.93)", "<=", "0.005")
inequality(f"abs({chi2} - 0.02)", "<=", "0.006")
for name, H, e, want in (("SPA", 67.19, 0.38, 2.07), ("DESI+BBN", 68.50, 0.58, 1.37), ("H0DN", 73.264, 0.806, 0.95)):
    zz = abs(m - H) / math.hypot(sm, e)
    print(f"vs {name}: z = {zz:.3f} (lens {want})")
    inequality(f"abs({zz} - {want})", "<=", "0.01")
frac = (m - 67.19) / (73.264 - 67.19)
print(f"fraction of the way SPA -> H0DN: {frac:.3f}")
inequality(f"abs({frac} - 2/3)", "<=", "0.02")
units("4.08 km/s/Mpc / (1.97 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
