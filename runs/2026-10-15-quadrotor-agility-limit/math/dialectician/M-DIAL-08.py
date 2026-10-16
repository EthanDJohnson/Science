"""M-DIAL-08. Thrust-to-weight elasticity of speed on a rest-to-rest segment.

Claim (lens finding 2): "The point-mass ceiling gives elasticity d ln v / d ln(T/W) ~ +0.5 at
T/W >= 4", set against a planner sweep giving d ln(lap)/d ln(TWR) = -0.565.

Independent derivation (SI):
  Constant-altitude point mass: a_h = g*sqrt((T/W)^2 - 1)  (dossier D-33).
  Elasticity of a_h in T/W: d ln a_h/d ln(T/W) = (T/W)^2/((T/W)^2 - 1).
  Rest-to-rest bang-bang over a fixed distance d: d = 2*(1/2)*a*(t/2)^2 = a t^2/4, so
  t = 2 sqrt(d/a) and the average speed v = d/t = (1/2) sqrt(a d), giving
  d ln v/d ln a = +1/2 exactly and d ln t/d ln a = -1/2.
  Therefore d ln v/d ln(T/W) = (1/2)*(T/W)^2/((T/W)^2 - 1).
Domain: T/W > 1, d > 0, g > 0.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, units, quantity, finish  # noqa: E402

G = 9.81


def a_h(twr):
    return G * math.sqrt(twr**2 - 1.0)


def v_avg(twr, d=10.0):
    return 0.5 * math.sqrt(a_h(twr) * d)


def elast(f, x, frac=1e-6):
    return math.log(f(x * (1 + frac)) / f(x * (1 - frac))) / math.log((1 + frac) / (1 - frac))


print("d = 10 m rest-to-rest segment, bang-bang, no drag")
for twr in (2.0, 4.0, 4.4, 12.35):
    print(f"  T/W = {twr:5.2f}: a_h = {a_h(twr):6.2f} m/s^2, v_avg = {v_avg(twr):6.2f} m/s, "
          f"d ln a_h/d ln(T/W) = {elast(a_h, twr):.4f}, "
          f"d ln v/d ln(T/W) = {elast(v_avg, twr):.4f}")
print(f"analytic: (1/2)(T/W)^2/((T/W)^2-1) = {0.5*16/15:.4f} at T/W = 4, "
      f"{0.5*4.4**2/(4.4**2-1):.4f} at T/W = 4.4  (lens: ~+0.5; dossier D-33 elasticity 1.07)")
print("the planner sweep d ln(lap)/d ln(TWR) = -0.565 corresponds to "
      f"d ln v/d ln(TWR) = +0.565, within {abs(0.565-0.5333)/0.5333:.1%} of the point-mass value "
      "at T/W = 4 (same order, as D-33 states)")

identity("d/(2*sqrt(d/a))", "sqrt(a*d)/2", domain={"a": (1.0, 100.0), "d": (1.0, 100.0)})
identity("a*diff(log(sqrt(a*d)/2), a)", "1/2", domain={"a": (1.0, 100.0), "d": (1.0, 100.0)})
identity("w*diff(log(g*sqrt(w**2 - 1)), w)", "w**2/(w**2 - 1)",
         domain={"w": (1.05, 20.0), "g": (1.0, 20.0)})
# high-thrust limit: the T/W elasticity of a_h tends to 1, so that of speed tends to 1/2
limit("w**2/(w**2 - 1)", "w", "oo", "1")
limit("w**2/(2*(w**2 - 1))", "w", "oo", "1/2")
# near hover the elasticity blows up (so "+0.5" is a high-thrust statement only)
limit("w**2/(2*(w**2 - 1))", "w", 1, "oo")
inequality("w**2/(2*(w**2 - 1))", ">", "1/2", domain={"w": (1.05, 20.0)})
quantity("9.81 m/s^2 * (4.4^2 - 1)^0.5", "42.03 m/s^2", rel_tol=2e-3)
units("0.5 * (42.03 m/s^2 * 10 m)^0.5", "speed")

raise SystemExit(finish())
