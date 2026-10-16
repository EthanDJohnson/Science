#!/usr/bin/env python3
"""M-EXAMINER-04  (examiner F5, candidates EXAMINER-E and EXAMINER-F)

CLAIM, stated precisely
-----------------------
Loop-delay bound.  A pure time delay tau (s) contributes phase -w*tau (rad) at frequency w.
Reserving 45 deg = pi/4 rad of phase for the delay at the crossover frequency w_c gives
   w_c <= (pi/4) / tau.
 (i)   at tau = 40 ms: w_c <= 19.63 rad/s = 3.12 Hz;
 (ii)  the lens's own (unsourced) map to speed, v <= w_c * R / m, with course radius R = 5 m and
       frequency-separation factor m in {3, 5}, gives v <= 19.6-32.7 m/s at 40 ms and
       6.0-10.1 m/s at 130 ms;
 (iii) inverting, the latency at which the bound binds is tau = (pi/4) * R / (m * v):
       112-187 ms at v = 7 m/s and 79-131 ms at v = 10 m/s (R = 5 m, m = 5 and 3).

Domain: tau > 0, R > 0, m >= 1, v > 0.  Units: tau in s, R in m, w_c in rad/s, v in m/s.
The 45 deg budget and the v <= w_c R / m map are ASSUMPTIONS taken from the analysis; what is
checked here is that the arithmetic and the inversion follow from them.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

tau, R, w = sp.symbols("tau R w", positive=True)
mm, vv = sp.symbols("mm vv", positive=True)

# phase of a pure delay reaching -pi/4 defines w_c
wc = sp.solve(sp.Eq(w * tau, sp.pi / 4), w)[0]
print("w_c =", wc)
identity(wc, sp.pi / (4 * tau), domain={"tau": (0.001, 1.0)})
limit(1 / wc, "tau", 0, sp.Integer(0))                      # no delay -> no bandwidth limit
limit(wc, "tau", sp.oo, sp.Integer(0))

# speed map and its inversion must be mutual inverses
v_of_tau = wc * R / mm
tau_of_v = sp.solve(sp.Eq(v_of_tau, vv), tau)[0]
print("tau_bind =", tau_of_v)
identity(tau_of_v, sp.pi * R / (4 * mm * vv),
         domain={"R": (1.0, 20.0), "mm": (1.0, 10.0), "vv": (1.0, 50.0)})
identity(v_of_tau.subs(tau, tau_of_v), vv,
         domain={"R": (1.0, 20.0), "mm": (1.0, 10.0), "vv": (1.0, 50.0)})

pi = float(sp.pi)
print("\n(i) bandwidth at tau = 40 ms:")
wc40 = pi / 4 / 0.040
print(f"   w_c = {wc40:.4f} rad/s = {wc40/(2*pi):.4f} Hz (claimed 19.63 rad/s, 3.12 Hz)")
quantity(f"{wc40:.5f} rad/s", "19.63 rad/s", rel_tol=1e-3)
quantity(f"{wc40/(2*pi):.5f} Hz", "3.12 Hz", rel_tol=2e-3)

print("\n(ii) speed cap v = w_c R / m, R = 5 m:")
for tau_v, m_v, want in ((0.040, 5, 19.6), (0.040, 3, 32.7), (0.130, 5, 6.0), (0.130, 3, 10.1)):
    v = (pi / 4 / tau_v) * 5.0 / m_v
    print(f"   tau = {tau_v*1000:5.0f} ms, m = {m_v}: v = {v:6.2f} m/s (claimed {want})")
    quantity(f"{v:.5f} m/s", f"{want} m/s", rel_tol=1.2e-2)

print("\n(iii) latency that would make the bound bind, R = 5 m:")
for v_v, m_v, want in ((7.0, 5, 112.0), (7.0, 3, 187.0), (10.0, 5, 79.0), (10.0, 3, 131.0)):
    tb = pi / 4 * 5.0 / (m_v * v_v)
    print(f"   v = {v_v:4.1f} m/s, m = {m_v}: tau = {tb*1000:6.1f} ms (claimed {want})")
    quantity(f"{tb*1000:.4f} ms", f"{want} ms", rel_tol=6e-3)

units("19.635 rad/s", "1/s")
units("19.63 rad/s * 5 m", "m/s")
units("3.1416/4 * 5 m / (3 * 7 m/s)", "s")

raise SystemExit(finish())
