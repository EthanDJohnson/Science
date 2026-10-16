#!/usr/bin/env python3
"""M-EXAMINER-03  (examiner F3, brief hidden premise 4)

CLAIM, stated precisely
-----------------------
A quadrotor of mass m with maximum total thrust T_max = TWR * m * g (TWR > 1 dimensionless) flies
level (no vertical acceleration).  Then
 (i)   the maximum horizontal acceleration is a_h = g * sqrt(TWR^2 - 1);
       a_h = 39.0-43.0 m/s^2 for TWR = 4.1-4.5 with g = 9.81 m/s^2;
 (ii)  a rest-to-rest bang-bang translation over distance d = 10.7 m (75 m lap / 7 gates) at
       |acceleration| = a_h gives mean speed v_mean = sqrt(a_h * d)/2 and peak sqrt(a_h * d):
       10.21-10.73 m/s mean and 20.4-21.5 m/s peak;
 (iii) d ln a_h / d ln TWR = TWR^2/(TWR^2 - 1) = 1.063 at TWR = 4.1;
 (iv)  d ln v_mean / d ln a_h = 1/2 exactly, so d ln v_mean / d ln TWR = 0.532, which is within
       6 per cent of a published planner sweep's 0.565.

Domain: TWR > 1, d > 0, g > 0.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

twr = sp.Symbol("twr", positive=True)
gg, d, t = sp.symbols("gg d t", positive=True)

# (i) my derivation: thrust vector magnitude T = TWR*m*g; vertical component must equal m*g,
# the remainder is horizontal:  (TWR*g)^2 = g^2 + a_h^2.
a_h = sp.sqrt((twr * gg) ** 2 - gg ** 2)
identity(a_h, gg * sp.sqrt(twr**2 - 1), domain={"twr": (1.0001, 20.0), "gg": (1.0, 20.0)})
limit(a_h / (twr * gg), "twr", sp.oo, sp.Integer(1))          # large TWR: all thrust horizontal
identity(a_h.subs(twr, sp.sqrt(2)), gg, domain={"gg": (1.0, 20.0)})  # TWR = sqrt(2) -> a_h = g

# (ii) bang-bang: accelerate a for t/2, decelerate for t/2.
# d = 2 * (a/2) * (t/2)^2 = a t^2 / 4  ->  t = 2 sqrt(d/a); v_mean = d/t; v_peak = a t / 2.
a = sp.Symbol("a", positive=True)
t_tot = sp.solve(sp.Eq(a * t**2 / 4, d), t)[0]
v_mean = sp.simplify(d / t_tot)
v_peak = sp.simplify(a * t_tot / 2)
print("t_tot =", t_tot, " v_mean =", v_mean, " v_peak =", v_peak)
identity(v_mean, sp.sqrt(a * d) / 2, domain={"a": (0.1, 100.0), "d": (0.1, 100.0)})
identity(v_peak, sp.sqrt(a * d), domain={"a": (0.1, 100.0), "d": (0.1, 100.0)})
identity(v_peak / v_mean, sp.Integer(2), domain={"a": (0.1, 100.0), "d": (0.1, 100.0)})

# (iii)-(iv) elasticities, closed form
e_a_twr = sp.simplify(twr / a_h * sp.diff(a_h, twr))
identity(e_a_twr, twr**2 / (twr**2 - 1), domain={"twr": (1.0001, 20.0), "gg": (1.0, 20.0)})
e_v_a = sp.simplify(a / v_mean * sp.diff(v_mean, a))
identity(e_v_a, sp.Rational(1, 2), domain={"a": (0.1, 100.0), "d": (0.1, 100.0)})
limit(e_a_twr, "twr", sp.oo, sp.Integer(1))                   # elasticity -> 1 at large TWR

print("\nnumbers (g = 9.81 m/s^2, d = 10.7 m):")
g = 9.81
for TWR, a_want, vm_want, vp_want in ((4.1, 39.0, 10.21, 20.4), (4.5, 43.0, 10.73, 21.5)):
    ah = g * (TWR**2 - 1) ** 0.5
    vm = (ah * 10.7) ** 0.5 / 2
    vp = (ah * 10.7) ** 0.5
    print(f"  TWR {TWR}: a_h = {ah:.2f} m/s^2, v_mean = {vm:.3f} m/s, v_peak = {vp:.2f} m/s "
          f"(claimed {a_want}, {vm_want}, {vp_want})")
    quantity(f"{ah:.5f} m/s^2", f"{a_want} m/s^2", rel_tol=3e-3)
    quantity(f"{vm:.5f} m/s", f"{vm_want} m/s", rel_tol=3e-3)
    quantity(f"{vp:.5f} m/s", f"{vp_want} m/s", rel_tol=5e-3)

el = float(e_a_twr.subs(twr, sp.Rational(41, 10)))
print(f"\nd ln a_h/d ln TWR at 4.1 = {el:.6f} (claimed 1.063)")
print(f"d ln v/d ln TWR = {0.5 * el:.6f} (claimed 0.532)")
print(f"gap to published sweep 0.565: {abs(0.5 * el - 0.565) / 0.565:.2%} (claimed within 6 per cent)")
identity(f"{el:.4f}", "1.0633")
identity(f"{0.5 * el:.4f}", "0.5316")

units("9.81 m/s^2 * 3.9762", "m/s^2")
units("39.02 m/s^2 * 10.7 m", "m^2/s^2")

raise SystemExit(finish())
