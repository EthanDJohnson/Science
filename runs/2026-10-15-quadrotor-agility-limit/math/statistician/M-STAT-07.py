"""M-STAT-07  (statistician F7; STAT-A, STAT-E; table row S12)

Claim checked, stated precisely.
  Point-mass thrust-to-weight model [D-33, A-34]: at constant altitude the usable horizontal
  acceleration is a_h = g sqrt(TW^2 - 1) (m/s^2), with TW = T/W > 1 dimensionless and
  g = 9.81 m/s^2. On a rest-to-rest bang-bang segment of fixed length d (m) the traversal time is
  t = 2 sqrt(d/a_h) and the mean speed is v_bar = d/t = sqrt(d a_h)/2, so
      dln t/dln a_h = -1/2 exactly,  dln v_bar/dln a_h = +1/2 exactly,
      dln a_h/dln TW = TW^2/(TW^2 - 1),
      e_TW := dln v_bar/dln TW = (1/2) TW^2/(TW^2 - 1) = 8/15 = 0.5333 at TW = 4.
  The lens compares this with the planner sweep [A-16] (lap 7.14 s at TWR 2.5, 5.81 s at TWR 3.6),
  whose log-log slope it reports as dln(lap)/dln(TWR) = -0.565, and states the two agree to 6 %.
Domain: TW > 1, d > 0 m, g > 0 m/s^2.

Independent derivation: a_h from the force balance (T^2 = W^2 + (m a_h)^2 for level flight at full
thrust); the bang-bang time by direct integration of the two-phase constant-acceleration profile
(not from the closed form); elasticities symbolically in SymPy and by finite differences; the
A-16 slope from the two reported (TWR, lap) points by ln-ratio.
"""
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

G = 9.81


def a_h(tw):
    return G * np.sqrt(tw ** 2 - 1)


def bang_bang_time(d, a, steps=2_000_000):
    """Integrate accelerate-then-decelerate over distance d; returns time (s) and mean speed."""
    half = d / 2
    dt = 2 * np.sqrt(half / a) / steps          # time for the accelerating half
    x, v, t = 0.0, 0.0, 0.0
    while x < half:
        x += v * dt
        v += a * dt
        t += dt
    return 2 * t, d / (2 * t)


print("=== M-STAT-07: thrust-to-weight elasticity; SI units (m, s, m/s, m/s^2) ===")
for tw in (2.0, 4.0, 8.0):
    print(f"TW = {tw}: a_h = {a_h(tw):.3f} m/s^2, dln a_h/dln TW = {tw ** 2 / (tw ** 2 - 1):.4f}")
d = 10.0
t_num, v_num = bang_bang_time(d, a_h(4.0))
t_cf = 2 * np.sqrt(d / a_h(4.0))
print(f"10 m rest-to-rest at TW = 4: t = {t_num:.4f} s (integrated) vs {t_cf:.4f} s (closed form); "
      f"mean speed = {v_num:.3f} m/s vs {np.sqrt(d * a_h(4.0)) / 2:.3f} m/s; "
      f"peak speed = {np.sqrt(d * a_h(4.0)):.3f} m/s")
e_tw = 0.5 * 16 / 15
print(f"e_TW = dln(mean speed)/dln(TW) at TW = 4: {e_tw:.4f}")
# finite-difference check of the full chain TW -> a_h -> mean speed
h = 1e-6
fd = (np.log(np.sqrt(d * a_h(4.0 * (1 + h))) / 2) - np.log(np.sqrt(d * a_h(4.0 * (1 - h))) / 2)) / (2 * h)
print(f"e_TW by finite difference: {fd:.6f}")
slope = np.log(5.81 / 7.14) / np.log(3.6 / 2.5)
print(f"[A-16] planner slope dln(lap)/dln(TWR) = {slope:.4f} (lens: -0.565)")
print(f"relative gap to the point-mass 8/15: {(abs(slope) - e_tw) / e_tw * 100:.2f} %")

units("9.81 m/s^2 * 3.8729833", "acceleration")
units("(10 m * 37.99 m/s^2)^0.5/2", "speed")
quantity(f"{a_h(2.0):.4f} m/s^2", "16.99 m/s^2", rel_tol=1e-3)
quantity(f"{a_h(4.0):.4f} m/s^2", "37.99 m/s^2", rel_tol=1e-3)
quantity(f"{a_h(8.0):.4f} m/s^2", "77.86 m/s^2", rel_tol=1e-3)
quantity(f"{t_cf:.4f} s", "1.03 s", rel_tol=5e-3)
quantity(f"{np.sqrt(d * a_h(4.0)) / 2:.4f} m/s", "9.8 m/s", rel_tol=1e-2)  # [A-34] rounds 9.746 to 9.8
quantity(f"{16 / 15:.6f}", "1.07", rel_tol=5e-3)
quantity(f"{e_tw:.6f}", "0.533", rel_tol=2e-3)
quantity(f"{slope:.6f}", "-0.565", rel_tol=3e-3)
quantity(f"{(abs(slope) - e_tw) / e_tw * 100:.4f}", "6", rel_tol=5e-2)
inequality(f"abs({t_num:.6f} - {t_cf:.6f})", "<", "1e-3")       # integration vs closed form
inequality(f"abs({fd:.9f} - {e_tw:.9f})", "<", "1e-6")

tw, dd, gg = sp.symbols("tw d gg", positive=True)
ah = gg * sp.sqrt(tw ** 2 - 1)
vbar = sp.sqrt(dd * ah) / 2
tt = 2 * sp.sqrt(dd / ah)
dom = {"tw": (1.01, 50.0), "d": (0.1, 100.0), "gg": (1.0, 20.0)}
identity(sp.simplify(ah / tt * sp.diff(tt, ah.free_symbols and ah)) if False else
         sp.simplify(tw / vbar * sp.diff(vbar, tw)), tw ** 2 / (2 * (tw ** 2 - 1)), domain=dom)
identity(sp.simplify(dd / tt * sp.diff(tt, dd)), sp.Rational(1, 2), domain=dom)
identity(sp.simplify(dd / vbar * sp.diff(vbar, dd)), sp.Rational(1, 2), domain=dom)
# elasticity of time to a_h is exactly -1/2 (substitute a for g sqrt(tw^2-1))
a_sym = sp.symbols("a", positive=True)
t_of_a = 2 * sp.sqrt(dd / a_sym)
identity(sp.simplify(a_sym / t_of_a * sp.diff(t_of_a, a_sym)), -sp.Rational(1, 2),
         domain={"d": (0.1, 100.0), "a": (1.0, 200.0)})
# limits: TW -> oo makes e_TW -> 1/2; TW -> 1+ makes it diverge (hover, no horizontal thrust)
limit(sp.simplify(tw / vbar * sp.diff(vbar, tw)), "tw", "oo", sp.Rational(1, 2), domain=dom)
limit(ah, "tw", 1, sp.Integer(0), domain=dom)
raise SystemExit(finish())
