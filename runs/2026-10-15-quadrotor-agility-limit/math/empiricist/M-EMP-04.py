"""M-EMP-04. What a 2.58x speed gain would cost through each single limit.

Claims (empiricist F4; load-bearing for EMP-A):
with a constant elasticity e = d ln v / d ln X of mean speed v with respect to a
limit X, buying a factor R = 2.58 in speed needs X multiplied by R^(1/e):
  e(v, T/W) = 0.5  -> X factor 6.66, so T/W from 4.4 to ~29;
  e(v, range) = 1.0 -> 2.6x range;  e(v, range) = 0.52 -> 6.2x range;
  |e(v, tau)| = 0.24 -> latency divided by ~52.
And: the latency route is unachievable because tau cannot go below zero.

Symbols: v mean speed (m/s), X the limit's value in its own units (T/W
dimensionless, range in m, latency tau in s), e dimensionless elasticity > 0 in
magnitude, R = 2.58 dimensionless. Domain: e > 0, R > 1. Assumption: v = C*X^e
exactly over the whole 1x..6.66x span, i.e. a constant elasticity extrapolated
far outside the point where it was computed.

Independent cross-check of the "tau cannot go below zero" step, which does not
need the power law: with the exact stop bound v*tau + v^2/(2a) = d, the speed at
tau = 0 is sqrt(2 a d), so the largest factor latency alone can buy is
sqrt(2 a d) / v(tau) -- computed here for d = 6 m, a = 40 m/s^2, tau = 40 ms.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

R = 2.58
print(f"inputs: R = {R} (seen/unseen speed ratio), elasticities from the dossier")
for name, e, claim, tol in (("T/W", 0.5, 6.656, 0.01),
                            ("range (dodge, e=1.0)", 1.0, 2.58, 0.005),
                            ("range (stop, e=0.52)", 0.52, 6.19, 0.02),
                            ("latency (|e|=0.24)", 0.24, 51.9, 0.3)):
    factor = R ** (1 / e)
    print(f"  e = {e}: required X factor = {factor:.4f} (claimed {claim})")
    inequality(f"abs({factor:.6f} - {claim})", "<", f"{tol}")

tw_needed = 4.4 * R ** (1 / 0.5)
print(f"T/W required = 4.4 * {R}^2 = {tw_needed:.3f} (claimed ~29)")
inequality(f"abs({tw_needed:.6f} - 29)", "<", "0.5")

# structure and limits of the constant-elasticity extrapolation
e, Rs, X = sp.symbols("e R X", positive=True)
identity((Rs ** (1 / e)) ** e, Rs, domain={"e": (0.05, 5.0), "R": (1.0, 10.0)})
limit("2.58**(1/e)", "e", "oo", "1")        # a perfectly elastic limit needs no change
limit("2.58**(1/e)", "e", 0, "oo", direction="+")   # an inelastic limit needs an unbounded change
units("(4.4 m) / (1 m)", "dimensionless")

# exact stop bound: the most that zero latency can buy
a, d, tau = 40.0, 6.0, 0.04      # m/s^2, m, s
v_tau = (-a * tau + sp.sqrt((a * tau) ** 2 + 2 * a * d)) / 1   # root of v^2/(2a) + v*tau = d
v_tau = sp.nsimplify(0) + sp.solve(sp.Symbol("v", positive=True) * tau
                                   + sp.Symbol("v", positive=True) ** 2 / (2 * a) - d,
                                   sp.Symbol("v", positive=True))[0]
v_0 = sp.sqrt(2 * a * d)
print(f"exact stop bound: v(tau=40 ms) = {float(v_tau):.4f} m/s, v(tau=0) = {float(v_0):.4f} m/s, "
      f"max factor from latency alone = {float(v_0 / v_tau):.4f}")
inequality(f"{float(v_0 / v_tau):.6f}", "<", f"{R}")        # far short of 2.58
inequality(f"{float(v_0 / v_tau):.6f}", "<", "1.10")
quantity(f"{float(v_0):.6f} m/s", "21.9089 m/s", rel_tol=1e-4)
units(f"{float(v_0):.6f} m/s", "speed")
units("((40 m/s^2) * (6 m))^0.5", "speed")
limit("sqrt(2*a*d)/((-a*t + sqrt((a*t)**2 + 2*a*d))*1)", "t", 0, "1",
      domain={"a": (1.0, 100.0), "d": (0.5, 50.0), "t": (0.0, 0.5)})
raise SystemExit(finish())
