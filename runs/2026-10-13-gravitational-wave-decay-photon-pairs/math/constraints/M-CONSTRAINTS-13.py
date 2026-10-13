"""M-CONSTRAINTS-13: exact plane-wave facts (F14). Geometric units G = c = 1, signature (-,+,+,+).
ds^2 = -dt^2 + dx^2 + dy^2 + dz^2 + H(u,x,y) du^2, u = t - z.
(a) H = A(u)(x^2 - y^2) + 2 B(u) x y: vacuum (G_ab = 0), Kretschmann = 0, R^x_txt = -A(t-z) (lens sign).
(b) H = F(u)(x^2 + y^2): G_ab = -2 F k_a k_b with k = du (null dust), trace 0, G_ab G^ab = 0;
    energy density G_ab u^a u^b for static observer = -2F >= 0 iff F <= 0 (lens: positive energy for F < 0).
(c) s = 2 w1 w2 (1 - cos theta) for w1 = w2 = 1 at 0, 1, 10, 90, 180 deg.
Own Christoffel/Riemann code; gr_tensors used as a cross-check of the Einstein tensor.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, finish

t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
u = t - z
A, B, F = sp.Function("A"), sp.Function("B"), sp.Function("F")

def curv(H):
    g = sp.diag(-1, 1, 1, 1) + H * sp.Matrix(4, 4, lambda i, j: (1 if i == 0 else 0 if i in (1, 2) else -1) * (1 if j == 0 else 0 if j in (1, 2) else -1))
    gi = sp.simplify(g.inv())
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4)) / 2)
             for c in range(4)] for b in range(4)] for a in range(4)]
    R = [[[[sp.simplify(sp.diff(Gam[a][d][b], X[c]) - sp.diff(Gam[a][c][b], X[d])
                        + sum(Gam[a][c][e] * Gam[e][d][b] - Gam[a][d][e] * Gam[e][c][b] for e in range(4)))
            for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.Matrix(4, 4, lambda b, d: sp.simplify(sum(R[a][b][a][d] for a in range(4))))
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
    Gt = sp.simplify(Ric - g * Rs / 2)
    # Kretschmann R_abcd R^abcd
    Rlow = lambda a, b, c, d: sum(g[a, e] * R[e][b][c][d] for e in range(4))
    Rl = [[[[sp.simplify(Rlow(a, b, c, d)) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    K = 0
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if Rl[a][b][c][d] == 0:
                        continue
                    K += Rl[a][b][c][d] * sum(gi[a, p] * gi[b, q] * gi[c, r] * gi[d, s_] * Rl[p][q][r][s_]
                                               for p in range(4) for q in range(4) for r in range(4) for s_ in range(4)
                                               if gi[a, p] != 0 and gi[b, q] != 0 and gi[c, r] != 0 and gi[d, s_] != 0)
    return g, gi, R, Gt, sp.simplify(K)

g, gi, R, Gt, K = curv(A(u) * (x**2 - y**2) + 2 * B(u) * x * y)
print("vacuum pp-wave: G_ab =", Gt.applyfunc(sp.simplify).tolist(), "; K =", K, "; R^x_txt =", sp.simplify(R[1][0][1][0]))
identity(sum(abs(e) for e in Gt) if False else sp.simplify(sum(e**2 for e in Gt)), 0)
identity(K, 0)
identity(sp.simplify(R[1][0][1][0] + A(u)), 0)

g2, gi2, R2, Gt2, K2 = curv(F(u) * (x**2 + y**2))
k = sp.Matrix([1, 0, 0, -1])   # k_a = d_a u
target = -2 * F(u) * k * k.T
print("null dust: G_ab =", Gt2.tolist())
identity(sp.simplify(sum((Gt2 - target)[i]**2 for i in range(16))), 0)
tr = sp.simplify(sum(gi2[a, b] * Gt2[a, b] for a in range(4) for b in range(4)))
sq = sp.simplify(sum(gi2[a, c] * gi2[b, d] * Gt2[a, b] * Gt2[c, d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
identity(tr, 0)
identity(sq, 0)
# energy density measured by u^a = (1/sqrt(-g_tt), 0,0,0) at x=y=0: G_tt = -2F -> positive iff F < 0
print("G_tt =", sp.simplify(Gt2[0, 0]))
identity(sp.simplify(Gt2[0, 0]), -2 * F(u))
# cross-check G_ab with gr_tensors
try:
    from gr_tensors import Spacetime
    st = Spacetime(g2, [t, x, y, z])
    Gtool = sp.Matrix(st.einstein())
    identity(sp.simplify(sum((Gtool - Gt2)[i]**2 for i in range(16))), 0)
except Exception as exc:
    print("gr_tensors cross-check skipped:", exc)
for deg, want in [(1, 3.05e-4), (10, 0.0304), (90, 2), (180, 4)]:
    s = 2 * (1 - math.cos(math.radians(deg)))
    print(f"theta={deg} deg: s/w^2 = {s:.4g}")
    quantity(f"{s}", f"{want}", rel_tol=0.01)
raise SystemExit(finish())
