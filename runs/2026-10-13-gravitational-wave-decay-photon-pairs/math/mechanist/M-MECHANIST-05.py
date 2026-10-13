"""M-MECHANIST-05: B&O eq. 8 in SI and the GW150914-point numbers.
Natural units: dP/dt = 3 G^2 N^2 w^3 sigma^2/(25 pi), N = E/(hbar w), G -> hbar G/c^5 (time^2).
SI form claimed: 3 G^2 E^2 w sigma^2/(25 pi c^10). Inputs (B&O): E = 2 Msun c^2, f = 150 Hz, sigma_w = 200 rad/s.
Claims: 1.4e-4 pairs/s; T_eff = 4 pi/(3 sigma) = 0.021 s; total 2.9e-6; 410 Mpc -> 4.2e16 s -> 5.9e12 pairs;
energy fraction 3.3e-66 (pair energy 2 hbar w); 1/(dP/dt) = 7.2e3 s; sigma/w = 0.21; c_tot = 4/25 <-> 3/(25 pi).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

G, hbar, c, E, w, sig = sp.symbols("G hbar c E w sigma", positive=True)
Nn = E / (hbar * w)
nat = 3 * (hbar * G / c**5) ** 2 * Nn**2 * w**3 * sig**2 / (25 * sp.pi)
identity(nat, 3 * G**2 * E**2 * w * sig**2 / (25 * sp.pi * c**10))      # hbar cancels
units("(6.674e-11 m^3/(kg*s^2))^2 * (1 J)^2 * (1 /s) * (1 /s)^2 / (1 m/s)^10", "1/s")
# per-packet total with c_tot = 4/25 divided by T_eff = 4 pi/(3 sigma) gives 3/(25 pi)
identity(sp.Rational(4, 25) / (4 * sp.pi / 3), 3 / (25 * sp.pi))
rate = "3*G^2*(2*Msun*c^2)^2*(2*pi*150 /s)*(200 /s)^2/(25*pi*c^10)"
quantity(rate, "1.398e-4 /s", rel_tol=3e-3)
quantity("4*pi/(3*200) s", "0.0209 s", rel_tol=3e-3)
quantity(f"({rate}) * 4*pi/(3*200) s", "2.928e-6", rel_tol=3e-3)
quantity("410 Mpc / c", "4.220e16 s", rel_tol=3e-3)
quantity(f"({rate}) * 410 Mpc / c", "5.90e12", rel_tol=3e-3)
quantity(f"({rate}) * 410 Mpc / c * 2*hbar*2*pi*150 /s / (2*Msun*c^2)", "3.28e-66", rel_tol=3e-3)
quantity(f"1/({rate})", "7.15e3 s", rel_tol=3e-3)
quantity("200/(2*pi*150)", "0.212", rel_tol=3e-3)
raise SystemExit(finish())
