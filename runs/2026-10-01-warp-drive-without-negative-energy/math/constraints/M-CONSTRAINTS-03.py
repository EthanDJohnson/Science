"""M-CONSTRAINTS-03: divergence identity and zero total Eulerian energy for curl-free shifts (F3).

Geometric units, N = 1, flat slices, rho_E = (theta^2 - K_ij K_ij)/(16 pi), K_ij = (d_i X_j + d_j X_i)/2.
Claim (a): theta^2 - d_i X_j d_j X_i = d_i(X_i theta) - d_j(X_i d_i X_j) for any C^2 X.
Claim (b): curl X = 0 => K_ij K_ij = d_i X_j d_j X_i, so rho_E is a divergence and int rho_E = 0
for X decaying faster than r^(-1/2) (surface term ~ r^2 * X dX ~ r^(1-2a)).
Claim (c): proxy X = v grad(z f), tanh top hat: reference (R = 100, Delta = 1, v = 10)
E_- = -1.667e7 m, E_+ = -E_-; paper-like E_- = -2.8576 m.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

x, y, z = sp.symbols("x y z", real=True)
Xs = [x, y, z]
X = [sp.Function(n)(x, y, z) for n in ("X1", "X2", "X3")]
th = sum(sp.diff(X[i], Xs[i]) for i in range(3))
lhs = th**2 - sum(sp.diff(X[j], Xs[i]) * sp.diff(X[i], Xs[j]) for i in range(3) for j in range(3))
rhs = sum(sp.diff(X[i] * th, Xs[i]) for i in range(3)) - sum(
    sp.diff(sum(X[i] * sp.diff(X[j], Xs[i]) for i in range(3)), Xs[j]) for j in range(3))
print("identity residual:", sp.simplify(sp.expand(lhs - rhs)))
identity(sp.expand(lhs - rhs), 0)
# (b) curl-free: X = grad Phi
Phi = sp.Function("Phi")(x, y, z)
Xg = [sp.diff(Phi, q) for q in Xs]
Kg = sp.Matrix(3, 3, lambda i, j: (sp.diff(Xg[j], Xs[i]) + sp.diff(Xg[i], Xs[j])) / 2)
cross = sum(sp.diff(Xg[j], Xs[i]) * sp.diff(Xg[i], Xs[j]) for i in range(3) for j in range(3))
identity(sp.expand(sum(Kg[i, j]**2 for i in range(3) for j in range(3)) - cross), 0)
# surface term falloff: X ~ r^-a, V ~ r^(-2a-1), flux ~ r^(1-2a) -> 0 iff a > 1/2
rr, a = sp.symbols("rr a", positive=True)
limit("rr**(1 - 2*a)", "rr", "oo", "0", domain={"a": (0.51, 5)})

# (c) explicit proxy Phi = v z f(r)
v = sp.symbols("v", positive=True)
f0, f1, f2, f3 = sp.symbols("f0 f1 f2 f3", real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
F = sp.Function("F")
P = v * z * F(r)
H = sp.hessian(P, Xs).doit()
rho = (H.trace()**2 - sum(H[i, j]**2 for i in range(3) for j in range(3))) / (16 * sp.pi)
rho = rho.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.doit())
for d in sorted(rho.atoms(sp.Derivative), key=lambda d: -d.derivative_count):
    rho = rho.subs(d, [f1, f2, f3][d.derivative_count - 1])
rho = rho.subs(F(r), f0)
R_, t_ = sp.symbols("R_ t_", positive=True)
rs = sp.simplify(rho.subs({x: R_ * sp.sin(t_), y: 0, z: R_ * sp.cos(t_)}))
print("rho_E(r, theta) =", rs)
fn = sp.lambdify((R_, t_, f0, f1, f2, v), rs, "numpy")

def derivs(q, R, s):
    sech2 = lambda w: 1 / np.cosh(np.clip(w, -300, 300))**2
    T = np.tanh
    n = 2 * np.tanh(s * R)
    d0 = (T(s * (q + R)) - T(s * (q - R))) / n
    d1 = (s * sech2(s * (q + R)) - s * sech2(s * (q - R))) / n
    d2 = (-2 * s**2 * sech2(s * (q + R)) * T(s * (q + R)) + 2 * s**2 * sech2(s * (q - R)) * T(s * (q - R))) / n
    return d0, d1, d2

def parts(R, s, vv, nr=1600, nt=500):
    lo = max(R - 25 / s, 1e-6)
    edges = list(np.linspace(lo, R + 25 / s, 41))
    if lo > 1e-6:
        edges = [1e-6] + edges
    gr, gw = np.polynomial.legendre.leggauss(40)
    rs_, ws = [], []
    for A, B in zip(edges[:-1], edges[1:]):
        rs_.append((B - A) / 2 * gr + (A + B) / 2); ws.append((B - A) / 2 * gw)
    rs_, ws = np.concatenate(rs_), np.concatenate(ws)
    tg, tw = np.polynomial.legendre.leggauss(nt)
    thg, thw = (tg + 1) * np.pi / 2, tw * np.pi / 2
    Rg, Tg = np.meshgrid(rs_, thg, indexing="ij")
    d0, d1, d2 = derivs(Rg, R, s)
    rh = fn(Rg, Tg, d0, d1, d2, vv)
    dV = 2 * np.pi * Rg**2 * np.sin(Tg) * np.outer(ws, thw)
    return float(np.sum(np.minimum(rh, 0) * dV)), float(np.sum(np.maximum(rh, 0) * dV))

Em, Ep = parts(100.0, 2.0, 10.0)
print("reference E- =", Em, " E+ =", Ep, " (E+ + E-)/|E-| =", (Ep + Em) / abs(Em))
Em1, Ep1 = parts(1.0, 8.0, 1.0)
print("paper-like E- =", Em1, " E+ =", Ep1, " rel =", (Ep1 + Em1) / abs(Em1))
quantity(f"{Em} m", "-1.667e7 m", rel_tol=2e-3)
quantity(f"{Em1} m", "-2.8576 m", rel_tol=2e-3)
quantity(f"{abs(Ep + Em) / abs(Em) + 1}", "1", rel_tol=1e-5)
quantity(f"{abs(Ep1 + Em1) / abs(Em1) + 1}", "1", rel_tol=1e-4)
quantity(f"{-Em} m * c^2/G", "2.25e34 kg", rel_tol=3e-3)
quantity(f"{-Em} m * c^2/G", "1.13e4 Msun", rel_tol=5e-3)
units("1 m * c^2/G", "kg")
raise SystemExit(finish())
