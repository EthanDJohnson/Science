"""M-DECOMPOSER-10: claim (P5, DECOMPOSER-D): "A non-generic path in vacuum with no tidal force is
locally Minkowski and gains nothing."
Null generic condition at a point of a null geodesic with tangent k:
   k_[e R_a]cd[b k_f] k^c k^d != 0     (Hawking-Ellis / Olum).
Test case: Schwarzschild (geometric units G = c = 1, M > 0, r > 2M), radial null geodesic
k^a = (1/f, 1, 0, 0), f = 1 - 2M/r (affinely parametrised, E = 1). Vacuum (R_ab = 0).
If the generic tensor vanishes identically along it while the Kretschmann scalar is nonzero,
the path is non-generic and tide-free in the transverse (generic-condition) sense, yet not
Minkowski: counterexample to "locally Minkowski". We also check its coordinate-time delay."""
import sys
import itertools
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import metrics
from math_checks import identity, sign, limit, finish

st, s = metrics.schwarzschild()
t, r, th, ph, M = s["t"], s["r"], s["theta"], s["phi"], s["M"]
g = st.g
Rup = st.riemann()
n = 4
Rl = [[[[sp.simplify(sum(g[a, e] * Rup[e][b][c][d] for e in range(n))) for d in range(n)]
        for c in range(n)] for b in range(n)] for a in range(n)]


def generic_tensor(kup):
    kl = [sp.simplify(sum(g[a, b] * kup[b] for b in range(n))) for a in range(n)]
    Qm = [[sp.simplify(sum(Rl[a][c][b][d] * kup[c] * kup[d] for c in range(n) for d in range(n)))
           for b in range(n)] for a in range(n)]
    # G_eabf = k_[e Q_a][b k_f] : antisymmetrise e<->a and b<->f of k_e Q_ab k_f
    out = {}
    for e, a, b, f in itertools.product(range(n), repeat=4):
        val = (kl[e] * Qm[a][b] * kl[f] - kl[a] * Qm[e][b] * kl[f]
               - kl[e] * Qm[a][f] * kl[b] + kl[a] * Qm[e][f] * kl[b]) / 4
        out[(e, a, b, f)] = sp.simplify(val)
    return out


f = 1 - 2 * M / r
k_rad = [1 / f, 1, 0, 0]
print("null check radial:", sp.simplify(sum(g[a, b] * k_rad[a] * k_rad[b] for a in range(n) for b in range(n))))
Grad = generic_tensor(k_rad)
nonzero = [kk for kk, v in Grad.items() if v != 0]
print("radial: nonzero generic-tensor components:", len(nonzero))
identity(str(len(nonzero)), "0")
K = sp.simplify(sum(Rl[a][b][c][d] * sp.simplify(
    sum(st.ginv[a, p] * st.ginv[b, q] * st.ginv[c, u] * st.ginv[d, w] * Rl[p][q][u][w]
        for p in range(n) for q in range(n) for u in range(n) for w in range(n)))
    for a in range(n) for b in range(n) for c in range(n) for d in range(n))) if hasattr(st, "ginv") else None
if K is None:
    K = 48 * M**2 / r**6
    print("ginv not exposed; using textbook Kretschmann 48 M^2/r^6 for the sign check")
print("Kretschmann:", K)
sign(K, "positive", domain={"M": (0.1, 10), "r": (25, 100)})
# a non-radial null direction at the equator (impact parameter): generic holds there
L = sp.Rational(1, 2)
kt = 1 / f
kph = L / r**2
kr = sp.sqrt(sp.simplify(1 - f * L**2 / r**2))
k_nr = [kt, kr, 0, kph]
Gnr = generic_tensor([sp.simplify(x.subs(th, sp.pi / 2)) if hasattr(x, "subs") else x for x in k_nr])
vals = [v.subs({th: sp.pi / 2, M: 1, r: 10}) for v in Gnr.values()]
nz = sum(1 for v in vals if abs(float(sp.N(v))) > 1e-14)
print("non-radial (L = 1/2, M = 1, r = 10): nonzero generic components:", nz)
sign(sp.Integer(nz), "positive")
# radial path delay: coordinate time per unit r = 1/f > 1 for r > 2M (Shapiro), flat limit M -> 0
sign(1 / f - 1, "positive", domain={"M": (0.1, 10), "r": (25, 100)})
limit(1 / f, "M", 0, 1, direction="+", domain={"r": (25, 100)})
raise SystemExit(finish())
