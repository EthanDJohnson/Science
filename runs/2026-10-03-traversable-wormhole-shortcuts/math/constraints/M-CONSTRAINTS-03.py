"""M-CONSTRAINTS-03 (F3). MT metric ds^2 = -dt^2 + dr^2/(1-b/r) + r^2 dOmega^2, b = r0(1+alpha(1-r0/r)).
Claims (alpha = 0.5, r0 = 1 m): rho > 0 at r = 1, 1.5, 3, 10 m; rho + p_r = -1.99e-2 m^-2 at the throat;
moving observer at throat sees gamma^2(rho + v^2 p_r) < 0 for v > sqrt(alpha); M_ADM = 0.75 r0;
radial ANEC (E = 1, both sides) = -0.0946 m^-1."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
import mpmath as mp
from math_checks import identity, sign, limit, inequality, finish
from _geom import einstein_mixed

t, rr, th, ph = sp.symbols("t r theta phi", positive=True)
r0, al = sp.symbols("r0 alpha", positive=True)
b = r0 * (1 + al * (1 - r0 / rr))
g = sp.diag(-1, 1 / (1 - b / rr), rr**2, rr**2 * sp.sin(th)**2)
Gm, Ric, R, Gam, Rs = einstein_mixed(g, [t, rr, th, ph])
rho = sp.simplify(-Gm[0, 0] / (8 * sp.pi))
pr = sp.simplify(Gm[1, 1] / (8 * sp.pi))
print("rho =", rho, " p_r =", pr)
identity(rho, sp.diff(b, rr) / (8 * sp.pi * rr**2))
identity(pr, -b / (8 * sp.pi * rr**3))
sign(rho.subs({r0: 1, al: sp.Rational(1, 2)}), "positive", domain={"r": (1, 10)})
thr = sp.simplify((rho + pr).subs(rr, r0))
identity(thr, -(1 - al) / (8 * sp.pi * r0**2))
print("throat rho+p_r (alpha=0.5, r0=1) =", sp.N(thr.subs({al: 0.5, r0: 1})))
inequality(abs(sp.N(thr.subs({al: 0.5, r0: 1})) + 0.0199) / 0.0199, "<", 0.005)
# moving observer: gamma^2 (rho + v^2 p_r) changes sign at v^2 = -rho/p_r = alpha at the throat
vcrit2 = sp.simplify(-(rho / pr).subs(rr, r0))
identity(vcrit2, al)
limit(vcrit2, "alpha", 0, "0")  # alpha -> 0 (Ellis-like zero static density) every observer sees rho<=0 limit
# ADM mass: m(r) = b/2 -> r0(1+alpha)/2
identity(sp.limit(b / 2, rr, sp.oo), r0 * (1 + al) / 2)
# ANEC: E = 1, k^t = 1, dl = dr/sqrt(1-b/r), two sheets
mp.mp.dps = 25
fr = sp.lambdify(rr, sp.simplify(((rho + pr) / sp.sqrt(1 - b / rr)).subs({al: sp.Rational(1, 2), r0: 1})), "mpmath")
# with r = 1 + w^2: sqrt(2r^2-3r+1) = w sqrt(1+2w^2), so fr(r) * 2w = sqrt2 (2-3r)/(8 pi r^3 sqrt(1+2w^2)) (alpha = 1/2)
print("fr check at r=2:", fr(2), mp.sqrt(2) * (2 - 6) / (16 * mp.pi * 8 * mp.sqrt(3)))
I = 2 * mp.quad(lambda w: mp.sqrt(2) * (2 - 3 * (1 + w**2)) / (8 * mp.pi * (1 + w**2)**3 * mp.sqrt(1 + 2 * w**2)), [0, 1, mp.inf])
print("ANEC =", mp.nstr(I, 8))
inequality(abs(float(I) + 0.0946) / 0.0946, "<", 0.005)
raise SystemExit(finish())
