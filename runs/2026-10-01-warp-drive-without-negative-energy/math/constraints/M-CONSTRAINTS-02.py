"""M-CONSTRAINTS-02: Natario zero-expansion drive energy (F2).

Geometric units. N = 1, flat slices, shift X = v curl((f/2)(-y, x, 0)), f the tanh top hat
(Delta = 2/s). theta = div X = 0 identically, so rho_E = -K_ij K_ij/(16 pi) <= 0 with
K_ij = (d_i X_j + d_j X_i)/2. Own derivation of K.K in spherical coordinates, own quadrature.
Claims: paper-like (R = 1, Delta = 0.25, v = 1) E = -3.288 m; reference (R = 100, Delta = 1,
v = 10) E = -4.4455e8 m = -5.99e35 kg = -3.0e5 Msun; E/(v^2 R^4/Delta^3) = -0.04446; ratio to
Alcubierre -5.5556e4 m is 8.0e3.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, sign, quantity, units, finish

x, y, z = sp.symbols("x y z", real=True)
v = sp.symbols("v", positive=True)
f = sp.Function("f")
r = sp.sqrt(x**2 + y**2 + z**2)
A = [-y * f(r) / 2, x * f(r) / 2, 0]
Xs = [x, y, z]
curl = [sp.diff(A[2], y) - sp.diff(A[1], z), sp.diff(A[0], z) - sp.diff(A[2], x), sp.diff(A[1], x) - sp.diff(A[0], y)]
Xv = [v * c for c in curl]
div = sum(sp.diff(Xv[i], Xs[i]) for i in range(3))
identity(sp.simplify(div), 0)   # theta = 0 exactly
K = sp.Matrix(3, 3, lambda i, j: (sp.diff(Xv[j], Xs[i]) + sp.diff(Xv[i], Xs[j])) / 2)
KK = sum(K[i, j]**2 for i in range(3) for j in range(3))
# flat limit: f = 1 gives X = v z-hat, K = 0
Kconst = K.subs(f(r), 1).doit()
identity(sp.simplify(sum(Kconst[i, j]**2 for i in range(3) for j in range(3))), 0)
# replace f and derivatives by symbols, then go spherical
f0, f1, f2, f3 = sp.symbols("f0 f1 f2 f3", real=True)
rr, th, ph = sp.symbols("rr th ph", positive=True)
KKs = KK.doit()
subsd = {}
KKs = KKs.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.doit())
derivs = sorted(KKs.atoms(sp.Derivative), key=lambda d: -d.derivative_count)
for d in derivs:
    n = d.derivative_count
    KKs = KKs.subs(d, [f1, f2, f3][n - 1])
KKs = KKs.subs(f(r), f0)
KKsph = sp.simplify(KKs.subs({x: rr * sp.sin(th) * sp.cos(ph), y: rr * sp.sin(th) * sp.sin(ph), z: rr * sp.cos(th)}))
print("K.K (spherical) =", KKsph)
assert ph not in KKsph.free_symbols or sp.simplify(sp.diff(KKsph, ph)) == 0
KKfun = sp.lambdify((rr, th, f1, f2, v), KKsph.subs(ph, 0), "numpy")

def profile_derivs(q, R, s):
    T = np.tanh
    sech2 = lambda w: 1 / np.cosh(w)**2
    n = 2 * np.tanh(s * R)
    d1 = (s * sech2(s * (q + R)) - s * sech2(s * (q - R))) / n
    d2 = (-2 * s**2 * sech2(s * (q + R)) * T(s * (q + R)) + 2 * s**2 * sech2(s * (q - R)) * T(s * (q - R))) / n
    return d1, d2

def energy(R, s, vv, nr=1200, nt=400):
    lo = max(R - 25 / s, 1e-6)
    segs = np.linspace(lo, R + 25 / s, 41)
    gr, gw = np.polynomial.legendre.leggauss(nr // 40)
    rs, ws = [], []
    for a, b in zip(segs[:-1], segs[1:]):
        rs.append((b - a) / 2 * gr + (a + b) / 2); ws.append((b - a) / 2 * gw)
    if lo > 1e-6:
        a, b = 1e-6, lo
        rs.append((b - a) / 2 * gr + (a + b) / 2); ws.append((b - a) / 2 * gw)
    rs, ws = np.concatenate(rs), np.concatenate(ws)
    tg, tw = np.polynomial.legendre.leggauss(nt)
    thg, thw = (tg + 1) * np.pi / 2, tw * np.pi / 2
    Rg, Tg = np.meshgrid(rs, thg, indexing="ij")
    d1, d2 = profile_derivs(Rg, R, s)
    rho = -KKfun(Rg, Tg, d1, d2, vv) / (16 * np.pi)
    dV = 2 * np.pi * Rg**2 * np.sin(Tg) * np.outer(ws, thw)
    return float(np.sum(rho * dV)), float(np.max(rho))

E1, m1 = energy(1.0, 8.0, 1.0)
E1b, _ = energy(1.0, 8.0, 1.0, nr=1800, nt=600)
E2, m2 = energy(100.0, 2.0, 10.0)
E2b, _ = energy(100.0, 2.0, 10.0, nr=1800, nt=600)
print("paper-like E =", E1, E1b, "max rho", m1)
print("reference E =", E2, E2b, "max rho", m2, " fit coeff", E2 / (100 * 100**4 / 1.0))
quantity(f"{E1} m", "-3.288 m", rel_tol=2e-3)
quantity(f"{E2} m", "-4.4455e8 m", rel_tol=1e-3)
quantity(f"{E2 / 1e10}", "-0.04446", rel_tol=2e-3)
# thinner wall: coefficient should converge (scaling v^2 R^4/Delta^3)
E3, _ = energy(1000.0, 2.0, 1.0)
print("R = 1000, Delta = 1 coeff", E3 / (1000.0**4))
quantity(f"{E3 / 1000.0**4}", "-0.0445", rel_tol=5e-3)
quantity(f"{E2 / -55556.0}", "8.0e3", rel_tol=5e-3)
quantity(f"{-E2} m * c^2/G", "5.99e35 kg", rel_tol=3e-3)
quantity(f"{-E2} m * c^4/G", "5.38e52 J", rel_tol=3e-3)
quantity(f"{-E2} m * c^2/G", "3.0e5 Msun", rel_tol=1e-2)
quantity(f"{-E1} m * c^2/G", "4.43e27 kg", rel_tol=3e-3)
quantity(f"{-E1} m * c^2/G", "2.23e-3 Msun", rel_tol=5e-3)
sign(-KKsph.subs({f1: sp.Symbol("a", real=True), f2: sp.Symbol("b", real=True), ph: 0}) / (16 * sp.pi), "nonpositive",
     domain={"rr": (0.1, 10), "th": (0, 3.14159), "a": (-10, 10), "b": (-10, 10), "v": (0.1, 10)})
units("1 m * c^2/G", "kg")
raise SystemExit(finish())
