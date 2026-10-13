"""M-EXAMINER-08 (SI): strong-field scales. GW150914: M = 65 Msun, f_GW = 150 Hz, sigma = 200 rad/s.
lambda/2pi = c/(2 pi f); r_g = G M/c^2; Kepler separation a = (G M / Om^2)^(1/3) with Om = pi f_GW (orbital angular
frequency = half the GW angular frequency); v = Om a. GW170817: M = 2.74 Msun, f_GW = 100 Hz.
Limit check: v/c = (G M Om / c^3)^(1/3) (Newtonian), identical algebraically."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import quantity, identity, finish

G, c, Msun = 6.67430e-11, 299792458.0, 1.98840987e30
for name, M, f, sig, lens in (("GW150914", 65, 150.0, 200.0, (3.3, 15.6, 3.4e5, 0.53)),
                              ("GW170817", 2.74, 100.0, None, None)):
    GM = G * M * Msun
    rg = GM / c ** 2
    lb = c / (2 * math.pi * f)
    Om = math.pi * f
    a = (GM / Om ** 2) ** (1 / 3)
    v = Om * a / c
    print(f"{name}: r_g = {rg:.3e} m; lambda/2pi = {lb:.3e} m = {lb/rg:.2f} r_g; a = {a:.3e} m; v/c = {v:.3f};"
          f" lambda/2pi / a = {lb/a:.2f}" + (f"; c/sigma = {c/sig:.3e} m = {c/sig/rg:.1f} r_g" if sig else ""))
    identity(sp.Float(v), sp.Float((GM * Om / c ** 3) ** (1 / 3)))
    if lens:
        for got, want in ((lb / rg, 3.3), (c / sig / rg, 15.6), (a, 3.4e5), (v, 0.53)):
            identity(sp.Float(f"{got:.2g}"), sp.Float(f"{want:.2g}"))
    else:
        identity(sp.Float(f"{lb/a:.2g}"), sp.Float("3.1"))
        identity(sp.Float(f"{v:.2g}"), sp.Float("0.16"))
quantity("G * 65 Msun / c^2", "9.6e4 m", rel_tol=0.01)
raise SystemExit(finish())
