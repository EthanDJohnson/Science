"""M-MECHANIST-09: inverse-variance means (finding 8), errors symmetrised as the mean of upper and lower.
One-step: TDCOSMO 71.1 +2.4/-2.3 [D-31], masers 71.6 ± 3.7 (stat only) [D-32], sirens 71.7 +9.4/-7.5 [D-33].
Add SBF 73.8 ± 0.7 ± 2.3 [D-29], TF 73.3 ± 2.1 ± 3.5 [D-30] (stat and sys in quadrature).
Tension vs CMB-SPA 67.19 ± 0.38 and H0DN 73.264 ± 0.806; gap fraction (mean - 67.19)/(73.264 - 67.19).
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, limit, finish
from mm_common import near, tension

x1, x2, s1, s2 = sp.symbols("x1 x2 s1 s2", positive=True)
wm = (x1 / s1**2 + x2 / s2**2) / (1 / s1**2 + 1 / s2**2)
identity(wm, (x1 * s2**2 + x2 * s1**2) / (s1**2 + s2**2))
print("limit s2 -> oo gives x1:", sp.limit(wm, s2, sp.oo))
limit("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "s2", "oo", "x1")


def wmean(pts):
    w = [1 / s**2 for _, s in pts]
    return sum(x * wi for (x, _), wi in zip(pts, w)) / sum(w), 1 / math.sqrt(sum(w))


one = [(71.1, (2.4 + 2.3) / 2), (71.6, 3.7), (71.7, (9.4 + 7.5) / 2)]
m, s = wmean(one)
near("one-step mean", m, 71.27, 0.01)
near("one-step sigma", s, 1.93, 0.01)
near("vs CMB-SPA", tension(m, s, 67.19, 0.38), 2.1, 0.05)
near("vs H0DN", tension(m, s, 73.264, 0.806), 1.0, 0.1)
near("gap fraction", (m - 67.19) / (73.264 - 67.19), 0.67, 0.01)
near("gap fraction sigma", s / (73.264 - 67.19), 0.32, 0.01)
nosn = one + [(73.8, math.hypot(0.7, 2.3)), (73.3, math.hypot(2.1, 3.5))]
m2, s2v = wmean(nosn)
near("no-SN mean", m2, 72.39, 0.015)
near("no-SN sigma", s2v, 1.41, 0.01)
near("no-SN vs CMB-SPA", tension(m2, s2v, 67.19, 0.38), 3.6, 0.05)
raise SystemExit(finish())
