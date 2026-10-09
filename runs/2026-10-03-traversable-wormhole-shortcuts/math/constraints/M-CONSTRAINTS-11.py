"""M-CONSTRAINTS-11 (F13). JT gravity on global AdS2, ds^2 = (-dt^2 + ds^2)/sin^2 s, 0 < s < pi.
Equation (from action (1/16 pi G) int phi (R + 2)): 8 pi G T_ab = -nabla_a nabla_b phi + g_ab (box phi - phi).
Claims: phi = cos t / sin s is vacuum (T = 0); phi = phi0 [1 + (pi/2 - s) cot s] has traceless T, minimum phi0 at
s = pi/2; with affine null k^a = sin^2 s (1, 1), T_kk = -phi0 sin^4 s/(4 pi G); ANEC over the complete
boundary-to-boundary ray = -phi0/(8G); phi_r = lim s->0 s*phi = pi phi0/2, so ANEC = -phi_r/(4 pi G)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
from math_checks import identity, sign, limit, finish
from _geom import ricci, christoffel

t, s = sp.symbols("t s", real=True)
phi0, G = sp.symbols("phi0 G", positive=True)
x = [t, s]
g = sp.diag(-1, 1) / sp.sin(s)**2
Ric, R, Gam = ricci(g, x)
gi = g.inv()
Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(2) for b in range(2)))
identity(Rs, sp.Integer(-2))   # AdS2 with unit radius


def hess(p):
    return sp.Matrix(2, 2, lambda a, b: sp.diff(p, x[a], x[b]) - sum(Gam[c][a][b] * sp.diff(p, x[c]) for c in range(2)))


def T(p):
    H = hess(p)
    box = sp.simplify(sum(gi[a, b] * H[a, b] for a in range(2) for b in range(2)))
    return sp.simplify((-H + g * (box - p)) / (8 * sp.pi * G))


Tvac = T(sp.cos(t) / sp.sin(s))
for a in range(2):
    for b in range(2):
        identity(Tvac[a, b], sp.Integer(0), domain={"t": (-3, 3), "s": (0.1, 3.0)})
phi = phi0 * (1 + (sp.pi / 2 - s) * sp.cot(s))
Tw = T(phi)
trace = sp.simplify(sum(gi[a, b] * Tw[a, b] for a in range(2) for b in range(2)))
identity(trace, sp.Integer(0), domain={"s": (0.05, 3.09)})
identity(sp.diff(phi, s).subs(s, sp.pi / 2), sp.Integer(0))
identity(phi.subs(s, sp.pi / 2), phi0)
sign(sp.diff(phi, s, 2).subs(s, sp.pi / 2), "positive")      # minimum at the throat
# affine null geodesic check
k = [sp.sin(s)**2, sp.sin(s)**2]
for a in range(2):
    acc = sum(k[b] * sp.diff(k[a], x[b]) for b in range(2)) + sum(Gam[a][b][c] * k[b] * k[c] for b in range(2) for c in range(2))
    identity(sp.simplify(acc), sp.Integer(0), domain={"s": (0.05, 3.09)})
Tkk = sp.simplify(sum(Tw[a, b] * k[a] * k[b] for a in range(2) for b in range(2)))
print("T_kk =", Tkk)
identity(Tkk, -phi0 * sp.sin(s)**4 / (4 * sp.pi * G), domain={"s": (0.05, 3.09)})
sign(Tkk, "negative", domain={"s": (0.01, 3.13)})
anec = sp.simplify(sp.integrate(sp.simplify(Tkk / sp.sin(s)**2), (s, 0, sp.pi)))   # d lambda = ds / k^s
identity(anec, -phi0 / (8 * G))
phir = sp.limit(s * phi, s, 0)
identity(phir, sp.pi * phi0 / 2)
identity(anec, -phir / (4 * sp.pi * G))
identity(anec, -2 * phir / (8 * sp.pi * G))
limit(-phi0 / (8 * G), "phi0", 0, "0")    # no wormhole (phi0 -> 0) -> no ANEC violation
raise SystemExit(finish())
