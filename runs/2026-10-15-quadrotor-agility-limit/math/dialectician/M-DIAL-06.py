"""M-DIAL-06. Clutter-regime elasticities of the dodge bound, and the three finite swaps.

Claim (lens finding 7 and finding 11; candidates DIAL-A and DIAL-E):
  With v = s/(tau + 2 sqrt(r/a)) (dossier D-31) at the baseline s = 6 m, tau = 100 ms,
  a = 16.33 m/s^2 (FoV-limited), r = 0.5 m, the baseline speed is 13.33 m/s and the elasticities
  are e_s = +1.000, e_a = +0.387, e_tau = -0.231. Finite swaps: range 6 -> 12 m gives
  +100 per cent; a wide-FoV camera (FoV cap lifted above the thrust cap, a = 42.03 m/s^2) gives
  +41.5 per cent; latency 100 -> 30 ms gives +18.4 per cent. Spread of elasticities 4.3x.

Independent derivation (SI):
  v(s, tau, r, a) = s / (tau + 2 sqrt(r/a)) with D = tau + 2 sqrt(r/a).
  d ln v/d ln s = 1 exactly.
  d ln v/d ln tau = -tau/D.
  d ln v/d ln a = +sqrt(r/a)/D  (= half the 2 sqrt(r/a) share of D).
  Hence 0 < e_a < 1/2 and -1 < e_tau < 0, and e_a + |e_tau| < 1 with e_s = 1 always largest.
Domain: s, tau, r, a > 0.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, quantity, units, finish  # noqa: E402

S0, TAU0, R0, A0 = 6.0, 0.100, 0.5, 16.33
A_THRUST = 9.81 * math.sqrt(4.4**2 - 1.0)


def v(s=S0, tau=TAU0, r=R0, a=A0):
    return s / (tau + 2.0 * math.sqrt(r / a))


D0 = TAU0 + 2.0 * math.sqrt(R0 / A0)
print(f"baseline: s = {S0} m, tau = {TAU0*1e3:.0f} ms, r = {R0} m, a = {A0} m/s^2")
print(f"  denominator D = {D0:.6f} s, v = {v():.4f} m/s  (lens: 13.33 m/s)")
print(f"analytic elasticities: e_s = 1.000000, e_a = {math.sqrt(R0/A0)/D0:.6f}, "
      f"e_tau = {-TAU0/D0:.6f}")

def forward(f, x0, frac=0.10):
    return math.log(f(x0 * (1 + frac)) / f(x0)) / math.log(1 + frac)


def central(f, x0, frac=0.10):
    return math.log(f(x0 * (1 + frac)) / f(x0 * (1 - frac))) / math.log((1 + frac) / (1 - frac))


print("10 per cent perturbations, one at a time:")
for name, fn, x0 in (("s", lambda x: v(s=x), S0), ("a", lambda x: v(a=x), A0),
                     ("tau", lambda x: v(tau=x), TAU0)):
    print(f"  {name:4s}: forward {forward(fn, x0):+.4f}, central {central(fn, x0):+.4f}, "
          f"analytic {central(fn, x0, 1e-7):+.6f}")
print("  (the lens's +0.387 and -0.231 are forward 10 per cent differences; the analytic values "
      f"are +{math.sqrt(R0/A0)/D0:.3f} and {-TAU0/D0:.3f})")

print("finite swaps:")
for name, val in (("range 6 -> 12 m", v(s=12.0)), ("wide-FoV camera, a -> thrust cap", v(a=A_THRUST)),
                  ("latency 100 -> 30 ms", v(tau=0.030))):
    print(f"  {name:36s}: v = {val:6.3f} m/s, change {100*(val/v()-1):+6.2f} per cent")
print(f"elasticity spread |e_s/e_tau| = {1.0/(TAU0/D0):.3f} (lens: 4.3x), "
      f"|e_s/e_a| = {1.0/(math.sqrt(R0/A0)/D0):.3f} (lens quotes 2.6x from the forward values)")

# --- symbolic -----------------------------------------------------------------------
s, tau, r, a = sp.symbols("s tau r a", positive=True)
vv = s / (tau + 2 * sp.sqrt(r / a))
dom = {"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)}
identity(sp.simplify(s * sp.diff(sp.log(vv), s)), sp.Integer(1), domain=dom)
identity(sp.simplify(tau * sp.diff(sp.log(vv), tau)),
         -tau / (tau + 2 * sp.sqrt(r / a)), domain=dom)
identity(sp.simplify(a * sp.diff(sp.log(vv), a)),
         sp.sqrt(r / a) / (tau + 2 * sp.sqrt(r / a)), domain=dom)
# bounds: e_a < 1/2 and |e_tau| < 1 always, so range always dominates
inequality(sp.sqrt(r / a) / (tau + 2 * sp.sqrt(r / a)), "<", sp.Rational(1, 2), domain=dom)
inequality(tau / (tau + 2 * sp.sqrt(r / a)), "<", sp.Integer(1), domain=dom)
# zero-latency limit: e_a -> 1/2, e_tau -> 0
limit(sp.sqrt(r / a) / (tau + 2 * sp.sqrt(r / a)), "tau", 0, sp.Rational(1, 2), domain=dom)
limit(tau / (tau + 2 * sp.sqrt(r / a)), "tau", 0, sp.Integer(0), domain=dom)
# infinite acceleration: the bound reduces to the pure latency bound s/tau
limit(vv, "a", "oo", s / tau, domain=dom)
quantity("6 m / (0.1 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "13.334 m/s", rel_tol=2e-3)
quantity("6 m / (0.03 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "15.791 m/s", rel_tol=2e-3)
quantity("6 m / (0.1 s + 2*(0.5 m/(42.03 m/s^2))^0.5)", "18.86 m/s", rel_tol=2e-3)
units("6 m / (0.1 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "speed")

raise SystemExit(finish())
