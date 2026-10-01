"""M-DIALECTICIAN-04: stationary-in-a-moving-frame warp metrics have Killing vector A = d_t + v d_x;
its asymptotic norm A.A = -1 + v^2 is >= 0 iff v >= 1 (c = 1), so Beig-Chrusciel case 1 (p = 0) applies;
for v < 1, p ∝ A gives ADM velocity |p_vec|/p^0 = v exactly. Geometric units, v dimensionless.
Independent: Lie derivative of a general warp metric ds^2 = -N^2 dt^2 + h_ij(dx^i - b^i dt)(dx^j - b^j dt)
with all fields functions of (x - v t, y, z) and asymptotically N -> 1, b -> 0, h -> delta (comoving shift form).
The Beig-Chrusciel theorem itself and PET rigidity are literature, not checked here.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, finish

t, x, y, z = sp.symbols("t x y z", real=True)
v = sp.symbols("v", positive=True)
X = [t, x, y, z]
xi = x - v * t
Nf = sp.Function("N")(xi, y, z)
bf = [sp.Function(f"b{i}")(xi, y, z) for i in range(3)]
hf = [[sp.Function(f"h{min(i,j)}{max(i,j)}")(xi, y, z) for j in range(3)] for i in range(3)]
g = sp.zeros(4, 4)
g[0, 0] = -Nf**2 + sum(hf[i][j] * bf[i] * bf[j] for i in range(3) for j in range(3))
for i in range(3):
    g[0, i + 1] = g[i + 1, 0] = -sum(hf[i][j] * bf[j] for j in range(3))
    for j in range(3):
        g[i + 1, j + 1] = hf[i][j]
A = [1, v, 0, 0]
# Lie derivative with constant components: (L_A g)_mn = A^r d_r g_mn
LAg = sp.Matrix(4, 4, lambda m, n: sum(A[r] * sp.diff(g[m, n], X[r]) for r in range(4)))
print("L_A g == 0:", sp.simplify(LAg) == sp.zeros(4, 4))
identity(sp.simplify(sum(LAg[m, n] ** 2 for m in range(4) for n in range(4))), 0)
# asymptotic norm with N=1, b=0, h=delta
eta = sp.diag(-1, 1, 1, 1)
norm = sum(eta[m, n] * A[m] * A[n] for m in range(4) for n in range(4))
identity(norm, v**2 - 1)
sign(norm, "positive", domain={"v": (1.000001, 100)})
sign(norm, "zero", domain={"v": (1, 1)})
sign(norm, "negative", domain={"v": (0, 0.999999)})
# subluminal: p = lambda A, with p timelike future: ADM velocity = p^x/p^t = v; boosted mass M: p = M gamma (1, v)
lam, M = sp.symbols("lambda M", positive=True)
p = [lam * a for a in A]
identity(p[1] / p[0], v)
gam = 1 / sp.sqrt(1 - v**2)
# fixing p.p = -M^2 gives lambda = M gamma and |p_vec| = gamma M v
lam_sol = [s for s in sp.solve(sp.Eq(-(lam**2) * (1 - v**2), -M**2), lam) if s.subs({v: sp.Rational(1, 2), M: 1}) > 0][0]  # future-pointing root
identity(lam_sol * v, gam * M * v, domain={"v": (0, 0.99)})
limit(lam_sol * v, "v", 0, 0)
raise SystemExit(finish())
