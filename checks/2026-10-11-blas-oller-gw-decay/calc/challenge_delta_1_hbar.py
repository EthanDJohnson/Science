#!/usr/bin/env python3
"""Challenge delta-1: an independent SI check of eqs. 8, 11 and 12 (exponents of hbar and c), and of the eq.19 overestimate at one point."""
import math
import sympy as sp

G, E, w, d, hb, c = sp.symbols("G E omega delta hbar c", positive=True)
x, y = sp.symbols("x y", real=True)
# SI base dimensions as (kg, m, s)
dim = {G: (-1, 3, -2), E: (1, 2, -2), w: (0, 0, -1), d: (0, 0, -1), hb: (1, 2, -1), c: (0, 1, -1)}
def dims(expo):
    return tuple(sum(expo[k] * dim[k][i] for k in expo) for i in range(3))
# natural-units eq.11: G^2 E^2 w^2 sig^2 with w_s = hbar omega, sig = hbar delta, G_nat = G/(hbar c^5): exponent of hbar, c for power [kg m^2 s^-3]
sol = sp.solve([sp.Eq(a, b) for a, b in zip(dims({G: 2, E: 2, w: 2, d: 2, hb: x, c: y}), (1, 2, -3))], [x, y])
print(f"eq.11  G^2 E^2 w^2 delta^2 hbar^x c^y = power  ->  {sol}   (B&O: hbar^1 c^-10)")
sol8 = sp.solve([sp.Eq(a, b) for a, b in zip(dims({G: 2, E: 2, w: 1, d: 2, hb: x, c: y}), (0, 0, -1))], [x, y])
print(f"eq.8   G^2 E^2 w delta^2 hbar^x c^y = 1/time   ->  {sol8}   (hbar-free photon-pair rate)")
solP = sp.solve([sp.Eq(a, b) for a, b in zip(dims({G: 2, E: 2, w: 1, d: 1, hb: x, c: y}), (0, 0, 0))], [x, y])
print(f"P_tot  G^2 E^2 w delta hbar^x c^y = number      ->  {solP}")
dt = sp.symbols("dt", positive=True)
eq12 = sp.Rational(3, 50) / sp.pi * (2 * G * E / c**4 / (c * dt))**2 * hb * w**2
eq11 = 6 * G**2 * hb / (25 * sp.pi * c**10) * E**2 * w**2 * d**2
print(f"eq.12/eq.11 = {sp.simplify(eq12/eq11)}  (=1 iff dt = 1/delta)")
# eq.19 factor at w_s = 1e-10 eV, eps = 0.1, z = 0
hbar = 6.582119569e-16; H0 = 67.4e3 / 3.0857e22
sig = 0.1 * 1e-10 / hbar
print(f"3 sig/(4 pi H0) at w_s = 1e-10 eV, eps = 0.1: {3*sig/(4*math.pi*H0):.3e}")
