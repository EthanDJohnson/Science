"""M-STAT-06  (statistician F6; STAT-F; table row S10)

Claim checked, stated precisely.
  Lateral-dodge bound [D-31]: at constant forward speed v (m/s) toward an obstacle of radius
  r (m) first sensed at range s (m), with bounded lateral acceleration u2 (m/s^2) and total
  perception latency tau (s):
      v_max = s / (tau + 2 sqrt(r / u2)).
  Elasticities e_s = dln v/dln s, e_a = dln v/dln u2, e_tau = dln v/dln tau. The lens asserts
  (with r = 0.5 m):
      e_tau runs from -0.069 (tau = 17 ms, u2 = 38 m/s^2) to -0.362 (tau = 130 ms, u2 = 38),
      and |e_tau| = 0.50 ("parity" with the stop bound's e_range ~ 0.5) only at
      tau = 161 ms for u2 = 77 m/s^2, 229 ms for 38 m/s^2 and 343 ms for 17 m/s^2;
  and the dossier's [A-33] dodge cases: e_s = 1 exactly, e_tau = -0.14 (s = 6 m, u2 = 20,
  tau = 50 ms) and -0.08 (u2 = 40, tau = 20 ms), e_a = 0.43 and 0.46, and e_tau = -0.24 at
  s = 10 m, tau = 100 ms, u2 = 20 m/s^2.
Domain: s, r > 0 m, u2 > 0 m/s^2, tau >= 0 s; the bound is meaningful only where
tau < s/v is satisfiable, i.e. v_max > 0, which holds for all tau >= 0 here.

Independent derivation: v_max from the definition; elasticities by central finite differences on
ln v and in closed form from
      e_s = 1,  e_tau = -tau/D,  e_a = sqrt(r/u2)/D,  D = tau + 2 sqrt(r/u2),
which imply the identity e_tau + 2 e_a = 1 (checked symbolically). |e_tau| = 1/2 therefore holds
exactly at tau = 2 sqrt(r/u2), solved both in closed form and numerically by bisection.
"""
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

R = 0.5     # obstacle radius, m


def v_dodge(s, u2, tau, r=R):
    return s / (tau + 2 * np.sqrt(r / u2))


def el_fd(s, u2, tau, r=R, h=1e-6):
    out = {}
    for name, idx in (("s", 0), ("a", 1), ("tau", 2)):
        hi, lo = [s, u2, tau], [s, u2, tau]
        hi[idx] *= 1 + h
        lo[idx] *= 1 - h
        out[name] = (np.log(v_dodge(*hi, r=r)) - np.log(v_dodge(*lo, r=r))) / (2 * h)
    return out


def el_cf(s, u2, tau, r=R):
    D = tau + 2 * np.sqrt(r / u2)
    return {"s": 1.0, "a": np.sqrt(r / u2) / D, "tau": -tau / D}


print("=== M-STAT-06: lateral-dodge bound, r = 0.5 m; SI units ===")
for u2, tau in ((38.0, 0.017), (38.0, 0.130), (20.0, 0.050), (40.0, 0.020)):
    cf, fd = el_cf(6.0, u2, tau), el_fd(6.0, u2, tau)
    print(f"s = 6 m, u2 = {u2:5.1f} m/s^2, tau = {tau * 1000:5.0f} ms: v = {v_dodge(6.0, u2, tau):6.3f} m/s  "
          f"e_s = {cf['s']:.4f} (fd {fd['s']:.4f})  e_a = {cf['a']:.4f} (fd {fd['a']:.4f})  "
          f"e_tau = {cf['tau']:.4f} (fd {fd['tau']:.4f})")
c10 = el_cf(10.0, 20.0, 0.100)
print(f"s = 10 m, u2 = 20 m/s^2, tau = 100 ms: v = {v_dodge(10.0, 20.0, 0.100):.3f} m/s, "
      f"e_tau = {c10['tau']:.4f}")
print("parity |e_tau| = 0.50:")
for u2 in (77.0, 38.0, 17.0):
    closed = 2 * np.sqrt(R / u2)
    num = brentq(lambda t: abs(el_cf(6.0, u2, t)["tau"]) - 0.5, 1e-6, 10.0, xtol=1e-14)
    print(f"  u2 = {u2:5.1f} m/s^2 -> tau = {closed * 1000:7.2f} ms (closed form), "
          f"{num * 1000:7.2f} ms (bisection)")

units("6 m / (0.04 s + 2*(0.5 m/(38 m/s^2))^0.5)", "speed")
units("2*(0.5 m/(38 m/s^2))^0.5", "time")
quantity("2*(0.5 m/(38 m/s^2))^0.5", "0.229416 s", rel_tol=1e-4)
quantity(f"{-el_cf(6.0, 38.0, 0.017)['tau']:.6f}", "0.069", rel_tol=1e-2)
quantity(f"{-el_cf(6.0, 38.0, 0.130)['tau']:.6f}", "0.362", rel_tol=1e-2)
quantity(f"{-el_cf(6.0, 20.0, 0.050)['tau']:.6f}", "0.14", rel_tol=3e-2)
quantity(f"{-el_cf(6.0, 40.0, 0.020)['tau']:.6f}", "0.08", rel_tol=3e-2)
quantity(f"{el_cf(6.0, 20.0, 0.050)['a']:.6f}", "0.43", rel_tol=3e-2)
quantity(f"{el_cf(6.0, 40.0, 0.020)['a']:.6f}", "0.46", rel_tol=3e-2)
quantity(f"{-c10['tau']:.6f}", "0.24", rel_tol=3e-2)
quantity(f"{2 * np.sqrt(R / 77.0) * 1000:.4f} ms", "161 ms", rel_tol=5e-3)
quantity(f"{2 * np.sqrt(R / 38.0) * 1000:.4f} ms", "229 ms", rel_tol=5e-3)
quantity(f"{2 * np.sqrt(R / 17.0) * 1000:.4f} ms", "343 ms", rel_tol=5e-3)
inequality(f"abs({el_cf(6.0, 38.0, 0.04)['s']:.9f} - 1)", "<", "1e-12")
inequality(f"abs({brentq(lambda t: abs(el_cf(6.0, 38.0, t)['tau']) - 0.5, 1e-6, 10.0):.9f} - "
           f"{2 * np.sqrt(R / 38.0):.9f})", "<", "1e-6")

s_, u_, t_, r_ = sp.symbols("s u t r", positive=True)
v_ = s_ / (t_ + 2 * sp.sqrt(r_ / u_))
dom = {"s": (0.1, 100), "u": (1.0, 200), "t": (0.001, 1.0), "r": (0.05, 2.0)}
e_s = sp.simplify(s_ / v_ * sp.diff(v_, s_))
e_a = sp.simplify(u_ / v_ * sp.diff(v_, u_))
e_t = sp.simplify(t_ / v_ * sp.diff(v_, t_))
identity(e_s, sp.Integer(1), domain=dom)
identity(2 * e_a - e_t, sp.Integer(1), domain=dom)
identity(e_t, -t_ / (t_ + 2 * sp.sqrt(r_ / u_)), domain=dom)
# limits: tau -> 0 removes the latency penalty; u2 -> oo makes the bound purely latency-limited
limit(e_t, "t", 0, sp.Integer(0), domain=dom)
limit(e_a, "t", 0, sp.Rational(1, 2), domain=dom)
limit(e_t, "u", "oo", sp.Integer(-1), domain=dom)
limit(v_, "u", "oo", s_ / t_, domain=dom)
raise SystemExit(finish())
