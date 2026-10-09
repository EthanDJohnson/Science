"""M-CONSTRAINTS-02 (F2). Static spherical metric ds^2 = -e^{2Phi(l)} dt^2 + dl^2 + r(l)^2 dOmega^2.
Claim: along the radial null geodesic (k_t = -E), integral T_kk d lambda = -(E/4pi) int e^{-Phi} (r'/r)^2 dl
+ boundary terms that vanish when Phi is bounded and r'/r -> 0 at both ends; hence strictly negative.
Numeric: Phi = -b0/r, r = sqrt(l^2+b0^2), b0 = 1 m gives -0.19798 m^-1 (E = 1)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
import mpmath as mp
from math_checks import identity, sign, inequality, finish
from _geom import ricci

t, l, th, ph = sp.symbols("t l theta phi", real=True)
En = sp.symbols("En", positive=True)
Phi = sp.Function("Phi")(l)
r = sp.Function("r")(l)
g = sp.diag(-sp.exp(2 * Phi), 1, r**2, r**2 * sp.sin(th)**2)
Ric, R, Gam = ricci(g, [t, l, th, ph])
# affine radial null vector: k^t = E e^{-2Phi}, k^l = E e^{-Phi}
k = [En * sp.exp(-2 * Phi), En * sp.exp(-Phi), 0, 0]
Rkk = sp.simplify(sum(Ric[a, b] * k[a] * k[b] for a in range(4) for b in range(4)))
print("R_kk =", Rkk)
# check k is geodesic: k^b nabla_b k^a = 0
for a in range(4):
    acc = sum(k[b] * sp.diff(k[a], [t, l, th, ph][b]) for b in range(4)) + \
        sum(Gam[a][b][c] * k[b] * k[c] for b in range(4) for c in range(4))
    identity(sp.simplify(acc), sp.Integer(0))
# integrand per dl: T_kk * d lambda/dl = (R_kk/8pi) / k^l
integrand = sp.simplify(Rkk / (8 * sp.pi) / k[1])
claimed = -(En / (4 * sp.pi)) * sp.exp(-Phi) * (sp.diff(r, l) / r)**2
boundary = -(En / (4 * sp.pi)) * sp.exp(-Phi) * sp.diff(r, l) / r     # candidate total-derivative term
identity(sp.simplify(integrand - claimed - sp.diff(boundary, l)), sp.Integer(0))

# sign of the reduced integrand: any real Phi, r > 0, r' real
Ph, rr, rp = sp.symbols("Ph rr rp", real=True)
sign(-(En / (4 * sp.pi)) * sp.exp(-Ph) * (rp / rr)**2, "nonpositive",
     domain={"Ph": (-5, 5), "rr": (0.1, 10), "rp": (-3, 3), "En": (0.1, 10)})

# numeric: Phi = -b0/r, b0 = 1, direct vs by-parts
mp.mp.dps = 30
def direct(lv):
    expr = integrand.subs(En, 1)
    return expr
rf = lambda lv: mp.sqrt(lv**2 + 1)
ll = sp.symbols("ll", real=True)
rexpr = sp.sqrt(ll**2 + 1)
phexpr = -1 / rexpr
sub = integrand.subs(En, 1).subs({sp.Derivative(r, (l, 2)): sp.diff(rexpr, ll, 2),
                                  sp.Derivative(Phi, (l, 2)): sp.diff(phexpr, ll, 2)})
sub = sub.subs({sp.Derivative(r, l): sp.diff(rexpr, ll), sp.Derivative(Phi, l): sp.diff(phexpr, ll)})
sub = sub.subs({r: rexpr, Phi: phexpr})
fd = sp.lambdify(ll, sub, "mpmath")
Idirect = mp.quad(fd, [-mp.inf, -5, 0, 5, mp.inf])
Ibp = -1 / (4 * mp.pi) * mp.quad(lambda v: mp.exp(1 / rf(v)) * (v / rf(v)**2)**2, [-mp.inf, 0, mp.inf])
print("Phi=-b0/r ANEC direct =", mp.nstr(Idirect, 10), " by parts =", mp.nstr(Ibp, 10))
identity(sp.Float(str(Idirect), 25), sp.Float(str(Ibp), 25))
identity(sp.Float(mp.nstr(Ibp, 5), 5), sp.Float("-0.19798", 5))
# limit Phi -> 0 reduces to Ellis -1/8
I0 = -1 / (4 * mp.pi) * mp.quad(lambda v: (v / rf(v)**2)**2, [-mp.inf, 0, mp.inf])
identity(sp.Float(str(I0), 25), sp.Rational(-1, 8))
inequality(sp.Float(str(Ibp), 20), "<", sp.Float(str(I0), 20))
raise SystemExit(finish())
