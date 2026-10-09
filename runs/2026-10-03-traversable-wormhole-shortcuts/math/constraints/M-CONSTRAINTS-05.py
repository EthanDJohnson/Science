"""M-CONSTRAINTS-05 (F5). Static thin-shell wormhole, two copies of -A dt^2 + dr^2/A + r^2 dOmega^2 glued at r = a.
Claims: sigma = -sqrt(A)/(2 pi a), P = (1 - M/a)/(4 pi a sqrt(A)); flat: sigma = -1/(2 pi a), mass -2a;
sigma + P >= 0 iff a <= 3M; shell ANEC sigma E/sqrt(A); SI numbers at a = 1 m flat and M = 1476.6 m."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
from math_checks import identity, sign, limit, quantity, finish
from _geom import christoffel

t, rr, th, ph = sp.symbols("t r theta phi", positive=True)
M, a, En = sp.symbols("M a En", positive=True)
A = 1 - 2 * M / rr
g = sp.diag(-A, 1 / A, rr**2, rr**2 * sp.sin(th)**2)
Gam = christoffel(g, [t, rr, th, ph])
n_r = 1 / sp.sqrt(A)              # outward unit normal (covariant r-component)
Ktt = -n_r * Gam[1][0][0]         # K_ij = -n_mu Gamma^mu_ij on r = const
Kthth = -n_r * Gam[1][2][2]
Kt_t = sp.simplify(Ktt / g[0, 0]); Kth_th = sp.simplify(Kthth / g[2, 2])
# wormhole: both sides flare outward, jump [K] = 2K; Lanczos S^i_j = -(1/8pi)([K^i_j] - delta [K])
trK = Kt_t + 2 * Kth_th
St_t = -(1 / (8 * sp.pi)) * (2 * Kt_t - 2 * trK)
Sth_th = -(1 / (8 * sp.pi)) * (2 * Kth_th - 2 * trK)
sigma = sp.simplify((-St_t).subs(rr, a)); P = sp.simplify(Sth_th.subs(rr, a))
Aa = 1 - 2 * M / a
print("sigma =", sigma, " P =", P)
identity(sigma, -sp.sqrt(Aa) / (2 * sp.pi * a), domain={"M": (0.1, 1), "a": (2.5, 10)})
identity(P, (1 - M / a) / (4 * sp.pi * a * sp.sqrt(Aa)), domain={"M": (0.1, 1), "a": (2.5, 10)})
limit(sigma, "M", 0, "-1/(2*pi*a)")
identity(sp.simplify(4 * sp.pi * a**2 * sigma.subs(M, 0)), -2 * a)
identity(sp.simplify(sigma + P), (3 * M / a - 1) / (4 * sp.pi * a * sp.sqrt(Aa)), domain={"M": (0.1, 1), "a": (2.5, 10)})
sign(sp.simplify(sigma + P).subs(M, 1), "positive", domain={"a": (2.01, 2.999)})
sign(sp.simplify(sigma + P).subs(M, 1), "negative", domain={"a": (3.001, 50)})
# shell ANEC: T_kk = S_ab k^a k^b delta(n); static-frame k^tau = k^n = E/sqrt(A); dlambda = dn/k^n
kt = En / sp.sqrt(Aa)
identity(sigma * kt**2 / kt, sigma * En / sp.sqrt(Aa), domain={"M": (0.1, 1), "a": (2.5, 10)})
# SI: c^4/G = 1.2103e44 N; c^2/G = 1.3466e27 kg/m
quantity("-1/(2*3.14159265) / (1 m) * c^4/G", "-1.926e43 J/m^2", rel_tol=2e-3)
quantity("1/(4*3.14159265) / (1 m) * c^4/G", "9.63e42 N/m", rel_tol=2e-3)
quantity("-2 * 1 m * c^2/G", "-2.693e27 kg", rel_tol=2e-3)
Mv = 1476.6
for av, s_cl, m_cl in [(2.5 * Mv, -2.33e39, -4.45e30), (3 * Mv, -2.51e39, -6.89e30), (4 * Mv, -2.31e39, -1.12e31), (1e4, -1.62e39, -2.26e31)]:
    s = float(sigma.subs({M: Mv, a: av})); ms = float(4 * sp.pi * av**2 * sigma.subs({M: Mv, a: av}))
    quantity(f"{s} / (1 m) * c^4/G", f"{s_cl} J/m^2", rel_tol=6e-3)
    quantity(f"{ms} m * c^2/G", f"{m_cl} kg", rel_tol=6e-3)
sp25 = float((sigma + P).subs({M: Mv, a: 2.5 * Mv}))
print("sigma+P at 2.5M =", sp25, "m^-1")
identity(sp.Float(round(sp25 * 1e6, 1)), sp.Float(9.6))
anec3 = float((sigma / sp.sqrt(Aa)).subs({M: Mv, a: 3 * Mv}))
quantity(f"{anec3} / (1 m) * c^4/G", "-4.35e39 J/m^2", rel_tol=3e-3)
raise SystemExit(finish())
