"""M-MECHANIST-02: ADM momentum P_i = (1/8pi) oint (K_ij - K h_ij) dS^j.

(a) Static slicing with zero shift (shell frame, Schwarzschild exterior): K_ij = -(1/2N)(d_t h_ij - D_i b_j - D_j b_i) = 0,
    hence P_i = 0 exactly.
(b) Limit check: weak-field point mass M moving at small v along x (harmonic gauge, t = 0):
    h_tt = 2M/r, h_ij = 2M/r delta_ij, h_tx = -4 M v / r, with r -> |x - v t|. Flux at large radius
    should give |P_x| = M v (the momentum of a boosted mass), confirming the formula/normalization.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

t, x, y, z = sp.symbols("t x y z", real=True)
Ms, v, Rr = sp.symbols("M v R", positive=True)
# (a) Schwarzschild isotropic, static: h_ij = psi^4 delta_ij, no t dependence, shift 0
rr = sp.sqrt(x**2 + y**2 + z**2)
psi = 1 + Ms / (2 * rr)
hij = psi**4 * sp.eye(3)
K_a = sp.Matrix(3, 3, lambda i, j: sp.diff(hij[i, j], t))  # shift terms vanish (beta = 0)
identity(sp.simplify(K_a.norm()), "0")

# (b) boosted weak-field mass
rp = sp.sqrt((x - v * t)**2 + y**2 + z**2)
beta_cov = [-4 * Ms * v / rp, 0, 0]          # beta_i = g_ti
h = (1 + 2 * Ms / rp) * sp.eye(3)
Xs = [x, y, z]
K = sp.Matrix(3, 3, lambda i, j: -sp.Rational(1, 2) * (sp.diff(h[i, j], t) - sp.diff(beta_cov[j], Xs[i]) - sp.diff(beta_cov[i], Xs[j])))
trK = K.trace()
th, ph = sp.symbols("theta phi", real=True)
n = [sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)]
sub = {x: Rr * n[0], y: Rr * n[1], z: Rr * n[2], t: 0}
integrand = sum((K[0, j] - trK * (1 if j == 0 else 0)) * n[j] for j in range(3)).subs(sub)
integrand = sp.simplify(integrand * Rr**2)
Px = sp.integrate(sp.integrate(integrand * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)) / (8 * sp.pi)
Px = sp.simplify(Px)
print("P_x (weak boosted mass, first order in v) =", Px)
identity(sp.Abs(Px), Ms * v)
limit(Px, "v", 0, "0")
raise SystemExit(finish())
