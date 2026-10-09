"""M-CONSTRAINTS-06 (F6). Linear stability of the Schwarzschild thin-shell wormhole.
Equation of motion: sigma = -(1/2 pi a) sqrt(A + adot^2)  =>  adot^2 + V(a) = 0, V = A(a) - (2 pi sigma a)^2.
Conservation: d sigma/da = -(2/a)(sigma + P), dP/d sigma = beta^2. Stable iff V''(a0) > 0.
Claims: critical beta^2 = 3.5 (stable above) at 2.5M; -1.75 at 4M, -0.79 at 10 km (M = 1476.6 m), -0.5 flat
(stable below); sign flip/divergence at 3M."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

a, M, b2, a0 = sp.symbols("a M beta2 a0", positive=True)
s0, p0 = sp.symbols("s0 p0", real=True)
A = 1 - 2 * M / a
# Taylor data of sigma(a) about a0 from conservation + EoS
sig = sp.Function("sig")(a); P = sp.Function("P")(a)
d1 = -(2 / a) * (sig + P)
dP1 = b2 * d1
d2 = sp.diff(d1, a).subs(sp.Derivative(sig, a), d1).subs(sp.Derivative(P, a), dP1)
V = A - (2 * sp.pi * sig * a)**2
V1 = sp.diff(V, a).subs(sp.Derivative(sig, a), d1)
V2 = sp.diff(sp.diff(V, a), a)
V2 = V2.subs(sp.Derivative(sig, (a, 2)), d2).subs(sp.Derivative(sig, a), d1).subs(sp.Derivative(P, a), dP1)
Aa = 1 - 2 * M / a0
sub = {sig: -sp.sqrt(Aa) / (2 * sp.pi * a0), P: (1 - M / a0) / (4 * sp.pi * a0 * sp.sqrt(Aa)), a: a0}
V0 = sp.simplify(V.subs(sub)); V1v = sp.simplify(V1.subs(sub)); V2v = sp.simplify(V2.subs(sub))
identity(V0, sp.Integer(0), domain={"M": (0.1, 1), "a0": (2.5, 10)})
identity(V1v, sp.Integer(0), domain={"M": (0.1, 1), "a0": (2.5, 10)})
crit = sp.simplify(sp.solve(sp.Eq(V2v, 0), b2)[0])
coef = sp.simplify(sp.diff(V2v, b2))
print("V'' =", sp.factor(V2v))
print("critical beta^2 =", sp.factor(crit), "; dV''/dbeta^2 =", sp.factor(coef))
xx = sp.symbols("x", positive=True)
pv = -(1 - 3 * xx + 3 * xx**2) / (2 * (1 - 2 * xx) * (1 - 3 * xx))   # Poisson-Visser 1995 form, x = M/a0
identity(sp.simplify(crit.subs(M, xx * a0)), pv, domain={"x": (0.01, 0.32), "a0": (0.1, 10)})
limit(pv, "x", 0, "-1/2")
for xv, cl in [(sp.Rational(2, 5), 3.5), (sp.Rational(1, 4), -1.75), (sp.Float(1476.6 / 1e4), -0.79)]:
    v = float(pv.subs(xx, xv)); c = float(sp.diff(V2v, b2).subs({M: xv, a0: 1}))
    print(f"x={float(xv):.5f}: crit beta^2 = {v:.4f} (claimed {cl}); dV''/dbeta^2 = {c:.4f} -> stable for beta^2 {'>' if c > 0 else '<'} crit")
    identity(sp.Float(round(v, 2)), sp.Float(cl))
raise SystemExit(finish())
