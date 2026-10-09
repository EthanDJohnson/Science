"""M-CONSTRAINTS-17 ([CONSTRAINTS-F]). Given the quoted FGM 2018 transit t* = -(l^2/r_+) ln(|dV|/(2l)) (dossier Q-14,
taken as input) and a comparison path of half the boundary circle of -dt^2 + l^2 dphi^2 (light time pi l):
claim t* < pi l  <=>  |dV| > 2 l exp(-pi r_+/l)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, limit, finish

l, rp, X = sp.symbols("ell r_p X", positive=True)    # X = |dV|
tstar = -(l**2 / rp) * sp.log(X / (2 * l))
thr = 2 * l * sp.exp(-sp.pi * rp / l)
identity(tstar.subs(X, thr), sp.pi * l)          # equality exactly at threshold
dt = sp.simplify(sp.diff(tstar, X))
inequality(dt, "<", 0)                            # t* decreasing in |dV|: so t* < pi l iff X > threshold
# half boundary circle at speed of light: dt = l dphi over phi in [0, pi]
identity(sp.integrate(l, (sp.symbols("p"), 0, sp.pi)), sp.pi * l)
inequality(tstar.subs({X: sp.Rational(1, 10**12), l: 1, rp: 1}), ">", 20)   # tiny shift: very long transit
raise SystemExit(finish())
