"""M-IDEALIZER-08: minimisation of the MMP-type energy E(ell) = r_e^3/(G ell^2) - N q/(8 ell)  (hbar = c = 1).

Inputs (taken from the lens, quoted from MMP; N multiplying the Casimir term is the lens's assumption):
  r_e > 0 mouth radius, ell > 0 throat length, G > 0, N q > 0.
Claim: ell* = 16 r_e^3/(G N q); E_min = -G N^2 q^2/(256 r_e^3); |E_min|/(r_e/G) = (r_e/ell*)^2.
Numbers: gamma = ell/r_e = 2e12, M_e = r_e c^2/G with r_e = 1.5e7 m: 2.02e34 kg; |E|/M = 2.5e-25; |E| = 5.05e9 kg.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, quantity, units, finish

re, ell, G, N, q = sp.symbols("r_e ell G N q", positive=True)
E = re**3 / (G * ell**2) - N * q / (8 * ell)
crit = sp.solve(sp.diff(E, ell), ell)
print("critical points:", crit)
lstar = crit[0]
identity(lstar, 16 * re**3 / (G * N * q))
sign(sp.diff(E, ell, 2).subs(ell, lstar), "positive")        # a minimum
Emin = sp.simplify(E.subs(ell, lstar))
identity(Emin, -G * N**2 * q**2 / (256 * re**3))
identity(sp.Abs(Emin) / (re / G), (re / lstar)**2)
# limits: no Casimir term (N q -> 0) -> ell* -> oo and E_min -> 0 (no static throat)
limit(Emin, "q", 0, 0)
limit(lstar, "q", 0, sp.oo)
# units (SI form): r_e^3 c^4/(G ell^2) and N q hbar c/(8 ell) are energies
units("(1 m)^3 * c^4 / (G * (1 m)^2)", "energy")
units("hbar * c / (1 m)", "energy")
# numbers
quantity("1.5e7 m * c^2 / G", "2.02e34 kg", rel_tol=2e-3)
frac = (1 / 2e12)**2
print("(r_e/ell)^2 =", frac)
quantity(f"{frac} * 1.5e7 m * c^2 / G", "5.05e9 kg", rel_tol=3e-3)
raise SystemExit(finish())
