"""M-DIALECTICIAN-05 (F2, F3, F6, cand D): arithmetic on the lens's simulation outputs (values read from the
lens's shape log, DR3, low bin log10 gN in [-11,-9.5], high bin [-8.5,-7.5]; gamma dimensionless).
Checks: calibrated ratio R = g_low/g_high; excess ratio (g_low-1)/(g_high-1); residual per unit f = (R-1)/f;
F6 surrogate 0.31 f; cand D: (median - gamma(0.3)) / (S - 1) ~ 0.4.  The MC values themselves are not re-derived here."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

med = {0.1: (1.077, 1.034), 0.2: (1.166, 1.098), 0.3: (1.251, 1.143)}
lens_R = {0.1: 1.042, 0.2: 1.062, 0.3: 1.094}
for f, (lo, hi) in med.items():
    R = lo / hi
    print(f"f={f}: R={R:.4f} (lens {lens_R[f]}); excess ratio {(lo - 1) / (hi - 1):.3f}; residual/f {(R - 1) / f:.3f}")
    quantity(f"{R}", f"{lens_R[f]}", rel_tol=0.001)
# excess ratio range 1.7-2.3
ex = [(lo - 1) / (hi - 1) for lo, hi in med.values()]
quantity(f"{min(ex)}", "1.7", rel_tol=0.01); quantity(f"{max(ex)}", "2.3", rel_tol=0.02)
# slope 0.31 for f >= 0.2
quantity(f"{(med[0.2][0] / med[0.2][1] - 1) / 0.2}", "0.31", rel_tol=0.01)
quantity(f"{(med[0.3][0] / med[0.3][1] - 1) / 0.3}", "0.31", rel_tol=0.02)
# a straight line through (0,0),(0.1,.042),(0.2,.062),(0.3,.094) by least squares through the origin
fs = [0.1, 0.2, 0.3]; rs = [med[f][0] / med[f][1] - 1 for f in fs]
b = sum(f * r for f, r in zip(fs, rs)) / sum(f * f for f in fs)
print(f"LSQ slope through origin over f=0.1..0.3: {b:.3f}; at f=0.1 the residual is {rs[0]:.3f} vs 0.31*0.1 = 0.031")
# p = 0.3 calibrated ratios (F2/F3)
for name, lo, hi, lens in (("Newton f=.2", 1.133, 1.096, 1.034), ("Newton f=.3", 1.171, 1.126, 1.040), ("MOND f=.2", 1.370, 1.093, 1.253)):
    print(f"{name}: p=0.3 ratio {lo / hi:.4f} (lens {lens})")
    quantity(f"{lo / hi}", f"{lens}", rel_tol=0.001)
# F6 surrogate
for f, lens in ((0.10, 0.03), (0.18, 0.06), (0.43, 0.13), (0.65, 0.20)):
    quantity(f"{0.31 * f}", f"{lens}", rel_tol=0.08)
    print(f"surrogate f={f}: {0.31 * f:.4f}; LSQ-slope version {b * f:.4f}")
# cand D: gap median - gamma(0.3) vs S - 1
for name, medv, g3, S, lens in (("f=.2", 1.166, 1.133, 1.079, 0.033), ("f=.3", 1.251, 1.171, 1.206, 0.080)):
    gap = medv - g3
    print(f"{name}: median-g(0.3) = {gap:.3f} (lens {lens}); ratio to S-1 = {gap / (S - 1):.3f}")
    quantity(f"{gap}", f"{lens}", rel_tol=0.01)
    quantity(f"{gap / (S - 1)}", "0.4", rel_tol=0.06)
# symbolic: R-1 small-excess limit: (1+x)/(1+y) - 1 ~ x - y as x, y -> 0
x, y = sp.symbols("x y", positive=True)
limit(((1 + x) / (1 + y) - 1) / (x - y), "x", y, sp.Integer(1) / (1 + y))
raise SystemExit(finish())
