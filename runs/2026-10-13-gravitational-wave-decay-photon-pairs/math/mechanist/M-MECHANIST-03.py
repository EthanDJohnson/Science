"""M-MECHANIST-03: two crossing monochromatic plane GWs (linear 'plus' pols, strain h each, angular frequency w,
crossing angle th in (0, pi]): in-in pair rate per volume Gamma = n_a n_b sigma_lin(s) (1 - cos th) (c = 1), with
n = rho/w = w h^2/(32 pi G) (rho = w^2 h^2/(32 pi G), Isaacson, plus pol), s = 2 w^2 (1 - cos th),
sigma_lin = (1/2) int dOmega |M|^2_lin /(64 pi^2 s), |M|^2_lin = (8 pi G)^2 (t^4 + u^4)/(2 s^2) (azimuth-averaged
linear = half the opposite-helicity value, M-MECHANIST-02). Claims: Gamma ~ th^4 at small th; 2.9e-101 m^-3 s^-1
head-on at h = 1e-21, f = 150 Hz; 1.5e-102 at th = 1; 1.8e-110 at th = 0.01 (SI).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

G, w, h, s, th, c, phi = sp.symbols("G w h s theta c phi", positive=True)
T = -s * (1 - c) / 2; U = -s * (1 + c) / 2
M2 = (8 * sp.pi * G) ** 2 * (T**4 + U**4) / (2 * s**2)
sigma = sp.Rational(1, 2) * sp.integrate(sp.integrate(M2, (c, -1, 1)), (phi, 0, 2 * sp.pi)) / (64 * sp.pi**2 * s)
sigma = sp.simplify(sigma)
print("sigma_lin =", sigma)
identity(sigma, sp.Rational(2, 5) * sp.pi * G**2 * s)
n = w * h**2 / (32 * sp.pi * G)
Gam = sp.simplify(n * n * sigma.subs(s, 2 * w**2 * (1 - sp.cos(th))) * (1 - sp.cos(th)))
print("Gamma =", Gam)
identity(Gam, w**4 * h**4 * (1 - sp.cos(th)) ** 2 / (1280 * sp.pi))
limit(Gam / th**4, "theta", 0, w**4 * h**4 / (5120 * sp.pi))       # theta^4 law
# SI: Gamma = w^4 h^4 (1 - cos th)^2/(1280 pi c^3)
W = 2 * math.pi * 150.0
units("(1 rad/s)^4 / (1 m/s)^3", "1/(m^3*s)")
for ang, want in ((math.pi, "2.9e-101"), (1.0, "1.54e-102"), (0.01, "1.82e-110")):
    val = W**4 * 1e-84 * (1 - math.cos(ang)) ** 2 / (1280 * math.pi * 299792458.0**3)
    print(f"theta = {ang:.4f}: Gamma = {val:.4e} m^-3 s^-1")
    quantity(f"{val:.6e} 1/(m^3*s)", f"{want} 1/(m^3*s)", rel_tol=0.02)
# energy density cross-check vs lens's 1.1898e-11 J/m^3
quantity("(2*pi*150 /s)^2 * (1e-21)^2 * c^2 / (32*pi*G)", "1.1898e-11 J/m^3", rel_tol=1e-3)
raise SystemExit(finish())
