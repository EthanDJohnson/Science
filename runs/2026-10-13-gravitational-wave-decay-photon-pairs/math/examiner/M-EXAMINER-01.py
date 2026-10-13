"""M-EXAMINER-01: the Pauli-Jordan field of a monopole source (scalar, natural units c = 1).
Source rho(t, x) = s(t) delta^3(x), s supported on [-T0, T0].
phi_ret = s(t - r)/(4 pi r), phi_adv = s(t + r)/(4 pi r), phi_PJ = phi_ret - phi_adv.
Claims: (a) phi_PJ solves the source-free wave equation everywhere, incl. r = 0 (regular there);
(b) for t > T0, phi_PJ = phi_ret; (c) for t < -T0, phi_PJ = -phi_adv (an incoming shell)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

t, r = sp.symbols("t r", positive=True)
tt = sp.Symbol("tt", real=True)
s = sp.Function("s")
phi_ret = s(tt - r) / (4 * sp.pi * r)
phi_adv = s(tt + r) / (4 * sp.pi * r)
phi = phi_ret - phi_adv

# (a) radial wave operator for r > 0: box phi = phi_tt - (1/r) (r phi)_rr
box = lambda f: sp.diff(f, tt, 2) - sp.diff(r * f, r, 2) / r
print("box phi_ret (r>0) =", sp.simplify(box(phi_ret)))
print("box phi_PJ  (r>0) =", sp.simplify(box(phi)))
# regularity at r = 0 with a concrete smooth s: Gaussian
S = sp.exp(-(tt) ** 2)
phiS = (S.subs(tt, tt - r) - S.subs(tt, tt + r)) / (4 * sp.pi * r)
lim0 = sp.limit(phiS, r, 0)
print("phi_PJ at r -> 0 (Gaussian s):", sp.simplify(lim0), " = -2 s'(t)/(4 pi)?",
      sp.simplify(lim0 - (-2 * sp.diff(S, tt) / (4 * sp.pi))) == 0)
identity(sp.simplify(box(phi)), sp.Integer(0))
# the retarded field alone, at r -> 0, is singular ~ s(t)/(4 pi r): it needs the source; the PJ field does not
limit(sp.simplify(phiS * r), "r", 0, sp.Integer(0))

# (b), (c): compact-support source, s(t) = bump on [-1, 1]; numeric spot checks
import mpmath as mp
def bump(x):
    return mp.e ** (-1 / (1 - x ** 2)) if abs(x) < 1 else mp.mpf(0)
def pj(T, R):
    return (bump(T - R) - bump(T + R)) / (4 * mp.pi * R)
def ret(T, R):
    return bump(T - R) / (4 * mp.pi * R)
def adv(T, R):
    return bump(T + R) / (4 * mp.pi * R)
ok_b = all(abs(pj(T, R) - ret(T, R)) == 0 for T in (1.5, 3, 10) for R in (0.3, 1.7, 2.5, 9.5, 20))
ok_c = all(abs(pj(T, R) + adv(T, R)) == 0 for T in (-1.5, -3, -10) for R in (0.3, 1.7, 2.5, 9.5, 20))
nonzero_in = abs(pj(-10, 9.6)) > 0   # at t = -10 the field is an incoming shell at r ~ 10, not zero
print("t > T0: PJ == ret:", ok_b, "; t < -T0: PJ == -adv:", ok_c, "; incoming shell nonzero at t=-10, r=9.6:",
      nonzero_in, float(pj(-10, 9.6)))
identity(sp.Integer(1 if (ok_b and ok_c and nonzero_in) else 0), sp.Integer(1))
raise SystemExit(finish())
