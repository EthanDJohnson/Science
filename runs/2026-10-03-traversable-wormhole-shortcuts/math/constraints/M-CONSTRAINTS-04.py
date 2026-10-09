"""M-CONSTRAINTS-04 (F4). Slow flare r(l) = b0 + sqrt(l^2+L^2) - L, Phi = 0, b0 = 1 m.
Claims: throat rho + p_l = -1/(4 pi b0 L); radial ANEC = -0.125, -0.0727, -0.0304, -0.01064, -0.00348 m^-1
for L = 1, 10, 1e2, 1e3, 1e4 m; asymptote I ~ -(sqrt2/4)/sqrt(b0 L); static rho at throat > 0 iff L > 2 b0."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-03-traversable-wormhole-shortcuts/math/constraints")
import sympy as sp
import mpmath as mp
from math_checks import identity, inequality, limit, finish
from _geom import einstein_mixed

t, l, th, ph = sp.symbols("t l theta phi", real=True)
b0, L = sp.symbols("b0 L", positive=True)
r = b0 + sp.sqrt(l**2 + L**2) - L
g = sp.diag(-1, 1, r**2, r**2 * sp.sin(th)**2)
Gm, Ric, R, Gam, Rs = einstein_mixed(g, [t, l, th, ph])
rho = sp.simplify(-Gm[0, 0] / (8 * sp.pi))
pl = sp.simplify(Gm[1, 1] / (8 * sp.pi))
identity(sp.simplify((rho + pl).subs(l, 0)), -1 / (4 * sp.pi * b0 * L))
rho0 = sp.simplify(rho.subs(l, 0))
print("rho at throat =", rho0)
identity(rho0, (1 - 2 * b0 / L) / (8 * sp.pi * b0**2))
# ANEC with E = 1: integral of (rho + p_l) dl (Phi = 0, k^t = k^l = 1)
mp.mp.dps = 25
claims = {1: -0.125, 10: -0.0727, 100: -0.0304, 1000: -0.01064, 10000: -0.00348}
dens = sp.lambdify((l, L), sp.simplify((rho + pl).subs(b0, 1)), "mpmath")
for Lv, c in claims.items():
    I = mp.quad(lambda v: dens(v, Lv), [-mp.inf, -10 * Lv, -Lv, -mp.sqrt(Lv), 0, mp.sqrt(Lv), Lv, 10 * Lv, mp.inf])
    asym = -mp.sqrt(2) / 4 / mp.sqrt(Lv)
    print(f"L={Lv}: ANEC = {mp.nstr(I, 8)}  claimed {c}  asymptote {mp.nstr(asym, 6)}")
    nd = len(str(abs(c)).rstrip('0').split('.')[1]) - 1
    inequality(abs(float(I) - c) / abs(c), "<", 0.005)
# asymptote: L*b0 -> infinity, I*sqrt(b0 L) -> -sqrt2/4 (independent stretched-coordinate derivation:
# r ~ b0(1+u^2), l = sqrt(2 L b0) u gives -(1/4pi) * sqrt2*pi/sqrt(L b0))
u = sp.symbols("u", real=True)
lead = -(1 / (4 * sp.pi)) * sp.integrate((2 / (L * b0)) * u**2 / (1 + u**2)**2 * sp.sqrt(2 * L * b0), (u, -sp.oo, sp.oo))
identity(sp.simplify(lead), -sp.sqrt(2) / (4 * sp.sqrt(b0 * L)))
rp = lambda v, Lv: v / mp.sqrt(v**2 + Lv**2); rs = lambda v, Lv: 1 + v**2 / (mp.sqrt(v**2 + Lv**2) + Lv)
Ibig = -1 / (4 * mp.pi) * mp.quad(lambda v: (rp(v, 1e8) / rs(v, 1e8))**2, [-mp.inf, -1e9, -1e8, -1e4, 0, 1e4, 1e8, 1e9, mp.inf])  # by-parts form, cancellation-free
print("L=1e8: I*sqrt(L) =", mp.nstr(Ibig * mp.sqrt(1e8), 8), " vs -sqrt2/4 =", mp.nstr(-mp.sqrt(2) / 4, 8))
inequality(abs(float(Ibig * mp.sqrt(1e8)) + 0.35355339) / 0.35355339, "<", 0.01)
limit(-1 / (4 * sp.pi * b0 * L), "L", "oo", "0")
raise SystemExit(finish())
