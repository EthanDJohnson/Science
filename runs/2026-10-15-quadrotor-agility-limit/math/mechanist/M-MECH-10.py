#!/usr/bin/env python3
"""M-MECH-10  Where the latency term and the braking term of the look-ahead budget cross.

CLAIM (mechanist finding 11, candidate MECH-C)
  Symbols: v speed [m/s]; tau effective sensing-plus-blind latency [s]; a braking acceleration
  [m/s^2]. The look-ahead budget is s_req = v tau + v^2/(2 a); its two terms are equal at
  v* = 2 a tau. Claimed: 3.4 m/s for (a = 42 m/s^2, tau = 40 ms), 9.0 m/s at tau = 107 ms,
  4.9 m/s for the FoV-capped a = 16.3 m/s^2 at tau_eff = 150 ms; above v* the perceived volume
  dominates, below it latency does.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

v, tau, a = sp.symbols("v tau a", positive=True)
sol = sp.solve(sp.Eq(v * tau, v**2 / (2 * a)), v)
print("solutions of v tau = v^2/(2a):", sol)
identity(sol[0], 2 * a * tau, domain={"a": (1, 100), "tau": (0.01, 1)})
# above v*, the braking term exceeds the latency term
ratio = (v**2 / (2 * a)) / (v * tau)
# above v* = 2 a tau the braking term exceeds the latency term: substitute v = 2 a tau (1 + x)
x = sp.symbols("x", positive=True)
inequality(ratio.subs(v, 2 * a * tau * (1 + x)), ">", 1,
           domain={"a": (1, 100), "tau": (0.01, 1), "x": (1e-6, 100)})
identity(sp.simplify(ratio), v / (2 * a * tau), domain={"a": (1, 100), "tau": (0.01, 1), "v": (0.1, 100)})
limit(ratio, "v", 0, 0)                       # at low speed the dead time dominates
# (the v -> oo divergence is immediate and left out: SymPy returns oo and the comparison is undecided)
units("2 * 42 m/s^2 * 0.107 s", "m/s")

for av, tv, want in ((42.034448, 0.040, "3.4 m/s"), (42.034448, 0.107, "9.0 m/s"),
                     (16.3266, 0.150, "4.9 m/s")):
    vs = 2 * av * tv
    print(f"a = {av:7.3f} m/s^2, tau = {tv*1e3:5.1f} ms -> v* = {vs:6.3f} m/s   (lens: {want})")
    quantity(f"{vs:.6f} m/s", want, rel_tol=1.5e-2)

raise SystemExit(finish())
