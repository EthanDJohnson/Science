"""M-EMP-06. Required stopping distance with a sensorimotor delay.

Claim (empiricist F6; load-bearing for EMP-D and the "range is not saturated" step):
with reaction latency tau = 40 ms and braking deceleration a = 40 m/s^2, a
point mass travelling at v needs
    d_stop(v) = v*tau + v^2/(2a)
= 0.51 m at 5 m/s, 1.65 m at 10 m/s, 5.80 m at 20 m/s.

Symbols: v speed (m/s, > 0), tau delay during which the speed is unchanged (s,
>= 0), a constant deceleration (m/s^2, > 0), d_stop distance to a full stop (m).
Assumptions: straight-line motion, no drag, constant full deceleration after the
delay, and a decision taken at the instant the obstacle is seen. Independent
route: numerical integration of the two-phase motion (coast then brake).
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

tau, a = 0.040, 40.0
print(f"inputs: tau = {tau * 1e3:.0f} ms, a = {a} m/s^2")


def integrate(v0, steps=4_000_000):
    """Distance until v reaches 0: coast for tau, then brake at a."""
    t_brake = v0 / a
    t_end = tau + t_brake
    t = np.linspace(0.0, t_end, steps)
    v = np.where(t <= tau, v0, np.maximum(v0 - a * (t - tau), 0.0))
    return float(np.trapezoid(v, t)), float(v[-1])


for v, claim in ((5.0, 0.51), (10.0, 1.65), (20.0, 5.80)):
    closed = v * tau + v**2 / (2 * a)
    num, v_end = integrate(v)
    print(f"  v = {v} m/s: closed form {closed:.6f} m, integration {num:.6f} m "
          f"(rel diff {abs(num - closed) / closed:.2e}, final speed {v_end:.2e} m/s), claimed {claim} m")
    inequality(f"abs({closed:.6f} - {claim})", "<", "0.006")
    inequality(f"abs({num:.8f} - {closed:.8f})/{closed:.8f}", "<", "1e-6")
    quantity(f"{v} m/s * {tau} s + ({v} m/s)^2/(2*{a} m/s^2)", f"{closed:.6f} m", rel_tol=1e-9)

units(f"{5} m/s * {tau} s + (5 m/s)^2/(2*{a} m/s^2)", "length")
identity("v*t + v**2/(2*a)", "v*(t + v/(2*a))",
         domain={"v": (0.1, 50.0), "t": (0.0, 0.5), "a": (1.0, 100.0)})
limit("v*t + v**2/(2*a)", "t", 0, "v**2/(2*a)", domain={"v": (0.1, 50.0), "a": (1.0, 100.0)})
limit("(v*t + v**2/(2*a))/v", "v", 0, "t", domain={"t": (0.01, 0.5), "a": (1.0, 100.0)})
# quadratic growth: doubling v more than doubles the distance
inequality("2*(v*t + v**2/(2*a))", "<", "(2*v)*t + (2*v)**2/(2*a)",
           domain={"v": (0.1, 50.0), "t": (0.0, 0.5), "a": (1.0, 100.0)})
raise SystemExit(finish())
