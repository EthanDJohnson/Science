"""M-EXAMINER-02: QGEM phase read as a proper-time difference of a rest-mass (Compton) clock.

Claim (findings 7, 13): Delta tau = hbar Delta phi / (m c^2) = 2.70e-38 s for Delta phi = 0.23 rad,
m = 1e-14 kg; 6.69e-38 s for 0.57 rad; fractional (per 1 s) 2.7e-38. SI units.

Independent derivation: a branch of rest mass m accrues phase phi = -m c^2 tau / hbar along its worldline
(action S = -m c^2 tau). Two branches with proper times differing by Delta tau differ in phase by
m c^2 Delta tau / hbar. Inverting gives the claim.
Consistency: in the Newtonian limit, the entangling phase for a pair at separation d over time T is
G m^2 T/(hbar d), and Delta tau = T * G m/(c^2 d): both sides give the same relation (checked symbolically).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

m, c, hbar, tau, G, T, d = sp.symbols("m c hbar tau G T d", positive=True)
phase = m * c**2 * tau / hbar
dphi = sp.symbols("dphi", positive=True)
dtau = sp.solve(sp.Eq(phase, dphi), tau)[0]
identity(dtau, hbar * dphi / (m * c**2))
# Newtonian consistency: phase from potential energy -G m^2/d over time T equals m c^2 (T G m/(c^2 d))/hbar
identity(G * m**2 * T / (hbar * d), m * c**2 * (T * G * m / (c**2 * d)) / hbar)

quantity("hbar * 0.23 / (1e-14 kg * c^2)", "2.70e-38 s", rel_tol=2e-3)
quantity("hbar * 0.57 / (1e-14 kg * c^2)", "6.69e-38 s", rel_tol=2e-3)
quantity("hbar * 0.23 / (1e-14 kg * c^2) / (1 s)", "2.7e-38", rel_tol=5e-3)
units("hbar * 0.23 / (1e-14 kg * c^2)", "time")

raise SystemExit(finish())
