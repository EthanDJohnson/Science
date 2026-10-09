"""M-EXAMINER-06: rocket equivalent of the MM proper-time ratio.

Rocket at Lorentz factor G through flat exterior over d: T_ext = d/v, tau = d/(G v) -> tau/T_ext = 1/G.
Matching MM's tau_MM / T_ext (d = l) = (pi r_e/c)/(l/c) = pi r_e / l -> G_eq = l/(pi r_e) = gam/pi.
KE = (G - 1) m c^2. Inputs quoted: r_e = 1.5e7 m, l = 3e3 ly. SI.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp

d, v, G, c, m = sp.symbols("d v G c m", positive=True)
identity((d / (G * v)) / (d / v), 1 / G)
# Newtonian limit of (G-1) m c^2 -> m v^2/2
limit(((1 / sp.sqrt(1 - v**2 / c**2) - 1) * m * c**2) / (m * v**2 / 2), "v", 0, 1)

ly = 9.4607304725808e15
re, l = 1.5e7, 3e3 * ly
Geq = l / (math.pi * re)
print("gam =", l / re, " G_eq =", Geq)
quantity(f"{Geq}", "6.023e11", rel_tol=1e-3)
quantity(f"({Geq} - 1) * 1 kg * c^2", "5.41e28 J", rel_tol=2e-3)
quantity(f"({Geq} - 1) * 70 kg * c^2", "3.79e30 J", rel_tol=2e-3)
units("1 kg * c^2", "J")
raise SystemExit(finish())
