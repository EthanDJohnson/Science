"""Independent check of the C6-2 finite-mouth line threshold and the 1.5a band.

Model (as stated in runs/2026-10-03-traversable-wormhole-shortcuts/calc/
falsifier-C6-2_finite_mouth_line.py.log, section 2): flat exterior, spherical
mouths of radius a, centres a distance d apart (D = d xhat), tube interior of
length L with geodesic length sqrt(L^2 + a^2 theta^2), gluing G in O(3).
Asymptotic through-line exists iff
    F_G(u;L) = min_{n,m} [a u.(n-m) + sqrt(L^2 + a^2 ang(n, G^T m)^2)] < D.u
for some unit u, with n.u <= 0 and m.u >= 0.

Reduction used here (not taken from the run's code): put m' = G^T m and
v = G^T u. Then u.m = v.m', the constraints are ang(n,-u) <= pi/2 and
ang(m',v) <= pi/2, and only Theta = ang(-u, v) matters. By the spherical
triangle inequality the minimum over (n, m') is
    g(Theta; lam) = min_{alpha,beta in [0,pi/2]}
        [-cos(alpha) - cos(beta) + sqrt(lam^2 + max(0, Theta-alpha-beta)^2)]
(lam = L/a), reached with n, m' on the great circle from -u to v.
g is non-decreasing in Theta, so the worst gluing is the one with
Theta = pi for every u, i.e. G^T u = u for all u (G = +I, the run's
"mirror"). Its threshold therefore bounds L*(G) from below for every G.
We also brute-force random O(3) gluings directly as a cross-check.
"""
import numpy as np
from scipy.optimize import brentq, minimize

rng = np.random.default_rng(20261027)


def g(Theta, lam, N=801):
    al = np.linspace(0.0, np.pi / 2, N)
    A, B = np.meshgrid(al, al, indexing="ij")
    gap = np.maximum(0.0, Theta - A - B)
    val = -np.cos(A) - np.cos(B) + np.sqrt(lam**2 + gap**2)
    i = np.unravel_index(np.argmin(val), val.shape)
    # local polish
    def obj(z):
        a_, b_ = np.clip(z, 0, np.pi / 2)
        return -np.cos(a_) - np.cos(b_) + np.sqrt(lam**2 + max(0.0, Theta - a_ - b_) ** 2)
    r = minimize(obj, [A[i], B[i]], method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-14})
    return min(val[i], r.fun)


d = 1.0
print("=== 1. Monotonicity of g(Theta) in Theta (lam = 11.6) ===")
Ths = np.linspace(0, np.pi, 13)
gs = [g(T, 11.6) for T in Ths]
for T, v in zip(Ths, gs):
    print(f"  Theta = {np.degrees(T):6.1f} deg : g = {v:.6f}")
print("  non-decreasing:", all(np.diff(gs) >= -1e-12))

print("\n=== 2. Thresholds from the reduction, a = 0.1 d (u = D-hat) ===")
for a in (0.1, 0.3, 0.01):
    for name, Th in (("aligned (Theta=0)", 0.0), ("worst  (Theta=pi)", np.pi)):
        Ls = brentq(lambda L: a * g(Th, L / a) - d, 0.5 * d, 2.0 * d, xtol=1e-12)
        print(f"  a = {a:<5} {name}: L* = {Ls:.4f} d ; (L*-d)/a = {(Ls-d)/a:.4f} ; band (pi a - (L*-d))/a = {np.pi-(Ls-d)/a:.4f}")


def ang(p, q):
    return np.arccos(np.clip(np.dot(p, q), -1, 1))


def unit(th, ph):
    return np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])


def F_direct(u, L, a, G, tries=12):
    # direct minimisation over n, m with hemisphere penalties (independent of the reduction)
    best = np.inf
    for _ in range(tries):
        z0 = rng.uniform([0, 0, 0, 0], [np.pi, 2 * np.pi, np.pi, 2 * np.pi])
        def obj(z):
            n = unit(z[0], z[1]); m = unit(z[2], z[3])
            pen = 1e3 * (max(0.0, np.dot(n, u)) ** 2 + max(0.0, -np.dot(m, u)) ** 2)
            return a * np.dot(u, n - m) + np.hypot(L, a * ang(n, G.T @ m)) + pen
        r = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 4000})
        best = min(best, r.fun)
    return best


def rand_O3():
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q * np.sign(np.diag(r))
    if rng.random() < 0.5:
        q = -q
    return q


print("\n=== 3. Direct brute force, a = 0.1 d, L = 1.16 d (just below the claimed worst L* = 1.1643 d) ===")
print("  a line must exist for every gluing if L*(G) >= 1.1643 d for all G")
a, L = 0.1, 1.16
e = np.array([1.0, 0, 0])
worst = np.inf
for k in range(25):
    G = rand_O3()
    # u along D maximises D.u; also try a few tilted u
    marg = min(F_direct(u, L, a, G, tries=6) - d * u[0]
               for u in [e] + [unit(np.pi / 2 - t, p) for t, p in rng.uniform([-0.3, -0.3], [0.3, 0.3], size=(3, 2))])
    worst = max(worst, marg) if np.isfinite(worst) else marg
    print(f"  G #{k:02d} det={np.linalg.det(G):+.0f}: best line margin F - D.u = {marg:+.5f} d")
for name, G in (("mirror G=+I", np.eye(3)), ("aligned G=-I", -np.eye(3))):
    print(f"  {name}: margin at L=1.16 d = {F_direct(e, 1.16, a, G) - d:+.5f} d ; at L=1.17 d = {F_direct(e, 1.17, a, G) - d:+.5f} d")
print(f"  largest (least negative) margin over the random gluings: {worst:+.5f} d (negative => line exists)")

print("\n=== 4. Worst-gluing band width (pi a - (L*-d)) / a versus a/d ===")
for a in (0.001, 0.01, 0.05, 0.09, 0.1, 0.11, 0.15, 0.2, 0.3):
    Ls = brentq(lambda L: a * g(np.pi, L / a) - d, 0.5 * d, 3.0 * d, xtol=1e-12)
    print(f"  a = {a:<6} d : worst band = {np.pi-(Ls-d)/a:.4f} a")
