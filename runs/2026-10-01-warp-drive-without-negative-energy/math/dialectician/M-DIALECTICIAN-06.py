"""M-DIALECTICIAN-06: flat cavity metric ds^2 = -alpha^2 dt^2 + (dx + b dt)^2 + dy^2 + dz^2 (c = 1), alpha, b constant.
Claims: Eulerian (u_i = 0) observers move at b/alpha relative to static (Killing) observers; = 0.026 c at b = 0.02,
alpha = 0.761; they cross 2R1 = 20 m in 3.3 us of Killing time; a static payload's clock runs slow by
1 - sqrt(1 - (b/alpha)^2) = 3.4e-4 relative to the same shell without shift, ~1.1e4 s per year.
"""
import sys, os
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from math_checks import identity, limit, quantity, units, finish
from tovshell import shell

al, b = sp.symbols("alpha b", positive=True)
g = sp.Matrix([[-al**2 + b**2, b, 0, 0], [b, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = g.inv()
n_low = sp.Matrix([-al, 0, 0, 0])
n_up = gi * n_low
print("n^mu =", list(sp.simplify(n_up)), " n.n =", sp.simplify((n_low.T * n_up)[0]))
# u_i = 0 means u_x = 0 lower: n has lower components (-alpha,0,0,0) -> it is the u_i = 0 observer
us_up = sp.Matrix([1, 0, 0, 0]) / sp.sqrt(al**2 - b**2)
identity(sp.simplify((us_up.T * g * us_up)[0]), -1, domain={"b": (0, 0.5), "alpha": (0.6, 1)})
gam = sp.simplify(-(us_up.T * g * n_up)[0])
vrel = sp.sqrt(1 - 1 / gam**2)
identity(sp.simplify(vrel), b / al, domain={"b": (0, 0.5), "alpha": (0.6, 1)})
# coordinate velocity of Eulerian observer
identity(sp.simplify(n_up[1] / n_up[0]), -b)
# static clock rate with and without shift
deficit = 1 - sp.sqrt(al**2 - b**2) / al
identity(deficit, 1 - sp.sqrt(1 - (b / al) ** 2), domain={"b": (0, 0.5), "alpha": (0.6, 1)})
limit(deficit, "b", 0, 0, domain={"alpha": (0.6, 1)})
# also: the cavity metric has constant coefficients -> flat -> static observers are geodesic (Christoffels vanish)
alpha_in = shell(4.49e27, 10.0, 20.0)["alpha_in"]
bb = 0.02
v = bb / alpha_in
cross = 20.0 / (bb * 2.99792458e8)
d = 1 - (1 - v**2) ** 0.5
print(f"alpha_in = {alpha_in:.5f}: b/alpha = {v:.5f} c; Killing-time crossing of 20 m = {cross:.4e} s; "
      f"local (static-frame) crossing = {20.0/(v*2.99792458e8):.4e} s; deficit = {d:.4e}; per Julian year = {d*3.15576e7:.4e} s")
quantity(f"{v}", "0.026", rel_tol=2e-2)
quantity(f"20 m/({bb}*c)", "3.3e-6 s", rel_tol=2e-2)
quantity(f"{d}", "3.4e-4", rel_tol=2e-2)
quantity(f"{d}*3.15576e7 s", "1.1e4 s", rel_tol=3e-2)
units("20 m/(0.02*c)", "s")
raise SystemExit(finish())
