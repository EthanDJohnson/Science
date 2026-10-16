#!/usr/bin/env python3
"""M-SIMULATOR-02: the thrust-to-weight ceiling, the horizontal acceleration ceiling, the tilt.

CLAIM (lens findings 1 and 2, verification rows "known limit"): for m = 0.75 kg and four
rotors each limited to 8.5 N, T/W = 4.6227; the maximum horizontal acceleration at constant
altitude is a_h = g sqrt((T/W)^2 - 1) = 44.260 m/s^2, reached at a tilt
theta = acos(1/(T/W)) = 77.51 deg with zero vertical residual.

SYMBOLS / DOMAIN. m > 0 kg vehicle mass; T > 0 N total available thrust along the body z
axis; W = m g N weight; r = T/W > 1 (dimensionless, must exceed 1 for level flight);
theta in [0, pi/2) rad tilt of the thrust axis from vertical; g = 9.80665 m/s^2.

INDEPENDENT DERIVATION. Rigid body, thrust along body z, no aerodynamic force (the ceiling is
defined on the thrust-limited vehicle). Level flight requires T cos(theta) = m g, so
cos(theta) = 1/r. The horizontal component is a_x = (T/m) sin(theta) = g r sqrt(1 - 1/r^2)
= g sqrt(r^2 - 1). Both the maximisation and the vertical-residual statement follow.
"""
import sys
from math import acos, degrees, sqrt

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

G = 9.80665
MASS = 0.75
T_TOTAL = 4 * 8.5
W = MASS * G
r = T_TOTAL / W
a_h = G * sqrt(r**2 - 1)
theta = acos(1 / r)
a_x_sim = (T_TOTAL / MASS) * sqrt(1 - (1 / r) ** 2)
a_z_res = (T_TOTAL / MASS) * (1 / r) - G

print("=== inputs (SI) ===")
print(f"m = {MASS} kg, T = {T_TOTAL} N, g = {G} m/s^2, W = {W:.6f} N")
print("\n=== derived ===")
print(f"T/W = {r:.6f} (dimensionless)")
print(f"a_h = g sqrt((T/W)^2 - 1) = {a_h:.6f} m/s^2")
print(f"a_h by the direct route (T/m) sin(theta) = {a_x_sim:.6f} m/s^2")
print(f"tilt = acos(1/(T/W)) = {degrees(theta):.4f} deg")
print(f"vertical residual at that tilt = {a_z_res:.3e} m/s^2")
print(f"also a_h = sqrt((T/m)^2 - g^2) = {sqrt((T_TOTAL/MASS)**2 - G**2):.6f} m/s^2")

print("\n=== checks ===")
quantity(f"{r:.6f}", "4.6227", rel_tol=1e-4)
quantity(f"{a_h:.6f} m/s^2", "44.260 m/s^2", rel_tol=1e-4)
quantity(f"{degrees(theta):.4f}", "77.51", rel_tol=1e-3)          # degrees, compared as a number
quantity(f"{a_x_sim:.6f} m/s^2", f"{a_h:.6f} m/s^2", rel_tol=1e-12)
inequality(f"{abs(a_z_res):.3e}", "<", "1e-12")                   # vertical residual, m/s^2
# the two algebraic forms of the ceiling agree for every r > 1
identity("g*sqrt(r**2 - 1)", "g*r*sqrt(1 - 1/r**2)", domain={"r": (1.0, 50.0), "g": (1.0, 20.0)})
identity("sqrt((g*r)**2 - g**2)", "g*sqrt(r**2 - 1)", domain={"r": (1.0, 50.0), "g": (1.0, 20.0)})
# limit: as T/W -> 1 the horizontal ceiling vanishes (all thrust holds altitude)
limit("g*sqrt(r**2 - 1)", "r", 1, "0", domain={"r": (1.0, 50.0), "g": (1.0, 20.0)})
# high-thrust limit: a_h -> g r = T/m
limit("g*sqrt(r**2 - 1)/(g*r)", "r", "oo", "1", domain={"r": (1.0, 1e6), "g": (1.0, 20.0)})
# the ceiling is below the total specific thrust and above zero
inequality("g*sqrt(r**2 - 1)", "<", "g*r", domain={"r": (1.0001, 50.0), "g": (1.0, 20.0)})
units("9.80665 m/s^2 * (4.6227^2 - 1)^(1/2)", "acceleration")
units("(4 * 8.5 N) / (0.75 kg * 9.80665 m/s^2)", "dimensionless")
raise SystemExit(finish())
