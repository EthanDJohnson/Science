#!/usr/bin/env python3
"""M-MECH-01  Stop look-ahead bound, braking acceleration from thrust-to-weight, crossing speeds.

CLAIM (mechanist finding 1, candidate MECH-REFRAME)
  Symbols, SI: g = 9.81 m/s^2 standard gravity; W = T_max/(m g) thrust-to-weight ratio (W > 1);
  a_h = maximum sustained horizontal acceleration of a quadrotor in level flight [m/s^2];
  v = forward speed [m/s]; tau = sensing-plus-compute transport latency [s]; s = usable
  perception range [m]; s_req = look-ahead distance needed to stop before a static obstacle [m].
  Assumptions: point mass, thrust along body z, altitude held (T cos(theta) = m g), constant
  braking at a_h after a dead time tau, single static obstacle, no estimation error.
  Claimed:  (i)  a_h = g sqrt(W^2 - 1), = 42.0 m/s^2 at W = 4.4;
            (ii) s_req = v tau + v^2/(2 a_h), = 0.93 m at v = 7 m/s, tau = 50 ms
                 and 1.33 m at tau = 107 ms;
            (iii) the crossing speed where s_req = s is v* = a(sqrt(tau^2 + 2 s/a) - tau),
                 = 12.0 m/s at s = 3 m, 18.4 m/s at s = 6 m, 24.9 m/s at s = 10 m
                 (a = 42.0 m/s^2, tau = 107 ms);
            (iv) d ln a_h/d ln W = W^2/(W^2 - 1) = 1.07 at W = 4.
  Derived independently below from the tilt geometry and the kinematics; the lens's scripts are
  not read or imported.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

G = 9.81  # m/s^2

# ---------------------------------------------------------------- (i) tilt geometry
# Level flight with thrust T = W m g tilted theta from vertical:
#   vertical:   T cos(theta) = m g      ->  cos(theta) = 1/W
#   horizontal: m a = T sin(theta)      ->  a = g W sin(theta) = g tan(theta) = g sqrt(W^2-1)
W, g_s = sp.symbols("W g_s", positive=True)
theta = sp.acos(1 / W)
a_from_geom = g_s * W * sp.sin(theta)
identity(sp.simplify(a_from_geom), g_s * sp.sqrt(W**2 - 1), domain={"W": (1.001, 20), "g_s": (1, 20)})
identity(g_s * sp.tan(theta), g_s * sp.sqrt(W**2 - 1), domain={"W": (1.001, 20), "g_s": (1, 20)})

a_h44 = G * (4.4**2 - 1) ** 0.5
a_h462 = G * (4.6211**2 - 1) ** 0.5   # 4*8.5 N / (0.75 kg * 9.81) = 4.621, Sun et al. TABLE II
print(f"inputs: g = {G} m/s^2, W = 4.4 and 4.621")
print(f"a_h(W=4.4)   = {a_h44:.3f} m/s^2")
print(f"a_h(W=4.621) = {a_h462:.3f} m/s^2")
quantity(f"{a_h44:.6f} m/s^2", "42.0 m/s^2", rel_tol=2e-3)
units("9.81 m/s^2 * 4.28", "acceleration")

# W -> 1 (hover-only thrust) must give zero horizontal acceleration
limit(g_s * sp.sqrt(W**2 - 1), "W", 1, 0)
# large W: a_h -> g W
limit(g_s * sp.sqrt(W**2 - 1) / (g_s * W), "W", "oo", 1)

# ---------------------------------------------------------------- (ii) required look-ahead
v, tau, s, a = sp.symbols("v tau s a", positive=True)
s_req = v * tau + v**2 / (2 * a)
for vv, tt in ((7.0, 0.050), (7.0, 0.107)):
    val = float(s_req.subs({v: vv, tau: tt, a: a_h44}))
    print(f"s_req(v={vv} m/s, tau={tt*1e3:.0f} ms, a={a_h44:.2f} m/s^2) = {val:.4f} m")
quantity(f"{float(s_req.subs({v: 7.0, tau: 0.050, a: a_h44})):.6f} m", "0.93 m", rel_tol=5e-3)
quantity(f"{float(s_req.subs({v: 7.0, tau: 0.107, a: a_h44})):.6f} m", "1.33 m", rel_tol=5e-3)
units("7 m/s * 0.107 s + (7 m/s)^2/(2 * 42 m/s^2)", "length")

# ---------------------------------------------------------------- (iii) crossing speed
v_star = a * (sp.sqrt(tau**2 + 2 * s / a) - tau)
# it must invert the bound exactly:  s_req(v_star) == s
identity(sp.simplify(s_req.subs(v, v_star)), s,
         domain={"a": (1, 100), "tau": (0.0, 1.0), "s": (0.1, 50)})
# zero-latency limit: v* -> sqrt(2 a s)
limit(v_star, "tau", 0, sp.sqrt(2 * a * s))
# zero-range limit: v* -> 0
limit(v_star, "s", 0, 0)
for ss, want in ((3.0, "12.0 m/s"), (6.0, "18.4 m/s"), (10.0, "24.9 m/s")):
    val = float(v_star.subs({a: a_h44, tau: 0.107, s: ss}))
    print(f"v*(s={ss} m, tau=107 ms, a={a_h44:.2f} m/s^2) = {val:.3f} m/s   (lens: {want})")
    quantity(f"{val:.6f} m/s", want, rel_tol=5e-3)
# v* = a * (time), and the radicand of the root is a time squared:
units("42 m/s^2 * 0.438 s", "m/s")
units("(0.107 s)^2 + 2 * 6 m/(42 m/s^2)", "s^2")

# ---------------------------------------------------------------- (iv) elasticity of a_h in W
ela = sp.simplify(W * sp.diff(sp.sqrt(W**2 - 1), W) / sp.sqrt(W**2 - 1))
identity(ela, W**2 / (W**2 - 1), domain={"W": (1.001, 20)})
print(f"d ln a_h/d ln W at W = 4   : {float(ela.subs(W, 4)):.4f}  (lens: 1.07)")
print(f"d ln a_h/d ln W at W = 4.4 : {float(ela.subs(W, 4.4)):.4f}")
quantity(f"{float(ela.subs(W, 4)):.6f} m", "1.0667 m", rel_tol=5e-3)

raise SystemExit(finish())
