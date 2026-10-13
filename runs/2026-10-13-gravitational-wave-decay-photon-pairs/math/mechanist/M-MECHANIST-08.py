"""M-MECHANIST-08 (and M-MECHANIST-09): kinematics (natural units, c = 1, metric +---).

Two gravitons of energy w each, opening angle th in [0, pi]: K = k1 + k2, s = K^2 = 2 w^2 (1 - cos th)
= 4 w^2 sin^2(th/2); k1 - k2 has (k1 - k2)^2 = -2 w^2 (1 - cos th) <= 0 (M-09).
ULDM (M-08): pair of scalars of mass m needs s >= 4 m^2, i.e. sin(th/2) >= m/w. In the resonant window
w <= m (1 + v^2/2) (v the DM speed, 0 < v << 1) this forces pi - th <= ~2 v.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, series, inequality, finish

w, th, v, m = sp.symbols("w theta v m", positive=True)
k1 = sp.Matrix([w, 0, 0, w])
k2 = sp.Matrix([w, w * sp.sin(th), 0, w * sp.cos(th)])
eta = sp.diag(1, -1, -1, -1)
sq = lambda a: (a.T * eta * a)[0]
identity(sp.simplify(sq(k1 + k2)), 2 * w**2 * (1 - sp.cos(th)))
identity(2 * w**2 * (1 - sp.cos(th)), 4 * w**2 * sp.sin(th / 2) ** 2)
sign(sp.simplify(sq(k1 - k2)), "nonpositive", domain={"w": (0.1, 10), "theta": (0, 3.14159)})
# ULDM threshold at the window edge w = m (1 + v^2/2): th_min solves sin(th/2) = 1/(1 + v^2/2).
# delta = pi - th_min; cos(delta/2) = 1/(1 + v^2/2) -> delta = 2 acos(1/(1+v^2/2)) = 2 v + O(v^3)
delta = 2 * sp.acos(1 / (1 + v**2 / 2))
series(delta, "v", 0, 3, 2 * v)
# Inside the window (w smaller) the allowed cone is narrower: delta(w) = 2 acos(m/w) increases with w
inequality(2 * sp.acos(1 / (1 + v**2 / 2)), "<=", "2.0001*v", domain={"v": (1e-4, 3e-2)})
raise SystemExit(finish())
