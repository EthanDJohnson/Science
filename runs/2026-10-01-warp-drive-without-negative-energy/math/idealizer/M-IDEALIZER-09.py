"""M-IDEALIZER-09: Shapiro delay vs shift advance along the axis (F9). Linear harmonic gauge, G = c = 1.
Uniform shell R1 = 10 m, R2 = 20 m, M = 3.334 m, p = 0: h_00 = 2U, h_ij = 2U delta_ij, U = int rho/|x-x'|.
Light along the axis: dt = (1 + 2U) dz -> delay = 2 int_{-L}^{L} U dz.
Claims: delay 16.46 m (54.9 ns) at L = 20 m, 37.9 m at 100 m, 99.3 m at 10 km; advance = 30 m * beta;
net advance needs beta >= 0.55 (L = 20) .. 3.3 (10 km); advance/delay at the cap 0.05-0.20 (L = 20), 0.008 (10 km).
Structural: for null k, (T_ab - eta_ab T/2) k^a k^b = T_kk, so the delay density 2 int T_kk/|x-x'| >= 0 under NEC.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/idealizer")
import numpy as np
import sympy as sp
from scipy.integrate import quad
from math_checks import identity, quantity, limit, finish
from profiles import KG_TO_M, C_SI

# structural identity
T = sp.Matrix(4, 4, lambda a, b: sp.Symbol(f"T{min(a,b)}{max(a,b)}", real=True))
eta = sp.diag(-1, 1, 1, 1)
trT = sum(eta[a, a]*T[a, a] for a in range(4))
k = sp.Matrix([1, 0, 0, 1])
lhs = (k.T*(T - eta*trT/2)*k)[0, 0]
identity(sp.expand(lhs), sp.expand((k.T*T*k)[0, 0]), domain={s.name: (-3, 3) for s in T.free_symbols})

M = 4.49e27*KG_TO_M; R1, R2 = 10.0, 20.0
rho = 3*M/(4*np.pi*(R2**3 - R1**3))
def U(r):
    r = abs(r)
    if r <= R1:
        return 2*np.pi*rho*(R2**2 - R1**2)
    if r <= R2:
        menc = 4*np.pi*rho*(r**3 - R1**3)/3
        return menc/r + 2*np.pi*rho*(R2**2 - r**2)
    return M/r
# continuity checks of the potential
quantity(f"{U(R2 - 1e-12)}", f"{M/R2}", rel_tol=1e-9)
quantity(f"{U(R1 + 1e-12)}", f"{U(R1)}", rel_tol=1e-9)
def delay(L):
    inner = quad(U, 0, min(L, R2), points=[R1], limit=200)[0]
    outer = M*np.log(L/R2) if L > R2 else 0.0
    return 2*2*(inner + outer)
out = {}
for L, claim in [(20.0, 16.46), (100.0, 37.9), (1e4, 99.3)]:
    d = delay(L); out[L] = d
    print(f"L = {L:g} m: delay = {d:.3f} m = {d/C_SI*1e9:.2f} ns; beta for net advance = {d/30:.3f}")
    quantity(f"{d}", f"{claim}", rel_tol=0.003)
quantity(f"{out[20.0]/C_SI*1e9}", "54.9", rel_tol=0.003)
quantity(f"{out[20.0]/30}", "0.55", rel_tol=0.01)
quantity(f"{out[1e4]/30}", "3.3", rel_tol=0.01)
for cap, L, claim in [(0.0272, 20.0, 0.05), (0.107, 20.0, 0.20), (0.0272, 1e4, 0.008)]:
    r = 30*cap/out[L]
    print(f"advance/delay at beta = {cap}, L = {L:g}: {r:.4f} (claim {claim})")
    quantity(f"{r}", f"{claim}", rel_tol=0.05)
limit("2*2*M*log(L/20)", "M", 0, 0)
raise SystemExit(finish())
