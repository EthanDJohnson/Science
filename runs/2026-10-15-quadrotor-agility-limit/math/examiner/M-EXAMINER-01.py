#!/usr/bin/env python3
"""M-EXAMINER-01  (examiner F2a, candidate EXAMINER-B)

CLAIM, stated precisely
-----------------------
A point mass flies horizontally at speed v. An obstacle becomes visible at range s (m).
After a fixed dead time tau (s) during which the speed is unchanged, the vehicle brakes with
constant deceleration a (m/s^2) and must stop within s. The largest admissible v is the
"stop bound" v(s, a, tau).

The lens asserts, for s > 0, a > 0, tau >= 0:
 (i)  v(s, a, tau) = a*(-tau + sqrt(tau^2 + 2*s/a));
 (ii) v is homogeneous of degree 1 in (s, a) jointly: v(k*s, k*a, tau) = k*v(s, a, tau);
 (iii) hence the log-elasticities e_s = (s/v) dv/ds and e_a = (a/v) dv/da satisfy
       e_s + e_a = 1 identically (Euler's relation);
 (iv) numerically e_s/e_a = 1.155-1.221 and e_tau = (tau/v) dv/dtau = -0.036 to -0.100
       over "the same four dossier parameter cases" (the cases are not stated in the analysis).

I re-derive (i) from the braking constraint, prove (ii)-(iii) symbolically, obtain closed forms
for the three elasticities, and then test whether the two stated numeric RANGES in (iv) can come
from one common set of cases.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, sign, units  # noqa: E402

s, a, tau, k, v = sp.symbols("s a tau k v", positive=True)

# --- my own derivation: distance used = coasting + braking, set equal to the range -----------
v_sol = sp.solve(sp.Eq(v * tau + v**2 / (2 * a), s), v)
v_pos = [r for r in v_sol if sp.simplify(sp.limit(r, tau, 0)) != 0]
v_stop = sp.simplify(v_pos[0])
print("my solved stop bound v =", v_stop)

v_lens = a * (-tau + sp.sqrt(tau**2 + 2 * s / a))
identity(v_stop, v_lens, domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})

# the bound really does exhaust the range
identity(sp.expand(v_lens * tau + v_lens**2 / (2 * a)), s,
         domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})

# --- (ii) joint homogeneity of degree 1 in (s, a) --------------------------------------------
v_scaled = v_lens.subs({s: k * s, a: k * a})
identity(v_scaled, k * v_lens,
         domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0), "k": (0.01, 100.0)})

# --- (iii) elasticities and Euler's relation --------------------------------------------------
e_s = sp.simplify(s / v_lens * sp.diff(v_lens, s))
e_a = sp.simplify(a / v_lens * sp.diff(v_lens, a))
e_t = sp.simplify(tau / v_lens * sp.diff(v_lens, tau))
print("e_s =", e_s)
print("e_a =", e_a)
print("e_tau =", e_t)

identity(e_s + e_a, sp.Integer(1),
         domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})

W = sp.sqrt(tau**2 + 2 * s / a)          # W has units of time
identity(e_s, (W + tau) / (2 * W), domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})
identity(e_t, -tau / W, domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})
identity(sp.simplify(e_s / e_a), (W + tau) / (W - tau),
         domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})
# e_tau is negative on the whole domain (more delay never helps)
sign(e_t, "negative", domain={"s": (0.1, 100.0), "a": (0.1, 100.0), "tau": (1e-9, 1.0)})

# --- limit the claim must reduce to: zero delay -> textbook sqrt(2 a s), e_s = e_a = 1/2 ------
limit(v_lens, "tau", 0, sp.sqrt(2 * a * s))
limit(e_s, "tau", 0, sp.Rational(1, 2))
limit(e_a, "tau", 0, sp.Rational(1, 2))
limit(e_t, "tau", 0, sp.Integer(0))

# --- units ------------------------------------------------------------------------------------
units("39 m/s^2 * 0.04 s", "m/s")
units("2 * 39 m/s^2 * 6 m", "m^2/s^2")
units("(0.04 s)^2 + 2 * 6 m / (39 m/s^2)", "s^2")

# --- (iv) are the two stated ranges mutually consistent? --------------------------------------
# Closed form couples them exactly: with x = tau/W,  e_tau = -x and e_s/e_a = (1+x)/(1-x).
ratio_of = lambda x: (1 + x) / (1 - x)
print("\nstated e_tau range -> implied e_s/e_a range:")
for x in (0.036, 0.100):
    print(f"  |e_tau| = {x:.3f}  ->  e_s/e_a = {ratio_of(x):.4f}")
print("stated e_s/e_a range -> implied |e_tau| range:")
for r in (1.155, 1.221):
    print(f"  e_s/e_a = {r:.3f}  ->  |e_tau| = {(r - 1) / (r + 1):.4f}")

x = sp.Symbol("x", positive=True)
identity(((1 + x) / (1 - x)).subs(x, sp.Rational(36, 1000)), sp.Rational(1036, 964))
# Consistency test: if |e_tau| ever reaches 0.036 in the same case set, min(e_s/e_a) must be
# 1.0747, not 1.155.  Check the gap is real and not rounding.
gap = float(ratio_of(0.036))
print(f"\nimplied min e_s/e_a from |e_tau| = 0.036 : {gap:.4f}  vs stated min 1.155 "
      f"(relative gap {abs(gap - 1.155) / 1.155:.1%})")

# spot value at the F10 operating point (s = 6 m, a = 39 m/s^2, tau = 0.040 s)
pt = {s: 6, a: 39, tau: sp.Rational(4, 100)}
vals = {name: float(expr.subs(pt)) for name, expr in
        (("v [m/s]", v_lens), ("e_s", e_s), ("e_a", e_a), ("e_tau", e_t),
         ("e_s/e_a", sp.simplify(e_s / e_a)))}
print("\nspot values at s = 6 m, a = 39 m/s^2, tau = 0.040 s:")
for nm, val in vals.items():
    print(f"  {nm} = {val:.4f}")

raise SystemExit(finish())
