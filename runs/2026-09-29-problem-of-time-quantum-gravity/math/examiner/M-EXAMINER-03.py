"""M-EXAMINER-03: fractional time dilation sourced by a small mass, G m / (c^2 d), and the gap to clock precision.

Claim (finding 7, Calculations item 3), SI:
  G m/(c^2 d) = 3.71e-38 (m = 1e-14 kg, d = 200 um), 1.65e-38 (d = 450 um);
  gap to 7.6e-21 fractional clock precision: 2.0e17 and 4.6e17;
  1 g at 1 mm: 7.4e-28; 1 kg at 1 cm: 7.4e-26.
Derivation: weak field, dtau/dt = 1 - G m/(r c^2) + O(c^-4), so the fractional rate shift at distance d is Gm/(c^2 d).
Limit: Schwarzschild exact sqrt(1 - 2Gm/(r c^2)) reduces to this at large r.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import series, quantity, units, finish

u = sp.symbols("u", positive=True)  # u = G m/(r c^2)
series(sp.sqrt(1 - 2 * u), "u", 0, 2, 1 - u)

quantity("G * 1e-14 kg / (c^2 * 200 um)", "3.71e-38", rel_tol=2e-3)
quantity("G * 1e-14 kg / (c^2 * 450 um)", "1.65e-38", rel_tol=3e-3)
quantity("7.6e-21 / (G * 1e-14 kg / (c^2 * 200 um))", "2.0e17", rel_tol=2.5e-2)  # stated to 2 significant figures
quantity("7.6e-21 / (G * 1e-14 kg / (c^2 * 450 um))", "4.6e17", rel_tol=1e-2)
quantity("G * 1 g / (c^2 * 1 mm)", "7.4e-28", rel_tol=5e-3)
quantity("G * 1 kg / (c^2 * 1 cm)", "7.4e-26", rel_tol=5e-3)
units("G * 1e-14 kg / (c^2 * 200 um)", "dimensionless")

raise SystemExit(finish())
