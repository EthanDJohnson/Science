"""M-EMP-08. The point-mass thrust bound over the 40 m line, and the observed fractions.

Claims (empiricist F6; load-bearing for EMP-F's elimination and EMP-B):
(a) a T/W = 4.4 platform over a 40 m straight line has a point-mass mean speed of
    20.5 m/s (bang-bang: accelerate for half the distance, brake for the other half);
(b) the observed 5-10 m/s is 0.24-0.49 of that bound;
(c) the observed 5-7 m/s is 0.37-0.58 of the paper's own 12.0-13.5 m/s
    perception-latency bound.

Symbols: T/W = thrust-to-weight ratio (dimensionless, > 1); g = 9.81 m/s^2;
a_max = g*sqrt((T/W)^2 - 1) the horizontal acceleration available while holding
altitude (m/s^2); L = 40 m (> 0); mean speed v_bar = L/t_total (m/s).
Bang-bang over L from rest to rest: t_total = 2*sqrt(L/a_max), v_peak =
sqrt(a_max*L), v_bar = v_peak/2 = sqrt(a_max*L)/2.
Assumptions: point mass, no drag, instant thrust reversal, start and end at rest,
level flight with altitude held (hence the sqrt((T/W)^2 - 1) projection).
Independent route: numerical integration of the two-phase velocity profile.
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

g, TW, L = 9.81, 4.4, 40.0
a_max = g * np.sqrt(TW**2 - 1)
t_half = np.sqrt(L / a_max)
t_total = 2 * t_half
v_peak = a_max * t_half
v_bar = L / t_total
print(f"inputs: T/W = {TW}, g = {g} m/s^2, L = {L} m")
print(f"a_max = {a_max:.4f} m/s^2 = {a_max / g:.3f} g; t_total = {t_total:.5f} s; "
      f"v_peak = {v_peak:.4f} m/s; mean = {v_bar:.4f} m/s (claimed 20.5 m/s)")
inequality(f"abs({v_bar:.6f} - 20.5)", "<", "0.06")
quantity(f"(({a_max:.6f} m/s^2) * ({L} m))^0.5 / 2", "20.5 m/s", rel_tol=3e-3)
units(f"(({a_max:.6f} m/s^2) * ({L} m))^0.5 / 2", "speed")

# numerical route: integrate the triangular speed profile and check the distance
steps = 2_000_000
t = np.linspace(0.0, t_total, steps)
v = np.where(t <= t_half, a_max * t, a_max * (t_total - t))
dist = float(np.trapezoid(v, t))
print(f"integrated distance = {dist:.8f} m (should be {L} m); mean from integration = "
      f"{dist / t_total:.6f} m/s")
inequality(f"abs({dist:.8f} - {L})/{L}", "<", "1e-8")

for v_obs, claim in ((5.0, 0.244), (10.0, 0.488)):
    frac = v_obs / v_bar
    print(f"  observed {v_obs} m/s is {frac:.4f} of the thrust bound (claimed {claim})")
    inequality(f"abs({frac:.6f} - {claim})", "<", "0.004")

for v_obs, bound, claim in ((5.0, 13.5, 0.370), (7.0, 12.0, 0.583)):
    frac = v_obs / bound
    print(f"  observed {v_obs} m/s is {frac:.4f} of the {bound} m/s perception bound (claimed {claim})")
    inequality(f"abs({frac:.6f} - {claim})", "<", "0.002")

identity("sqrt(a*L)/2", "L/(2*sqrt(L/a))", domain={"a": (1.0, 200.0), "L": (1.0, 500.0)})
limit("9.81*sqrt(w**2 - 1)", "w", 1, "0", direction="+", domain={"w": (1.0, 20.0)})  # T/W -> 1: no accel
limit("sqrt(9.81*sqrt(w**2 - 1)*40)/2", "w", "oo", "oo", domain={"w": (1.0, 100.0)})
# mean speed is half the peak speed for a symmetric bang-bang profile
inequality("sqrt(a*L)/2", "<", "sqrt(a*L)", domain={"a": (1.0, 200.0), "L": (1.0, 500.0)})
raise SystemExit(finish())
