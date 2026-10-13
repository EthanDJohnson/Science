"""M-IDEALIZER-04: profile-free law P = (12 pi/25) G^2 w Int L(t)^2 dt (natural units; SI /c^10),
and the Gaussian profile numbers c_tot = 6 sqrt(2 pi)/25, T_eff = sqrt(pi/2)/sigma, rate ratio 4 pi.

Own reduction (narrow band, from M-01): for alpha = Theta g(u), u = k - w, the band integral over the graviton
axis gives 2 (g*g)(d0)/|K| in place of 2(sigma - |d0|)/|K|; so P = (4/25) G^2 N^2 w^3 * (3/2) Int (g*g)^2 dd0/(Int g^2)^2
(reduces to the top hat when g = 1 on the band). Time domain: a(t) = Int g(u) e^{-iut} du, L(t) = E |a|^2/Int |a|^2,
Parseval: Int |a|^2 = 2 pi Int |g|^2, Int |a|^4 = 2 pi Int |g*g|^2. E = N w.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, units, limit, finish
import sympy as sp
import numpy as np

G, w, sig, Nn = sp.symbols("G w sigma N_", positive=True)
Ee = Nn * w
# symbolic: with J4 = Int (g*g)^2, J2 = Int g^2, P = (4/25)(3/2) G^2 N^2 w^3 J4/J2^2;  Int L^2 dt = E^2 * 2pi J4/(2pi J2)^2
J4, J2 = sp.symbols("J4 J2", positive=True)
P_spec = sp.Rational(4, 25) * sp.Rational(3, 2) * G**2 * Nn**2 * w**3 * J4 / J2**2
IntL2 = Ee**2 * 2 * sp.pi * J4 / (2 * sp.pi * J2)**2
identity(P_spec, sp.Rational(12, 25) * sp.pi * G**2 * w * IntL2)
# top-hat reduction: J4 = 2 sig^3/3, J2 = sig
identity(P_spec.subs({J4: 2 * sig**3 / 3, J2: sig}), sp.Rational(4, 25) * G**2 * Nn**2 * w**3 * sig)

# Gaussian amplitude profile g = exp(-u^2/(2 sig^2))
u, d = sp.symbols("u d", real=True)
g = sp.exp(-u**2 / (2 * sig**2))
gg = sp.simplify(sp.integrate(g * g.subs(u, d - u), (u, -sp.oo, sp.oo)))
J4g = sp.integrate(gg**2, (d, -sp.oo, sp.oo))
J2g = sp.integrate(g**2, (u, -sp.oo, sp.oo))
Jg1 = sp.integrate(g, (u, -sp.oo, sp.oo))
c_g = sp.simplify(sp.Rational(4, 25) * sp.Rational(3, 2) * J4g / J2g**2 / sig)
T_g = sp.simplify(2 * sp.pi * J4g / Jg1**4)
print("Gaussian c_tot =", c_g, float(c_g), " T_eff =", T_g)
identity(c_g, 6 * sp.sqrt(2 * sp.pi) / 25)
identity(T_g, sp.sqrt(sp.pi / 2) / sig)
ratio = sp.simplify((c_g / T_g) / (sp.Rational(4, 25) / (4 * sp.pi / (3 * sig))))
print("Gaussian/top-hat rate coefficient ratio =", ratio, float(ratio))
identity(ratio, 4 * sp.pi)

# numeric Parseval check on a grid, complex (chirped) Gaussian profile, w = G = 1, N = 1
uu = np.linspace(-40, 40, 2**15); du = uu[1] - uu[0]
gnum = np.exp(-uu**2 / 2) * np.exp(1j * 0.7 * uu**2)
conv = np.convolve(gnum, gnum) * du
J4n = np.sum(np.abs(conv)**2) * du; J2n = np.sum(np.abs(gnum)**2) * du
P1 = 0.16 * 1.5 * J4n / J2n**2
tt = np.linspace(-200, 200, 2**15); dt = tt[1] - tt[0]
a = np.array([np.sum(gnum * np.exp(-1j * uu * t)) * du for t in tt[::8]])
L = np.abs(a)**2; L = L / (np.sum(L) * dt * 8)          # E = N w = 1
P2 = 12 * np.pi / 25 * np.sum(L**2) * dt * 8
print(f"chirped Gaussian: spectral P = {P1:.6e}, time-domain P = {P2:.6e}")
quantity(f"{P1}", f"{P2}", rel_tol=1e-3)
# SI units: G^2 w Int L^2 dt / c^10 dimensionless
units("(6.674e-11 m^3/(kg s^2))^2 * (1/s) * (1 W)^2 * (1 s) / (299792458 m/s)^10", "dimensionless")
limit(c_g / T_g * T_g, "sigma", 0, 6 * sp.sqrt(2 * sp.pi) / 25)
raise SystemExit(finish())
