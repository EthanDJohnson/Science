"""M-EXAMINER-07: MM payload back-reaction arithmetic.

Payload rest energy over |E_bin|, with E_bin ~ -5e9 kg c^2 (quoted Q-02, ~ -4.5e26 J);
locally boosted energy at the throat centre = gam m c^2, gam = l / r_e (Killing energy m c^2 at rest
outside; local static observer at the centre has lapse 1/gam relative to the exterior -> E_loc = gam E).
SI.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp

E, N = sp.symbols("E N", positive=True)   # Killing energy and lapse ratio (gam)
# local energy measured by static observer = E / lapse; lapse at centre relative to exterior = 1/gam
identity(E / (1 / N), N * E)
limit(N * E, "N", 1, E)   # no redshift -> local = conserved

ly = 9.4607304725808e15
gam = 3e3 * ly / 1.5e7
quantity("5e9 kg * c^2", "4.5e26 J", rel_tol=1e-2)
quantity("1 kg * c^2 / (5e9 kg * c^2)", "2.0e-10", rel_tol=1e-3)
quantity("70 kg * c^2 / (5e9 kg * c^2)", "1.4e-8", rel_tol=1e-3)
quantity(f"{gam} * 1 kg * c^2", "1.70e29 J", rel_tol=2e-3)
quantity(f"{gam} * 70 kg * c^2", "1.19e31 J", rel_tol=2e-3)
units("70 kg * c^2", "J")
raise SystemExit(finish())
