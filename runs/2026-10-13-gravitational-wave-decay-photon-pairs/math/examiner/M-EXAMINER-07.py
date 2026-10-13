"""M-EXAMINER-07 (SI): far-zone fraction table, F(R) = F(wR = 10) * (10/(wR))^3 with F(10) = 2.7e-3 (lens toy law,
labelled extrapolation; M-EXAMINER-04 gives 3.0e-3 to 4.9e-3 at wR = 10 depending on window), w = 2 pi f_GW.
Also sigma * t_prop for GW150914 (sigma = 200 rad/s, d = 410 Mpc, t_prop = d/c, Euclidean light-travel time)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import quantity, identity, finish

c = 299792458.0
AU, pc = 1.495978707e11, 3.0856775814913673e16
Mpc = 1e6 * pc
quantity("c / (2 * pi * 150 Hz)", "3.18e5 m", rel_tol=5e-3)
rows = [("GW150914", 150.0, 410 * Mpc, [2.7e-6, 2.6e-17, 3.0e-33, 4.3e-59]),
        ("GW170817", 100.0, 40 * Mpc, [2.7e-6, 8.8e-17, 1.0e-32, 1.6e-55]),
        ("WD binary", 6.2e-3, 1e3 * pc, [2.7e-6, 3.7e-4, 4.2e-20, 4.2e-29])]
for name, f, d, lens in rows:
    lb = c / (2 * math.pi * f)
    vals = [2.7e-3 * (10 / (R / lb)) ** 3 for R in (100 * lb, AU, pc, d)]
    print(f"{name}: lambda/2pi = {lb:.3e} m; F = " + ", ".join(f"{v:.2g}" for v in vals) + "; lens " + ", ".join(f"{v:.2g}" for v in lens))
    for v, l in zip(vals, lens):
        identity(sp.Float(f"{v:.1e}"), sp.Float(f"{l:.1e}"))
tp = 410 * Mpc / c
print(f"t_prop(410 Mpc) = {tp:.3e} s; sigma*t_prop = {200 * tp:.3e}")
quantity("200 Hz * 410 Mpc / c", "8.4e18", rel_tol=0.01)
# limit: F -> its wR = 10 value at R = 10 lambda/2pi (consistency of the law)
identity(sp.Float(2.7e-3 * (10 / 10) ** 3), sp.Float(2.7e-3))
raise SystemExit(finish())
