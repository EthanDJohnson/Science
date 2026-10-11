"""M-CONSTRAINTS-01 (F1): EF-dominated QUMOND/AQUAL asymptotes at g_ext = 1.785 a0.

Independent derivation: linearise QUMOND about the uniform Newtonian EF g_Ne (along z):
  nabla^2 Phi = nu_e (nabla^2 Phi_N + K d_z^2 Phi_N), K = dln nu/dln y at y_e.
Solution Phi = -GM nu_e/r (1 + K sin^2(theta)/2); sphere-averaged radial boost nu_e (1 + K/3).
AQUAL: anisotropic Poisson mu_e (d_perp^2 + (1+L) d_z^2) phi = 4 pi G rho, L = dln mu/dln x.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import sympy as sp
import mpmath as mp
from math_checks import identity, quantity, finish
from cklib import ef_state, qumond_ef, aqual_ef, q

mp.mp.dps = 30
# 1. g_ext numeric value (SI)
quantity("(232.8 km/s)^2/(8.2 kpc)", "2.142e-10 m/s^2", rel_tol=1e-3)
gx = mp.mpf("2.142e-10") / mp.mpf("1.2e-10")
print("g_ext/a0 =", gx)
q(gx, 1.785, 2e-3, "g_ext/a0")

# 2. Potential solves the linearised QUMOND equation (away from origin)
x, y, z, nue, K = sp.symbols("x y z nu_e K", real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
Phi = -nue / r * (1 + K * (x**2 + y**2) / r**2 / 2)
PhiN = -1 / r
lhs = sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)
rhs = nue * K * sp.diff(PhiN, z, 2)   # nabla^2 Phi_N = 0 away from the origin
identity(lhs - rhs, sp.Integer(0), domain={"x": (0.1, 3), "y": (-3, 3), "z": (-3, 3), "nu_e": (1, 3), "K": (-0.9, 0)})
# sphere average of sin^2 theta = 2/3
th = sp.symbols("theta", positive=True)
identity(sp.integrate(sp.sin(th)**2 * sp.sin(th), (th, 0, sp.pi)) / 2, sp.Rational(2, 3))

# 3. Table values at 1.785 a0 (BZ18 Table 3 per lens)
lens = {"simple": (1.4228, 1.4056, 1.5602), "standard": (1.0726, 1.0662, 1.1462), "MLS": (1.3692, 1.3508, 1.5081)}
for name, (qu, aq, ne) in lens.items():
    ye, nu_e, Kk = ef_state(name, gx)
    print(f"{name}: y_e={float(ye):.5f} nu_e={float(nu_e):.5f} K={float(Kk):.5f}")
    q(qumond_ef(name, gx), qu, 2e-4, f"{name} QUMOND")
    q(aqual_ef(name, gx), aq, 2e-4, f"{name} AQUAL")
    q(nu_e, ne, 2e-4, f"{name} nu_e")
q(qumond_ef("n1.5", gx), 1.1670, 2e-4, "n=1.5 QUMOND")
# orientation range for simple: perpendicular nu_e(1+K/2) to parallel nu_e
ye, nu_e, Kk = ef_state("simple", gx)
q(nu_e * (1 + Kk / 2), 1.354, 1e-3, "simple perpendicular")
# g_ext range 1.71 - 2.09 a0
for name, lo, hi in [("simple", 1.4424, 1.3580), ("standard", 1.0800, 1.0505), ("MLS", 1.3894, 1.3021)]:
    q(qumond_ef(name, mp.mpf("1.71")), lo, 3e-4, f"{name} at 1.71 a0")
    q(qumond_ef(name, mp.mpf("2.09")), hi, 3e-4, f"{name} at 2.09 a0")
# limits: strong EF -> Newton (boost -> 1); weak EF -> large boost
q(qumond_ef("simple", mp.mpf(1e6)), 1.0, 1e-3, "simple, g_ext = 1e6 a0 (Newton limit)")
ye, nu_e, Kk = ef_state("simple", mp.mpf("1e-4")); q(qumond_ef("simple", mp.mpf("1e-4")) / nu_e, 5.0 / 6.0, 1e-3, "deep-MOND EF limit: boost/nu_e -> 1 - 1/6 (K -> -1/2)")
raise SystemExit(finish())
