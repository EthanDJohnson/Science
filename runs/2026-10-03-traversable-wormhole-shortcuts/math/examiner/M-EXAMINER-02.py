"""M-EXAMINER-02: Ellis (Ellis-Bronnikov, Phi = 0) transit.

Metric (independent, standard): ds^2 = -c^2 dt^2 + dl^2 + (l^2 + b0^2) dOmega^2, r(l) = sqrt(l^2 + b0^2).
Static observers at areal radius r_obs on each side: l = +/- sqrt(r_obs^2 - b0^2).
Radial null ray: c dt = dl  ->  T_thru = 2 sqrt(r_obs^2 - b0^2)/c (static clocks = coordinate clocks, Phi = 0).
Payload at constant local speed v: tau = L_proper sqrt(1 - v^2/c^2)/v.
Exterior: mouths separated by D (centre to centre), observers on facing sides, flat exterior
-> T_ext = (D - 2 r_obs)/c (the lens's convention; reproduces its 1 km ratio).
SI units.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp

l, b0, r = sp.symbols("l b0 r", positive=True)
# Null radial transit from areal radius: integral of dl from -L to L where r(L) = r_obs
L = sp.sqrt(r**2 - b0**2)
identity(sp.integrate(1, (l, -L, L)), 2 * sp.sqrt(r**2 - b0**2), domain={"r": (1.01, 100), "b0": (0.1, 1)})
# Limit: b0 -> 0 recovers flat space through the origin (2 r_obs)
limit("2*sqrt(r**2 - b0**2)", "b0", 0, "2*r")

c = 299792458.0
b, ro = 1.0, 10.0
T = 2 * math.sqrt(ro**2 - b**2) / c
print("T_thru (b0=1 m, r_obs=10 m) =", T, "s")
quantity(f"{2*math.sqrt(ro**2-b**2)} m / c", "6.6378e-8 s", rel_tol=1e-4)
AU, ly = 1.495978707e11, 9.4607304725808e15
for D, lens in [(1e3, 2.031e-2), (AU, 1.330e-10), (ly, 2.103e-15)]:
    ratio = T / ((D - 2 * ro) / c)
    print(f"D={D:.4g} m ratio={ratio:.4g} (lens {lens})")
    identity(f"{ratio:.4g}", f"{lens}")
# r_obs = 100 m
T100 = 2 * math.sqrt(100.0**2 - 1) / c
for D, lens in [(1e3, 2.500e-1), (AU, 1.337e-9), (ly, 2.114e-14)]:
    ratio = T100 / ((D - 200.0) / c)
    print(f"r_obs=100 m D={D:.4g} m ratio={ratio:.4g} (lens {lens})")
    identity(f"{ratio:.4g}", f"{lens}")
quantity(f"{(1e3-20)} m / c", "3.27e-6 s", rel_tol=2e-3)
# tau at 0.1c local speed
v = 0.1
tau = 2 * math.sqrt(ro**2 - b**2) * math.sqrt(1 - v**2) / (v * c)
print("tau at 0.1c =", tau, "s")
quantity(f"{tau} s", "6.60e-7 s", rel_tol=2e-3)
units("19.9 m / (0.1 * c)", "s")
raise SystemExit(finish())
