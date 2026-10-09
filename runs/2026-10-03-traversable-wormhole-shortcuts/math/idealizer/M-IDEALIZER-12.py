"""M-IDEALIZER-12: number of quanta to carry rest energy m c^2 as quanta of wavelength ~ R.

Each quantum has energy ~ hbar c / R (reduced wavelength R), so N ~ m c^2 / (hbar c / R) = m c R / hbar.
Claim: 2.8e42 for m = 1 kg, R = 1 m.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

m, c, R, hbar = sp.symbols("m c R hbar", positive=True)
Nq = sp.simplify(m * c**2 / (hbar * c / R))
identity(Nq, m * c * R / hbar)
limit(Nq, "R", 0, 0)    # a vanishing throat admits no payload quanta of fitting wavelength
units("1 kg * c * 1 m / hbar", "dimensionless")
quantity("1 kg * c * 1 m / hbar", "2.84e42", rel_tol=0.01)
raise SystemExit(finish())
