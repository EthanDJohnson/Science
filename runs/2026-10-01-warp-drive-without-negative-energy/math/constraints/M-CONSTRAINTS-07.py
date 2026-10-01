"""M-CONSTRAINTS-07: light along the shift axis through the shell (F8; CONSTRAINTS-A, B).

Coordinates (ct, x, y, z) in m, comoving with the shell. On the x axis the toolkit metric reduces to
ds^2 = -e^{2a} dct^2 - 2 S beta dct dx + e^{2b} dx^2 (radial direction). Own derivation:
dx/dct = [S beta +- sqrt(S^2 beta^2 + e^{2a+2b})]/e^{2b}; interior (S = 1, b = 0) speeds sqrt(beta^2 + e^{2a}) +- beta.
Advance condition sqrt(beta^2 + e^{2a}) + beta > 1 <=> beta > (1 - e^{2a})/2.
Asymmetry dt_back - dt_fwd = 2 beta int S e^{-2a} dx (exact, linear in beta).
Metric functions a(r), b(r), S(r) from the toolkit rebuild (input).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, inequality, quantity, finish
from warp_shell import build_shell

bt, e2a, e2b, S = sp.symbols("beta e2a e2b S", positive=True)
fwd = (S * bt + sp.sqrt(S**2 * bt**2 + e2a * e2b)) / e2b
bwd = (-S * bt + sp.sqrt(S**2 * bt**2 + e2a * e2b)) / e2b    # speed magnitude backwards
# check null condition
u = sp.symbols("u")
null = -e2a - 2 * S * bt * u + e2b * u**2
identity(sp.simplify(null.subs(u, fwd)), 0)
identity(sp.simplify(null.subs(u, -bwd)), 0)
identity(sp.simplify(1 / bwd - 1 / fwd), 2 * S * bt / e2a)
# threshold
A = sp.symbols("A", positive=True)
inequality(sp.sqrt(bt**2 + A) + bt - 1, ">", 0, domain={"A": (0.1, 0.9), "beta": (0.5, 0.9)})
sol = sp.solve(sp.Eq(sp.sqrt(bt**2 + A) + bt, 1), bt)
print("threshold:", sol)
identity(sol[0], (1 - A) / 2, domain={"A": (0.1, 0.99)})

sh = build_shell(4.49e27, 10.0, 20.0)
ea = float(sh.lapse_static(0.0))
print("e^a(0) =", ea)
quantity(f"{ea}", "0.761", rel_tol=1e-3)
E2 = ea**2
for b_, vf, vb in ((0.04, 0.802, 0.722),):
    quantity(f"{np.sqrt(b_**2 + E2) + b_}", f"{vf}", rel_tol=1e-3)
    quantity(f"{np.sqrt(b_**2 + E2) - b_}", f"{vb}", rel_tol=1e-3)
quantity(f"{(1 - E2) / 2}", "0.210", rel_tol=3e-3)

c = 299792458.0
def times(beta, L=2000.0, n=400001):
    xs = np.linspace(-L, L, n)
    r = np.abs(xs)
    ea2 = sh.lapse_static(r)**2
    eb2 = sh.grr(r)
    Sx = sh.S(r)
    root = np.sqrt(Sx**2 * beta**2 + ea2 * eb2)
    dtf = eb2 / (root + Sx * beta)
    dtb = eb2 / (root - Sx * beta)
    tf = np.trapezoid(dtf, xs); tb = np.trapezoid(dtb, xs)
    return (tf - 2 * L) / c * 1e9, (tb - 2 * L) / c * 1e9
f04, b04 = times(0.04)
f02, b02 = times(0.02)
f30, _ = times(0.30)
f04L, b04L = times(0.04, L=4000.0, n=800001)
print(f"beta 0.04: fwd delay {f04:.2f} ns, back {b04:.2f} ns, diff {b04 - f04:.2f} ns; L=4000 diff {b04L - f04L:.2f}")
print(f"beta 0.02 diff {b02 - f02:.2f} ns; beta 0.30 fwd delay {f30:.2f} ns")
quantity(f"{f04}", "264.6", rel_tol=3e-3)
quantity(f"{b04}", "278.3", rel_tol=3e-3)
quantity(f"{b04 - f04}", "13.7", rel_tol=5e-3)
quantity(f"{b04L - f04L}", "13.7", rel_tol=5e-3)
quantity(f"{b02 - f02}", "6.9", rel_tol=1e-2)
quantity(f"{f30}", "228.9", rel_tol=3e-3)
# limit: beta -> 0 asymmetry vanishes
f0, b0 = times(0.0)
quantity(f"{b0 - f0 + 1}", "1", rel_tol=1e-9)
raise SystemExit(finish())
