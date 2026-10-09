"""M-ENGINEER-03: Ford-Roman band width (formula quoted, Q-21): a0 <~ (r0/(8 f^4 lP))^(1/3) lP, f = 0.01.
Checks the arithmetic, the r0^(1/3) scaling and the radii at which the band reaches 0.2 um and 1e-10 m.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

r0, f, lP = sp.symbols("r0 f lP", positive=True)
a0 = (r0 / (8 * f**4 * lP))**sp.Rational(1, 3) * lP
identity(sp.diff(sp.log(a0), r0) * r0, sp.Rational(1, 3))   # d ln a0/d ln r0 = 1/3
identity(a0, (r0 * lP**2)**sp.Rational(1, 3) / (2 * f**sp.Rational(4, 3)))
limit(a0 / r0, "r0", "oo", "0")   # band always thinner than the throat for large r0
units("(1 m/(8*0.01^4*l_P))^(1/3)*l_P", "length")

LP = math.sqrt(1.054571817e-34 * 6.67430e-11 / 299792458.0**3)
band = lambda r: (r / (8 * 0.01**4 * LP))**(1/3) * LP
for r in (1e-6, 0.1, 1.0, 1.5e7, 4.215e21):
    print(f"r0 = {r:g} m: band = {band(r):.3e} m, log10(1e-10 m/band) = {math.log10(1e-10/band(r)):.1f}")
quantity("(1 m/(8*0.01^4*l_P))^(1/3)*l_P", "1.5e-21 m", rel_tol=2e-2)
quantity("(1 um/(8*0.01^4*l_P))^(1/3)*l_P", "1.5e-23 m", rel_tol=2e-2)
quantity("(0.1 m/(8*0.01^4*l_P))^(1/3)*l_P", "6.9e-22 m", rel_tol=2e-2)
quantity("(1.5e7 m/(8*0.01^4*l_P))^(1/3)*l_P", "3.7e-19 m", rel_tol=2e-2)
# invert: r0 where band = X
inv = lambda X: (X / LP)**3 * 8 * 0.01**4 * LP
print(f"band = 0.2 um at r0 = {inv(2e-7):.3e} m; band = 1e-10 m at r0 = {inv(1e-10):.3e} m")
print(f"0.2 um radius / observable-universe radius 4.4e26 m: {math.log10(inv(2e-7)/4.4e26):.2f} orders")
quantity(f"{inv(2e-7)} m", "2.5e42 m", rel_tol=0.06)
quantity(f"{inv(1e-10)} m", "3e32 m", rel_tol=0.06)
raise SystemExit(finish())
