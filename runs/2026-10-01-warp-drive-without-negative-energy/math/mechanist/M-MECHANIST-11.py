"""M-MECHANIST-11: ideal GW/photon-rocket mass fractions; superkick conversion; e^(-3L) vs e^(-L).

Fraction of initial mass radiated per leg: 1 - sqrt((1-b)/(1+b)) (own derivation, M-08); start + stop: 1 - (1-b)/(1+b).
Photon rocket in rapidity L: m_f/m_i = e^(-L) with tanh L = b.  Claim: 3.9 %, 7.7 %, 3.47e26 kg, 3.1e43 J (of 4.51e27 kg
initial), 15,000 km/s = 0.050 c, e^(-3L) = (e^(-L))^3 < e^(-L) for L > 0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, quantity, limit, finish

b, L = sp.symbols("b L", positive=True)
identity(sp.exp(-sp.atanh(b)), sp.sqrt((1 - b) / (1 + b)), domain={"b": (0.001, 0.99)})
inequality("exp(-3*L)", "<", "exp(-L)", domain={"L": (0.001, 5)})
limit("1 - sqrt((1-b)/(1+b))", "b", 0, "0")
f1 = 1 - (0.96 / 1.04) ** 0.5
f2 = 1 - 0.96 / 1.04
print(f"per leg {f1:.5f}; start+stop {f2:.5f}; mass {f2*4.5114e27:.4e} kg; energy {f2*4.5114e27*2.99792458e8**2:.4e} J")
quantity(f"{f1} m/m", "0.039 m/m", rel_tol=0.01)
quantity(f"{f2} m/m", "0.077 m/m", rel_tol=0.005)
quantity(f"{f2*4.5114e27} kg", "3.47e26 kg", rel_tol=0.003)
quantity(f"{f2*4.5114e27} kg * (2.99792458e8 m/s)^2", "3.1e43 J", rel_tol=0.01)
quantity("15000 km/s / (2.99792458e8 m/s)", "0.050", rel_tol=0.002)
raise SystemExit(finish())
