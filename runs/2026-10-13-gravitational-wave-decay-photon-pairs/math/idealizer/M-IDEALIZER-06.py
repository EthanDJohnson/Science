"""M-IDEALIZER-06: for a gas of on-shell gravitons T^{mn} = sum_i n_i k_i^m k_i^n / w_i, so
T_mn T^mn = sum_ij n_i n_j w_i w_j (1 - cos_ij)^2, and the kinetic rate (1/2) sum n n sigma_unpol v equals
(2 pi/5) G^2 T_mn T^mn. Plane wave (all k parallel): T_mn T^mn = 0.
Natural units, metric diag(1,-1,-1,-1). Random numeric gas plus symbolic two-beam identity.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, limit, finish
import numpy as np
import sympy as sp

eta = np.diag([1.0, -1, -1, -1])
rng = np.random.default_rng(3)
n_beams = 7
ws = rng.uniform(0.5, 2.0, n_beams); ns = rng.uniform(0.1, 3.0, n_beams)
dirs = rng.normal(size=(n_beams, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
ks = np.column_stack([ws, ws[:, None] * dirs])
T = sum(ns[i] * np.outer(ks[i], ks[i]) / ws[i] for i in range(n_beams))
TT = np.einsum("ab,cd,ac,bd->", T, T, eta, eta)
G = 1.0
kin = 0.0
for i in range(n_beams):
    for j in range(n_beams):
        cos = dirs[i] @ dirs[j]
        s = 2 * ws[i] * ws[j] * (1 - cos)
        kin += 0.5 * ns[i] * ns[j] * (2 * np.pi / 5) * G**2 * s * (1 - cos)
print(f"random gas: kinetic Gamma = {kin:.12g}, (2pi/5) G^2 TT = {2*np.pi/5*TT:.12g}")
quantity(f"{kin}", f"{2*np.pi/5*TT}", rel_tol=1e-10)
# plane wave: all along z
Tp = sum(ns[i] * np.outer([ws[i], 0, 0, ws[i]], [ws[i], 0, 0, ws[i]]) / ws[i] for i in range(n_beams))
TTp = np.einsum("ab,cd,ac,bd->", Tp, Tp, eta, eta)
print("plane wave TT =", TTp)
quantity(f"{abs(TTp) + 1}", "1", rel_tol=1e-12)
# symbolic two-beam: T_mn T^mn for beams at angle th
w1, w2, n1, n2, th = sp.symbols("w1 w2 n1 n2 theta", positive=True)
k1 = sp.Matrix([w1, 0, 0, w1]); k2 = sp.Matrix([w2, w2 * sp.sin(th), 0, w2 * sp.cos(th)])
Ts = n1 * k1 * k1.T / w1 + n2 * k2 * k2.T / w2
E = sp.diag(1, -1, -1, -1)
TTs = sp.simplify((E * Ts * E * Ts).trace())
identity(TTs, 2 * n1 * n2 * w1 * w2 * (1 - sp.cos(th))**2, domain={"theta": (0, 3.14159)})
limit(TTs, "theta", 0, 0)       # collinear limit -> 0
raise SystemExit(finish())
