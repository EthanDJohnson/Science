"""M-IDEALIZER-07 (F7): Born-Oppenheimer/WKB time in [-(1/2M) d^2/dx^2 - M e0 + H_S] Psi = 0 (hbar = 1, model units).
Exact: Psi = sum_n c_n e^{i k_n x}|n>, k_n = sqrt(2M(M e0 - E_n)). Heavy WKB phase k_0-like: S = M v x, v = sqrt(2 e0).
Conditional chi_n(t) = c_n e^{i(k_n - M v) x}, t = x/v. Claim: i d_t chi = [H_S + H_S^2/(2 M v^2) + O(M^-2)] chi.
Numbers: E = (0, 1, 2.5), e0 = 50, equal weights, t = 10: 1-F(order 0) = 1.89e-4 (M=10), 1.88e-6, 1.88e-8, 1.88e-10;
prediction t^2 Var(E^2)/(2 M v^2)^2; corrected equation residual 1.3e-9 at M = 10.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import mpmath as mp
import sympy as sp
from math_checks import series, quantity, limit, finish

M, e0, En = sp.symbols("M e0 E_n", positive=True)
v = sp.sqrt(2 * e0)
kn = sp.sqrt(2 * M * (M * e0 - En))
# phase per unit t: -(k_n - M v) * v (so that chi ~ e^{-i omega_n t}); expand in 1/M
eps = sp.symbols("epsilon", positive=True)  # eps = 1/M
omega = sp.simplify(-(kn - M * v) * v).subs(M, 1 / eps)
series(omega, "epsilon", 0, 2, En + eps * En**2 / (2 * v**2), domain={"e0": (1, 100), "E_n": (0.1, 3)})
# heavy limit: omega -> E_n as M -> oo
limit(sp.simplify(-(kn - M * v) * v), "M", "oo", "E_n", domain={"e0": (1, 100), "E_n": (0.1, 3)})

mp.mp.dps = 40
E = [mp.mpf(0), mp.mpf(1), mp.mpf("2.5")]
p = [mp.mpf(1) / 3] * 3
e0v = mp.mpf(50); vv = mp.sqrt(2 * e0v); t = mp.mpf(10)
def infid(Mv, order):
    tot = 0
    for En_, pn in zip(E, p):
        k = mp.sqrt(2 * Mv * (Mv * e0v - En_))
        ph_exact = -(k - Mv * vv) * t   # phase at x = v t is (k - Mv) v t; exponent i(k-Mv)x
        ph_exact = (k - Mv * vv) * vv * t
        ph_model = -En_ * t if order == 0 else -(En_ + En_**2 / (2 * Mv * vv**2)) * t
        tot += pn * mp.expj(ph_exact - ph_model)
    return 1 - abs(tot) ** 2
varE2 = sum(pn * En_**4 for En_, pn in zip(E, p)) - sum(pn * En_**2 for En_, pn in zip(E, p)) ** 2
for Mv, want in [(10, "1.89e-4"), (100, "1.88e-6"), (1000, "1.88e-8"), (10000, "1.88e-10")]:
    Mv = mp.mpf(Mv)
    f0 = infid(Mv, 0); f1 = infid(Mv, 1)
    pred = t**2 * varE2 / (2 * Mv * vv**2) ** 2
    print(f"M={mp.nstr(Mv,5)}: 1-F0={mp.nstr(f0,6)}, prediction={mp.nstr(pred,6)}, 1-F1={mp.nstr(f1,4)}")
    quantity(f"{float(f0)}", want, rel_tol=0.01)
    quantity(f"{float(f0)}", f"{float(pred)}", rel_tol=0.01)
    if Mv == 10:
        quantity(f"{float(f1)}", "1.3e-9", rel_tol=0.05)
raise SystemExit(finish())
