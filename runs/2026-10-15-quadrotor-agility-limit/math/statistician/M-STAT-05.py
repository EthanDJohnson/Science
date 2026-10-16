"""M-STAT-05  (statistician F6, F7; STAT-D; table rows S9, S10)

Claim checked, stated precisely.
  Stop-before-obstacle bound [D-32]: a point mass flying at speed v (m/s) first senses an obstacle
  at range s (m), reacts after a total latency tau (s), then brakes at constant a (m/s^2):
      v*tau + v^2/(2a) = s   =>   v_max(s, a, tau) = a*(-tau + sqrt(tau^2 + 2 s/a)).
  Elasticities at fixed obstacle geometry, one input perturbed at a time:
      e_range = dln v/dln s, e_accel = dln v/dln a, e_latency = dln v/dln tau.
  The lens asserts, at s = 6 m, a = 38 m/s^2 (T/W 4.1) and tau = 40 ms:
      e_range = +0.536, e_accel = +0.464, e_latency = -0.071 (ratio 7.5x);
  at tau = 17 ms the ratio is 17x and at tau = 130 ms it is 2.7x, with e_range spanning
  0.52-0.61, e_accel 0.39-0.49 and e_latency -0.030 to -0.225; the latency term v*tau equals the
  braking term v^2/(2a) at v = 2 a tau = 3.0 m/s.
  It also reports reproducing the dossier's [A-33] case s = 6 m, a = 20 m/s^2, tau = 50 ms:
  v = 14.524 m/s (dossier 14.5) with e_latency = -0.0644 (dossier -0.064).
Domain: s > 0 m, a > 0 m/s^2, tau >= 0 s, v > 0 m/s.

Independent derivation: v_max is obtained (i) from the quadratic root, (ii) by bisection on
f(v) = v*tau + v^2/(2a) - s, and (iii) by forward Euler integration of the stopping manoeuvre
(coast for tau, then decelerate at a) to confirm the stopping distance equals s. Elasticities are
computed by central finite differences on ln v and, independently, in closed form by implicit
differentiation of v*tau + v^2/(2a) = s, which gives with D = v*tau + v^2/a
      e_range = s/D,  e_accel = (v^2/(2a))/D,  e_latency = -(v*tau)/D,
so that e_range + e_accel = 1 identically. The identity and the tau -> 0 limits are checked in
SymPy.
"""
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402


def v_root(s, a, tau):
    return a * (-tau + np.sqrt(tau ** 2 + 2 * s / a))


def v_bisect(s, a, tau):
    return brentq(lambda v: v * tau + v * v / (2 * a) - s, 1e-9, 1e4, xtol=1e-13)


def stop_distance(v, a, tau, steps=4_000_000):
    """Forward Euler: coast tau, then brake at a until v = 0."""
    t_total = tau + v / a
    dt = t_total / steps
    x, u = 0.0, v
    for i in range(steps):
        x += u * dt
        if i * dt >= tau:
            u = max(0.0, u - a * dt)
    return x


def elasticities_fd(s, a, tau, h=1e-6):
    out = {}
    for name, idx in (("range", 0), ("accel", 1), ("latency", 2)):
        base = [s, a, tau]
        if base[idx] == 0:
            out[name] = 0.0
            continue
        hi, lo = list(base), list(base)
        hi[idx] *= 1 + h
        lo[idx] *= 1 - h
        out[name] = (np.log(v_root(*hi)) - np.log(v_root(*lo))) / (2 * h)
    return out


def elasticities_cf(s, a, tau):
    v = v_root(s, a, tau)
    D = v * tau + v * v / a
    return {"range": s / D, "accel": (v * v / (2 * a)) / D, "latency": -(v * tau) / D}


print("=== M-STAT-05: stop-before-obstacle bound; SI units (m, s, m/s, m/s^2) ===")
base = (6.0, 38.0, 0.040)
v0 = v_root(*base)
print(f"s = 6 m, a = 38 m/s^2, tau = 40 ms -> v_max = {v0:.4f} m/s "
      f"(bisection {v_bisect(*base):.4f} m/s)")
print(f"integration check: stopping distance from {v0:.4f} m/s = "
      f"{stop_distance(v0, 38.0, 0.040, 200000):.4f} m (target 6 m)")
for tau in (0.040, 0.017, 0.130):
    fd, cf = elasticities_fd(6.0, 38.0, tau), elasticities_cf(6.0, 38.0, tau)
    ratio = cf["range"] / abs(cf["latency"])
    print(f"tau = {tau * 1000:5.0f} ms: v = {v_root(6.0, 38.0, tau):6.3f} m/s  "
          f"e_range = {cf['range']:.4f} (fd {fd['range']:.4f})  e_accel = {cf['accel']:.4f} "
          f"(fd {fd['accel']:.4f})  e_latency = {cf['latency']:.4f} (fd {fd['latency']:.4f})  "
          f"range/latency = {ratio:.2f}x")
a33 = elasticities_cf(6.0, 20.0, 0.050)
print(f"[A-33] case s = 6 m, a = 20 m/s^2, tau = 50 ms: v = {v_root(6.0, 20.0, 0.050):.4f} m/s, "
      f"e_range = {a33['range']:.4f}, e_accel = {a33['accel']:.4f}, e_latency = {a33['latency']:.4f}")
a33b = elasticities_cf(6.0, 40.0, 0.020)
print(f"[A-33] case s = 6 m, a = 40 m/s^2, tau = 20 ms: v = {v_root(6.0, 40.0, 0.020):.4f} m/s, "
      f"e_latency = {a33b['latency']:.4f}")
print(f"crossover v where v*tau = v^2/(2a): 2*a*tau = {2 * 38.0 * 0.040:.3f} m/s")
print(f"tau -> 0 limit: sqrt(2 a s) = {np.sqrt(2 * 38.0 * 6.0):.4f} m/s, v(tau=1e-9) = "
      f"{v_root(6.0, 38.0, 1e-9):.4f} m/s")

cf0 = elasticities_cf(*base)
units("38 m/s^2 * 0.04 s", "speed")
units("(2 * 38 m/s^2 * 6 m)^0.5", "speed")
quantity("(2 * 38 m/s^2 * 6 m)^0.5", "21.3542 m/s", rel_tol=1e-4)
quantity(f"{v0:.6f} m/s", f"{v_bisect(*base):.6f} m/s", rel_tol=1e-9)
quantity(f"{stop_distance(v0, 38.0, 0.040, 200000):.6f} m", "6 m", rel_tol=2e-4)
quantity(f"{cf0['range']:.6f}", "0.536", rel_tol=3e-3)
quantity(f"{cf0['accel']:.6f}", "0.464", rel_tol=3e-3)
quantity(f"{-cf0['latency']:.6f}", "0.071", rel_tol=1e-2)
quantity(f"{cf0['range'] / abs(cf0['latency']):.4f}", "7.5", rel_tol=1e-2)
quantity(f"{elasticities_cf(6.0, 38.0, 0.017)['range'] / abs(elasticities_cf(6.0, 38.0, 0.017)['latency']):.4f}",
         "17", rel_tol=2e-2)
quantity(f"{elasticities_cf(6.0, 38.0, 0.130)['range'] / abs(elasticities_cf(6.0, 38.0, 0.130)['latency']):.4f}",
         "2.7", rel_tol=2e-2)
quantity(f"{-elasticities_cf(6.0, 38.0, 0.017)['latency']:.6f}", "0.030", rel_tol=2e-2)
quantity(f"{-elasticities_cf(6.0, 38.0, 0.130)['latency']:.6f}", "0.225", rel_tol=2e-2)
quantity(f"{elasticities_cf(6.0, 38.0, 0.130)['range']:.6f}", "0.61", rel_tol=1e-2)
quantity(f"{elasticities_cf(6.0, 38.0, 0.130)['accel']:.6f}", "0.39", rel_tol=2e-2)
quantity(f"{v_root(6.0, 20.0, 0.050):.6f} m/s", "14.524 m/s", rel_tol=1e-4)
quantity(f"{-a33['latency']:.6f}", "0.0644", rel_tol=5e-3)
quantity(f"{-a33b['latency']:.6f}", "0.037", rel_tol=2e-2)
quantity(f"{2 * 38.0 * 0.040:.6f} m/s", "3.0 m/s", rel_tol=2e-2)
inequality(f"abs({cf0['range'] + cf0['accel']:.12f} - 1)", "<", "1e-9")
inequality(f"abs({cf0['range']:.9f} - {elasticities_fd(*base)['range']:.9f})", "<", "1e-6")
inequality(f"abs({cf0['latency']:.9f} - {elasticities_fd(*base)['latency']:.9f})", "<", "1e-6")

# symbolic: e_range + e_accel = 1 and e_latency = -v tau/(v tau + v^2/a) for all s, a, tau > 0
s_, a_, t_ = sp.symbols("s a t", positive=True)
v_ = a_ * (-t_ + sp.sqrt(t_ ** 2 + 2 * s_ / a_))
e_s = sp.simplify(s_ / v_ * sp.diff(v_, s_))
e_a = sp.simplify(a_ / v_ * sp.diff(v_, a_))
e_t = sp.simplify(t_ / v_ * sp.diff(v_, t_))
D_ = v_ * t_ + v_ ** 2 / a_
identity(e_s + e_a, sp.Integer(1), domain={"s": (0.1, 100), "a": (1.0, 200), "t": (0.001, 1.0)})
identity(e_t, -v_ * t_ / D_, domain={"s": (0.1, 100), "a": (1.0, 200), "t": (0.001, 1.0)})
identity(e_s, s_ / D_, domain={"s": (0.1, 100), "a": (1.0, 200), "t": (0.001, 1.0)})
# tau -> 0: the bound becomes sqrt(2 a s) and the elasticities become 1/2, 1/2, 0
limit(v_, "t", 0, sp.sqrt(2 * a_ * s_), domain={"s": (0.1, 100), "a": (1.0, 200)})
limit(e_s, "t", 0, sp.Rational(1, 2), domain={"s": (0.1, 100), "a": (1.0, 200)})
limit(e_a, "t", 0, sp.Rational(1, 2), domain={"s": (0.1, 100), "a": (1.0, 200)})
limit(e_t, "t", 0, sp.Integer(0), domain={"s": (0.1, 100), "a": (1.0, 200)})
# latency-dominated limit: tau -> oo gives v -> s/tau and e_latency -> -1
limit(e_t, "t", "oo", sp.Integer(-1), domain={"s": (0.1, 100), "a": (1.0, 200)})
raise SystemExit(finish())
