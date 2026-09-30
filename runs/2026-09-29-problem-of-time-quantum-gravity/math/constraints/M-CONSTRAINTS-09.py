"""M-CONSTRAINTS-09: Tolman ratio, Unruh temperature, modular-to-proper-time factor, Hawking temperature (SI).

Tolman: T sqrt(-g_tt) = const in Schwarzschild, g_tt = -(1 - 2GM/(rc^2)).
  T(R+h)/T(R) - 1 = sqrt((1 - rs/R)/(1 - rs/(R+h))) - 1 ~ -GMh/(R^2 c^2), claim -1.0927e-19 for h = 1 mm at Earth.
Unruh: T_U = hbar a/(2 pi c kB), claim 3.98e-20 K at a = g.
Bisognano-Wichmann: modular parameter s <-> boost rapidity 2 pi s; proper time tau = (c/a) * rapidity => dtau/ds = 2 pi c/a,
  claim 1.92e8 s at a = g.
Hawking: T_H = hbar c^3/(8 pi G M kB), claim 6.17e-8 K for 1 Msun; horizon 2GM/c^2 = 2953.25 m; kappa = 1/(4M) = 1.6930e-4 1/m.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
import sympy as sp
from gr_tensors import horizons_1p1
from math_checks import series, quantity, units, finish

mp.mp.dps = 50
G = mp.mpf("6.67430e-11"); c = mp.mpf(299792458); GM = mp.mpf("3.986004418e14"); R = mp.mpf("6.371e6")
rs = 2 * GM / c**2
h = mp.mpf("1e-3")
ratio = mp.sqrt((1 - rs / R) / (1 - rs / (R + h))) - 1
print("Tolman ratio - 1 (50 digits):", mp.nstr(ratio, 8), " float64:", (1 - 2*3.986004418e14/299792458.0**2/6.371e6)**0.5/(1 - 2*3.986004418e14/299792458.0**2/(6.371e6+1e-3))**0.5 - 1)
quantity(f"{float(-ratio)}", "1.0927e-19", rel_tol=5e-4)
quantity("GM_E_over_R2 * 1 mm / c^2".replace("GM_E_over_R2", "(3.986004418e14 m^3/s^2)/(6.371e6 m)^2"), "1.0927e-19", rel_tol=5e-4)
# weak-field series: sqrt((1-u)/(1-v)) with u = rs/R, v = rs/(R+h): leading term -(u - v)/2
u, v = sp.symbols("u v", positive=True)
series(sp.sqrt((1 - v * u) / (1 - u)), "u", 0, 2, "1 + u*(1 - v)/2")   # v = R/(R+h) scaling check
quantity("hbar * 9.80665 m/s^2 / (2*pi*c*kB)", "3.98e-20 K", rel_tol=3e-3)
units("hbar * 9.80665 m/s^2 / (2*pi*c*kB)", "K")
quantity("2*pi*c/(9.80665 m/s^2)", "1.92e8 s", rel_tol=3e-3)
quantity("hbar * c^3 / (8*pi*G*Msun*kB)", "6.17e-8 K", rel_tol=3e-3)
quantity("2*G*Msun/c^2", "2953.25 m", rel_tol=1e-5)
quantity("c^2/(4*G*Msun)", "1.6930e-4 1/m", rel_tol=1e-4)
# kappa -> T: T = hbar c kappa/(2 pi kB), consistency with T_H
quantity("hbar*c*(1.6930e-4 1/m)/(2*pi*kB)", "6.17e-8 K", rel_tol=3e-3)
# Independent horizon check with the toolkit, PG river u = -sqrt(2M/r), M = GMsun/c^2 in metres
import numpy as np
M = 1.32712440018e20 / 299792458.0**2
xs = np.linspace(1000.0, 6000.0, 20001)
hz = horizons_1p1(lambda x: -np.sqrt(2 * M / x), xs)
print("horizons_1p1:", hz)
raise SystemExit(finish())
