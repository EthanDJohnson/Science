"""M-DECOMPOSER-10: a long throat (T_thru = tau > d/c) carries no achronal null geodesic through it (L7, Graham-Olum p. 5-6).

Same toy model as M-DECOMPOSER-08 (flat exterior, point mouths A = 0, B = d e, forward throat delay tau,
relative mouth rotation R, c = 1). For the points p = A - Lp u (before entry) and q = B + Lq R u (after exit)
the time difference along the geodesic is tau + Lp + Lq and the exterior straight-line separation is
D = |d e + Lp u + Lq R u|. As Lp, Lq -> 0, D - (tau + Lp + Lq) -> d - tau < 0 whatever u and R are:
q lies in the chronological future of p through the exterior, so every throat-crossing line is chronal.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import limit, sign, inequality, finish

Lp, Lq, d, tau = sp.symbols("Lp Lq d tau", positive=True)
a1, a2, a3, b1, b2, b3 = sp.symbols("a1 a2 a3 b1 b2 b3", real=True)  # u and R u components (unit vectors)
D = sp.sqrt((d + Lp * a1 + Lq * b1)**2 + (Lp * a2 + Lq * b2)**2 + (Lp * a3 + Lq * b3)**2)
margin = D - tau - Lp - Lq
m0 = margin.subs(Lq, 0)
limit(m0, "Lp", 0, d - tau, domain={"a1": (-1, 1), "a2": (-1, 1), "a3": (-1, 1)})
# for a long throat, tau = d + delta with delta > 0, the short-range margin is negative
delta = sp.symbols("delta", positive=True)
sign((d - tau).subs(tau, d + delta), "negative")
# triangle bound: D <= d + Lp + Lq for unit u, Ru, so the margin is <= d - tau < 0 at every Lp, Lq (not only near the mouths)
th1, ph1, th2, ph2 = sp.symbols("th1 ph1 th2 ph2", real=True)
sub = {a1: sp.sin(th1) * sp.cos(ph1), a2: sp.sin(th1) * sp.sin(ph1), a3: sp.cos(th1),
       b1: sp.sin(th2) * sp.cos(ph2), b2: sp.sin(th2) * sp.sin(ph2), b3: sp.cos(th2)}
inequality(D.subs(sub), "<=", d + Lp + Lq,
           domain={"th1": (0, 3.14159), "ph1": (0, 6.28318), "th2": (0, 3.14159), "ph2": (0, 6.28318)})
raise SystemExit(finish())
