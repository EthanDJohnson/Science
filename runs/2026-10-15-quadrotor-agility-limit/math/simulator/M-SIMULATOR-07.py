#!/usr/bin/env python3
"""M-SIMULATOR-07: the elasticity table and the comparisons drawn from it.

CLAIM (lens findings 6, 7, 8 and candidates A, B, D): the reported elasticities are the arc
elasticities e = ln(v2/v1)/ln(x2/x1) of the reported speed pairs, and the comparisons made
from them hold: thrust-to-weight +0.527 reproduces the hardware +0.565 "to within 7 per
cent"; the four seen-course elasticities (+0.527, -0.462, +0.381, -0.132) have a largest/
smallest ratio under four and the two biggest within 15 per cent; the range elasticity
(+0.986, +1.082) is "2 to 10 times every rival"; |e_range/e_latency| = 9.4.

SYMBOLS / DOMAIN. v > 0 m/s mean path speed (or dodge speed); x > 0 the perturbed limit in
its own units (s for time constants, N for per-rotor thrust, m for range); e dimensionless.
Arc (log-log) elasticity e = d ln v / d ln x evaluated as a finite difference between two
runs, which is what "across A -> B" means.

INDEPENDENT DERIVATION. Pure arithmetic on the lens's own reported speeds; this check tests
internal consistency and the comparative statements, not the simulation that produced the
speeds. Where only one of the two speeds is reported, the elasticity is used to predict the
other and the prediction is cross-checked against a second, independent route.
"""
import sys
from math import log

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, quantity  # noqa: E402


def elast(v1, v2, x1, x2):
    return log(v2 / v1) / log(x2 / x1)


print("=== elasticities recomputed from the lens's own reported speed pairs ===")
rows = [
    ("motor_tau 39.1 -> 78.2 ms, 0.20 m tol", 16.165, 7.954, 39.1, 78.2, -1.023),
    ("motor_tau 5 -> 10 ms (equal speeds)", 19.862, 19.862, 5.0, 10.0, 0.000),
    ("tau_vio 5 -> 130 ms (composite)", 18.892, 10.601, 5.0, 130.0, None),
    ("thrust 8.5 -> 10 N (0.50 m tol)", 19.592, 19.602, 8.5, 10.0, 0.003),
    ("range 3 -> 6 m, tau = 50 ms", 8.541, 16.920, 3.0, 6.0, 0.986),
    ("range 6 -> 10 m, tau = 50 ms", 16.920, 29.412, 6.0, 10.0, 1.082),
]
got = {}
for name, v1, v2, x1, x2, claimed in rows:
    e = elast(v1, v2, x1, x2)
    got[name] = e
    tag = "" if claimed is None else f" (lens {claimed:+.3f})"
    print(f"  {name:<42s}: e = {e:+.4f}{tag}")

print("\n=== thrust row: two independent routes to the speed at 10 N per rotor ===")
v6 = 16.840
v75 = v6 * (7.5 / 6.0) ** 0.527
v10_a = v6 * (10.0 / 6.0) ** 0.297
v10_b = 19.592 * (10.0 / 8.5) ** 0.003
print(f"  from e(6 -> 7.5) = +0.527 and v(6 N) = {v6} m/s: v(7.5 N) = {v75:.3f} m/s")
print(f"  from e(6 -> 10) = +0.297: v(10 N) = {v10_a:.4f} m/s")
print(f"  from e(8.5 -> 10) = +0.003 and v(8.5 N) = 19.592 m/s: v(10 N) = {v10_b:.4f} m/s")
print(f"  the two routes agree to {100*abs(v10_a-v10_b)/v10_b:.3f} per cent")

print("\n=== tau_vio rows: implied intermediate speeds, monotonicity ===")
v40 = 10.601 * (130.0 / 40.0) ** 0.267
v10 = v40 * (40.0 / 10.0) ** 0.132
print(f"  from e(40 -> 130) = -0.267 and v(130) = 10.601 m/s: v(40) = {v40:.3f} m/s")
print(f"  from e(10 -> 40) = -0.132: v(10) = {v10:.3f} m/s")
print(f"  implied e(5 -> 10) with v(5) = 18.892 m/s: {elast(18.892, v10, 5.0, 10.0):+.4f}")
print(f"  composite e(5 -> 130) = {elast(18.892, 10.601, 5.0, 130.0):+.4f}")

print("\n=== the comparative statements ===")
hw, mine = 0.565, 0.527
print(f"  thrust elasticity: mine {mine:+.3f} vs hardware {hw:+.3f} -> "
      f"{100*abs(mine-hw)/hw:.2f} per cent apart")
seen = {"thrust-to-weight": 0.527, "motor time constant": 0.462, "aero magnitude": 0.381,
        "VIO latency": 0.132}
vals = sorted(seen.values())
print(f"  seen-course set {seen}: largest/smallest = {vals[-1]/vals[0]:.3f}, "
      f"two biggest apart by {100*(vals[-1]-vals[-2])/vals[-2]:.2f} per cent")
rivals = {"thrust-to-weight": 0.527, "motor time constant": 0.462, "VIO latency": 0.267,
          "perception latency": 0.143, "IMU latency": 0.348}
for name, r in sorted(rivals.items(), key=lambda kv: -kv[1]):
    print(f"  range 0.986 / {name} {r:.3f} = {0.986/r:.2f} x ; with 1.082: {1.082/r:.2f} x")
print(f"  |e_range/e_latency| = 0.986/0.105 = {0.986/0.105:.2f}")

print("\n=== checks ===")
quantity(f"{got['motor_tau 39.1 -> 78.2 ms, 0.20 m tol']:.4f}", "-1.023", rel_tol=1e-3)
quantity(f"{got['range 3 -> 6 m, tau = 50 ms']:.4f}", "0.986", rel_tol=1e-3)
quantity(f"{got['range 6 -> 10 m, tau = 50 ms']:.4f}", "1.082", rel_tol=1e-3)
quantity(f"{got['thrust 8.5 -> 10 N (0.50 m tol)']:.6f}", "0.003", rel_tol=0.05)
quantity(f"{v10_a:.4f}", f"{v10_b:.4f}", rel_tol=1e-3)
quantity(f"{100*abs(mine-hw)/hw:.4f}", "7.0", rel_tol=0.05)
quantity(f"{0.986/0.105:.4f}", "9.4", rel_tol=2e-3)
inequality(f"{vals[-1]/vals[0]:.4f}", "<", "4")
inequality(f"{100*(vals[-1]-vals[-2])/vals[-2]:.4f}", "<", "15")
# "2 to 10 times every rival": the weakest case is the thrust elasticity
print("  the 'at least 2x every rival' claim, worst case:")
inequality(f"{0.986/0.527:.4f}", ">=", "2")
# arc elasticity identities: it is antisymmetric and composes additively in log space
e_s = __import__("sympy").symbols("v1 v2 x1 x2", positive=True)
v1s, v2s, x1s, x2s = e_s
import sympy as sp  # noqa: E402

identity(sp.log(v2s / v1s) / sp.log(x2s / x1s), sp.log(v1s / v2s) / sp.log(x1s / x2s))
# a linear law v = c x gives e = 1 exactly
c, x1n, x2n = sp.symbols("c x1n x2n", positive=True)
identity(sp.log(c * x2n / (c * x1n)) / sp.log(x2n / x1n), sp.Integer(1))
raise SystemExit(finish())
