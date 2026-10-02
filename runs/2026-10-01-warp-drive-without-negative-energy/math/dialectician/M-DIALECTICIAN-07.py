"""M-DIALECTICIAN-07: one-way light-time difference across the cavity, ds^2 = -alpha^2 dt^2 + (dx + b dt)^2.
Null rays: dx/dt = -b ± alpha. Over a proper length L (flat cavity, h = delta), t_minus - t_plus = L/(alpha-b) - L/(alpha+b)
= 2 L b/(alpha^2 - b^2) (Killing time, c = 1). Claim: 4.5–4.6 ns for L = 20 m, b = 0.02, alpha = 0.761–0.769.
"""
import sys, os
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from math_checks import identity, limit, quantity, units, finish
from tovshell import shell

al, b, L, w = sp.symbols("alpha b L w", positive=True)
roots = sp.solve(sp.Eq(-al**2 + (w + b) ** 2, 0), w)
print("null coordinate speeds:", roots)
dt = L / (al - b) - L / (al + b)
identity(sp.simplify(dt), 2 * L * b / (al**2 - b**2), domain={"b": (0, 0.5), "alpha": (0.6, 1)})
limit(dt, "b", 0, 0, domain={"alpha": (0.6, 1)})
c = 2.99792458e8
for a in (shell(4.49e27, 10.0, 20.0)["alpha_in"], shell(4.49e27, 10.0, 20.0, pressure=False)["alpha_in"]):
    val = 2 * 20.0 * 0.02 / (a**2 - 0.02**2) / c
    print(f"alpha = {a:.5f}: delta t = {val*1e9:.4f} ns (Killing time); static-observer proper time = {val*a*1e9:.4f} ns")
quantity(f"2*20 m*0.02/({shell(4.49e27, 10.0, 20.0)['alpha_in']}^2 - 0.02^2)/c", "4.6 ns", rel_tol=1e-2)
quantity(f"2*20 m*0.02/({shell(4.49e27, 10.0, 20.0, pressure=False)['alpha_in']}^2 - 0.02^2)/c", "4.5 ns", rel_tol=1e-2)
units("2*20 m*0.02/c", "s")
raise SystemExit(finish())
