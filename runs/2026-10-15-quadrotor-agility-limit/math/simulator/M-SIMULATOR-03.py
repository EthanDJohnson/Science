#!/usr/bin/env python3
"""M-SIMULATOR-03: the smooth reference family's feasible speed and its time penalty.

CLAIM (lens findings 5 and 11, and candidate SIMULATOR-E): for the reference family that
traverses the slalom at constant x-speed U, the lateral acceleration demand is A k^2 U^2 with
A = 3 m and k = 2 pi/30 m^-1; it equals the horizontal ceiling a_h = 44.260 m/s^2 at
U_feas = 18.339 m/s; and at that ceiling the family's traversal time exceeds the point-mass
time optimum t_opt = 4.5020 s by 9.01 per cent.

SYMBOLS / DOMAIN. U > 0 m/s constant x-component of velocity; A > 0 m amplitude;
k > 0 m^-1 spatial angular frequency; a_h > 0 m/s^2; t = 90 m / U the traversal time;
all motion at constant altitude.

INDEPENDENT DERIVATION. With x(t) = U t and y = A sin(k x), the acceleration vector is
(0, -A k^2 U^2 sin(k U t)), whose magnitude peaks at A k^2 U^2 (at the crests, where the
tangential term vanishes because speed |v| = U sqrt(1 + y'^2) is extremal). Hence
U_feas = sqrt(a_h/(A k^2)) and the penalty is (90/U_feas)/t_opt - 1.
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity, units  # noqa: E402

G = 9.80665
A_H = np.sqrt((4 * 8.5 / 0.75) ** 2 - G**2)
AMP, LAM, XEND = 3.0, 30.0, 90.0
K = 2 * np.pi / LAM
T_OPT = 4.5020          # s, the lens's denominator (checked independently in M-SIMULATOR-01)
S_PATH = 98.315         # m

print("=== inputs (SI) ===")
print(f"A = {AMP} m, k = 2 pi/{LAM} = {K:.6f} 1/m, a_h = {A_H:.5f} m/s^2, t_opt = {T_OPT} s")

demand_coeff = AMP * K**2
U_feas = np.sqrt(A_H / demand_coeff)
print("\n=== derived ===")
print(f"A k^2 = {demand_coeff:.6f} 1/m  (lateral accel per (m/s)^2)")
print(f"U_feas = sqrt(a_h/(A k^2)) = {U_feas:.4f} m/s")

# brute-force maximum of |a| over one period at U_feas, to confirm the peak demand formula
t = np.linspace(0, LAM / U_feas, 200001)
ax = np.zeros_like(t)
ay = -AMP * K**2 * U_feas**2 * np.sin(K * U_feas * t)
amax = np.max(np.hypot(ax, ay))
print(f"max |a| over a period at U_feas, by sampling: {amax:.5f} m/s^2 (a_h = {A_H:.5f})")

t_feas = XEND / U_feas
penalty = t_feas / T_OPT - 1
mean_path_speed = S_PATH / t_feas
print(f"t at U_feas = 90/U = {t_feas:.5f} s; t/t_opt = {t_feas/T_OPT:.5f} -> penalty {100*penalty:.3f} per cent")
print(f"mean path speed there = {mean_path_speed:.4f} m/s = {S_PATH/XEND:.5f} x U")
print(f"path/x ratio S/90 = {S_PATH/XEND:.5f}")
print("\n=== cross-checks on the lens's reported operating points ===")
for label, U in (("U* at 0.50 m tol", 18.05), ("U* at 0.20 m tol", 14.875)):
    print(f"  {label}: U = {U} m/s -> demand {demand_coeff*U**2:.3f} m/s^2 "
          f"({100*demand_coeff*U**2/A_H:.1f} per cent of a_h), 90/U = {XEND/U:.3f} s")

print("\n=== checks ===")
quantity(f"{U_feas:.5f} m/s", "18.3394 m/s", rel_tol=1e-4)
quantity(f"{amax:.5f} m/s^2", f"{A_H:.5f} m/s^2", rel_tol=1e-6)
quantity(f"{100*penalty:.4f}", "9.01", rel_tol=2e-3)
quantity(f"{mean_path_speed:.4f} m/s", "20.028 m/s", rel_tol=1e-3)
# the demand formula, symbolically: |d^2/dt^2 (A sin(k U t))| peaks at A k^2 U^2
identity("A*k**2*U**2*sin(k*U*t)", "-diff(A*sin(k*U*t), t, 2)")
# U_feas inverts the demand
identity("A*k**2*(sqrt(a/(A*k**2)))**2", "a")
# small-amplitude limit: a flat course imposes no speed limit from curvature
identity("sqrt(a/(A*k**2))", "sqrt(a)/(k*sqrt(A))")
units("(44.26 m/s^2 / (3 m * (0.20944 m^-1)^2))^(1/2)", "speed")
units("3 m * (0.20944 m^-1)^2 * (18.34 m/s)^2", "acceleration")
raise SystemExit(finish())
