"""M-CONSTRAINTS-01 (F1). Ellis-Bronnikov, Phi = 0: ds^2 = -dt^2 + dl^2 + (l^2+b0^2) dOmega^2.
Claims: rho = p_l = -1/(8 pi b0^2), p_t = +1/(8 pi b0^2) at the throat; rho + p_l = -1/(4 pi b0^2);
rho + p_l + 2 p_t = 0; radial ANEC = -E/(8 b0); Kretschmann 12/b0^4 at the throat; SI values
-9.63e42 J/m^3 and -1.513e43 J/m^2 for b0 = 1 m (per unit E). Independent derivation from the metric."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
from math_checks import identity, limit, sign, quantity, finish
from _geom import einstein_mixed, kretschmann

t, l, th, ph = sp.symbols("t l theta phi", real=True)
b0, En = sp.symbols("b0 En", positive=True)
r = sp.sqrt(l**2 + b0**2)
g = sp.diag(-1, 1, r**2, r**2 * sp.sin(th)**2)
x = [t, l, th, ph]
Gm, Ric, R, Gam, Rs = einstein_mixed(g, x)
rho = sp.simplify(-Gm[0, 0] / (8 * sp.pi))
pl = sp.simplify(Gm[1, 1] / (8 * sp.pi))
pt = sp.simplify(Gm[2, 2] / (8 * sp.pi))
print("rho =", rho, " p_l =", pl, " p_t =", pt)
identity(rho.subs(l, 0), -1 / (8 * sp.pi * b0**2))
identity(pl.subs(l, 0), -1 / (8 * sp.pi * b0**2))
identity(pt.subs(l, 0), 1 / (8 * sp.pi * b0**2))
identity(rho + pl, -b0**2 / (4 * sp.pi * r**4))
identity(rho + pl + 2 * pt, sp.Integer(0))
sign((rho + pl).subs(b0, 1), "negative", domain={"l": (-50, 50)})

# radial null geodesic, affine: k^t = E, k^l = E (Phi = 0); T_kk = R_kk / (8 pi); d lambda = dl / E
k = [En, En, 0, 0]
Rkk = sp.simplify(sum(Ric[a, b] * k[a] * k[b] for a in range(4) for b in range(4)))
Tkk = Rkk / (8 * sp.pi)
anec = sp.simplify(sp.integrate(Tkk / En, (l, -sp.oo, sp.oo)))
print("ANEC =", anec)
identity(anec, -En / (8 * b0))
limit(-En / (8 * b0), "b0", "oo", "0")   # flat limit: infinitely wide throat, no violation

K = kretschmann(g, x, R)
print("Kretschmann =", sp.simplify(K))
identity(K.subs(l, 0), 12 / b0**4)

# SI: geometric stress (m^-2) times c^4/G gives J/m^3
quantity("-0.0795774715 * c^4/G / (1 m)^2", "-9.63e42 J/m^3", rel_tol=2e-3)
quantity("-0.125 / (1 m) * c^4/G", "-1.513e43 J/m^2", rel_tol=2e-3)
raise SystemExit(finish())
