"""M-EXAMINER-07: Smith-Ahmadi gravitational clock-system coupling lam E = G E/(c^4 x).

Claim (finding 10, hardest question 1), SI: lam = G/(c^4 x) (units 1/energy), lam E at x = 1 mm:
  2.35e-60 for an optical photon energy (hbar * 2 pi * 429 THz), 1.07e-49 for Sr-87 rest energy,
  7.43e-28 for a 1 g rest energy; lam E ~ 1 at Planck energy and Planck length.
Independent derivation: Newtonian interaction -G m_C m_S / x with m = H/c^2 gives
  H_CS = -G H_C H_S/(c^4 x) = -lam H_C H_S. For a rest energy, lam m c^2 = G m/(c^2 x) (the redshift factor).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

G, c, x, EC, ES, m, hbar = sp.symbols("G c x E_C E_S m hbar", positive=True)
identity(-G * (EC / c**2) * (ES / c**2) / x, -(G / (c**4 * x)) * EC * ES)
identity((G / (c**4 * x)) * m * c**2, G * m / (c**2 * x))
# Planck scale: E_P = sqrt(hbar c^5/G), l_P = sqrt(hbar G/c^3) -> lam E = 1
identity(G * sp.sqrt(hbar * c**5 / G) / (c**4 * sp.sqrt(hbar * G / c**3)), 1)

quantity("G * hbar * 2*pi*429 THz / (c^4 * 1 mm)", "2.35e-60", rel_tol=3e-3)
quantity("G * 86.9088775 Da * c^2 / (c^4 * 1 mm)", "1.07e-49", rel_tol=3e-3)
quantity("G * 1 g * c^2 / (c^4 * 1 mm)", "7.43e-28", rel_tol=2e-3)
quantity("G * m_P * c^2 / (c^4 * l_P)", "1", rel_tol=1e-6)
units("G / (c^4 * 1 mm)", "1/J")
units("G * hbar * 2*pi*429 THz / (c^4 * 1 mm)", "dimensionless")

raise SystemExit(finish())
