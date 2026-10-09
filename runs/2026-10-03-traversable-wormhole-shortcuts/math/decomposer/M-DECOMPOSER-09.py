"""M-DECOMPOSER-09: throat radius from the tidal criterion a ~ size * c^2 / r^2 < a_max (the scaling MM use, Q-01).
r_min = c * sqrt(size / a_max). Compare MM (20 g, 0.5 m), the lens's MT pairing (1 g, 2 m, L14), and the
dossier's Q-52 variant (1 g, 0.5 m)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

size, a, c = sp.symbols("size a c", positive=True)
r = sp.symbols("r", positive=True)
rmin = sp.solve(sp.Eq(size * c**2 / r**2, a), r)[0]
identity(rmin, c * sp.sqrt(size / a))
units("c * (0.5 m / (20 * 9.8 m/s^2))^0.5", "length")
quantity("c * (0.5 m / (20 * 9.8 m/s^2))^0.5", "1.5e7 m", rel_tol=2e-2)       # MM anchor reproduced
quantity("c * (0.5 m / (1 * 9.8 m/s^2))^0.5", "6.8e7 m", rel_tol=1e-2)        # Q-52: 1 g but 0.5 m body
r_mt = "c * (2 m / (1 * 9.8 m/s^2))^0.5"                                          # L14: 1 g over 2 m
quantity(r_mt, "1.354e8 m", rel_tol=2e-3)
print("ratio 1 g/2 m vs 20 g/0.5 m:", math.sqrt((2 / 1) / (0.5 / 20)), "; ratio 1 g/0.5 m vs 20 g/0.5 m:", math.sqrt(20))
# the lens's L14 factor "about 4.5" for 1 g over 2 m: test it (expected to fail; true factor sqrt(80) = 8.94)
quantity(f"{math.sqrt((2 / 1) / (0.5 / 20))}", "4.5", rel_tol=0.1)
raise SystemExit(finish())
