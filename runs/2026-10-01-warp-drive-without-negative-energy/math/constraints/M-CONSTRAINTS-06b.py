"""M-CONSTRAINTS-06 (part b): finer bisection of beta_crit along the perpendicular axis, and scale invariance.

Same own FD Einstein-tensor machinery as M-CONSTRAINTS-06 (copied from my own script, not the lens's).
Dense r sampling 11.0-13.5 m (step 0.01 m) on the y axis, h = 0.025 m. Claim beta_crit = 0.0244 +- 0.0002.
Scale check: M x 10, R1, R2 x 10 => min NEC x 1/100 at the scaled point (T ~ 1/L^2 at fixed compactness).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/constraints")
import importlib.util
import numpy as np
from math_checks import quantity, finish
spec = importlib.util.spec_from_file_location("m06", "runs/2026-10-01-warp-drive-without-negative-energy/math/constraints/M-CONSTRAINTS-06.py")
src = open("runs/2026-10-01-warp-drive-without-negative-energy/math/constraints/M-CONSTRAINTS-06.py").read()
src = src.split("rs = np.arange")[0]          # only the function definitions
ns = {}
exec(src, ns)
build_shell, einstein, make_g, DIRS = ns["build_shell"], ns["einstein"], ns["make_g"], ns["DIRS"]

def min_nec(beta, P, h=0.025, M=4.49e27, R1=10.0, R2=20.0):
    sh = build_shell(M, R1, R2, beta_warp=beta)
    Gab, G = einstein(make_g(sh), P, h * R1 / 10.0)
    T = Gab / (8 * np.pi)
    worst = (np.inf, None)
    for k in range(len(P)):
        gk = G[k]; Gi = np.linalg.inv(gk)
        N = 1 / np.sqrt(-Gi[0, 0]); n = -N * Gi[:, 0]
        S = np.linalg.inv(np.linalg.cholesky(gk[1:, 1:])).T
        E = np.zeros((4, 4)); E[0] = n
        for A in range(3):
            E[A + 1, 1:] = S[:, A]
        Tf = E @ T[k] @ E.T
        kk = np.hstack([np.ones((len(DIRS), 1)), DIRS])
        m = np.einsum("na,ab,nb->n", kk, Tf, kk).min()
        if m < worst[0]:
            worst = (m, P[k])
    return worst

rs = np.arange(11.0, 13.51, 0.01)
P = np.stack([np.zeros_like(rs), rs, np.zeros_like(rs)], 1)
lo, hi = 0.0235, 0.025
for _ in range(7):
    mid = 0.5 * (lo + hi)
    m, p = min_nec(mid, P)
    print(f"beta {mid:.5f}: min NEC {m:+.3e} at r = {np.linalg.norm(p):.2f}")
    if m < 0:
        hi = mid
    else:
        lo = mid
bc = 0.5 * (lo + hi)
print("beta_crit (perpendicular axis, dense r) =", bc, "+-", (hi - lo) / 2)
quantity(f"{bc}", "0.0244", rel_tol=0.03)
# scale invariance at beta = 0.03
m1, p1 = min_nec(0.03, P)
m10, p10 = min_nec(0.03, P * 10, M=4.49e28, R1=100.0, R2=200.0)
print("scale: ", m1, m10 * 100, np.linalg.norm(p1), np.linalg.norm(p10))
quantity(f"{m10 * 100 / m1}", "1", rel_tol=0.02)
raise SystemExit(finish())
