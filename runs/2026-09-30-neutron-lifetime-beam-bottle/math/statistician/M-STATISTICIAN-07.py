"""M-STATISTICIAN-07: correlated (GLS) combinations (F7). Mean = 1^T V^-1 x / 1^T V^-1 1, var = 1/(1^T V^-1 1),
chi2 = r^T V^-1 r. Lifetimes in s.
Lens: (i) sys parts of Serebrov05-Serebrov18 and Pattie18-Musedinovic25 at rho 0.8 -> 878.316 (from 878.321);
(ii) total errors of the same pairs at rho 0.8 -> 878.10 +- 0.22, S 2.42, tension 4.69 sigma;
(iii) BL1-Sussex sys at rho 0.8 -> 887.64 +- 2.24, tension 4.08 sigma."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish
import numpy as np
import sympy as sp

def gls(rows, pairs, rho, which):
    n = len(rows); V = np.diag([r[2] ** 2 for r in rows])
    idx = {r[0]: i for i, r in enumerate(rows)}
    for a, b in pairs:
        i, j = idx[a], idx[b]
        ea = rows[i][4] if which == "sys" else rows[i][2]
        eb = rows[j][4] if which == "sys" else rows[j][2]
        V[i, j] = V[j, i] = rho * ea * eb
    x = np.array([r[1] for r in rows]); one = np.ones(n)
    Vi = np.linalg.inv(V)
    var = 1 / (one @ Vi @ one); m = var * (one @ Vi @ x)
    r = x - m; chi2 = r @ Vi @ r
    return m, math.sqrt(var), chi2, max(1, math.sqrt(chi2 / (n - 1)))

pairs = [("Serebrov05", "Serebrov18"), ("Pattie18", "Musedinovic25")]
m0 = gls(STORAGE, pairs, 0.0, "sys"); identity(f"{m0[0]:.6f}", f"{wmean(STORAGE)[0]:.6f}")  # rho=0 reduces to plain mean
m1 = gls(STORAGE, pairs, 0.8, "sys"); print("(i)", m1); identity(f"{m1[0]:.3f}", "878.316")
m2 = gls(STORAGE, pairs, 0.8, "tot"); print("(ii)", m2)
identity(f"{m2[0]:.2f}", "878.10"); identity(f"{m2[1]:.2f}", "0.22"); identity(f"{m2[3]:.2f}", "2.42")
mp_, sp_, *_ = wmean(PROTON)
t2 = (mp_ - m2[0]) / q(sp_, m2[1] * m2[3]); print("(ii) tension", t2); identity(f"{t2:.2f}", "4.69")
p3 = gls(PROTON, [("BL1 Yue13", "Sussex-ILL Byrne96")], 0.8, "sys"); print("(iii)", p3)
identity(f"{p3[0]:.2f}", "887.64"); identity(f"{p3[1]:.2f}", "2.24")
ms, ss, c, d, S = wmean(STORAGE)
t3 = (p3[0] - ms) / q(p3[1], ss * S); print("(iii) tension", t3); identity(f"{t3:.2f}", "4.08")
# symbolic 2x2 GLS limit: rho -> 0 gives inverse-variance mean
x1, x2, s1, s2, r = sp.symbols("x1 x2 s1 s2 r", positive=True)
V = sp.Matrix([[s1**2, r*s1*s2], [r*s1*s2, s2**2]]); o = sp.Matrix([1, 1]); X = sp.Matrix([x1, x2])
mg = (o.T * V.inv() * X)[0] / (o.T * V.inv() * o)[0]
limit(mg, "r", 0, "(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)")
raise SystemExit(finish())
