"""M-ENGINEER-04: Visser thin-shell wormhole, flat limit.
Two copies of Schwarzschild (mass M >= 0) exterior r >= a glued at r = a, static shell.
Israel junction (G = c = 1): K^theta_theta = sqrt(1 - 2M/a)/a on each side, jump 2 sqrt(1-2M/a)/a,
sigma = -(1/4pi)[K^theta_theta] = -sqrt(1 - 2M/a)/(2 pi a). Flat limit M -> 0: sigma = -1/(2 pi a).
SI: areal energy = c^4/G times geometric (1/m). Shell rest mass m_s = 4 pi a^2 sigma.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

a, M = sp.symbols("a M", positive=True)
# extrinsic curvature of the r = a sphere in Schwarzschild: K_theta_theta = n^r Gamma... = sqrt(f) / a for metric -f dt^2 + dr^2/f + r^2 dOmega
f = 1 - 2 * M / a
rr = sp.symbols("rr", positive=True)
# n^r = sqrt(f); K_thth (mixed) = (1/r) n^r  for areal radius r
Kthth = sp.sqrt(f) / a
sigma = -(2 * Kthth) / (4 * sp.pi)
identity(sigma, -sp.sqrt(1 - 2 * M / a) / (2 * sp.pi * a))
limit(sigma, "M", 0, -1 / (2 * sp.pi * a), direction="+")
identity((4 * sp.pi * a**2 * sigma).subs(M, 0), -2 * a)
units("c^4/(2*pi*G*1 m)", "J/m^2")
quantity("c^4/(2*pi*G*1 m)", "1.926e43 J/m^2", rel_tol=2e-3)
quantity("c^4/(2*pi*G*0.1 m)", "1.926e44 J/m^2", rel_tol=2e-3)
quantity("c^4/(2*pi*G*1 um)", "1.926e49 J/m^2", rel_tol=2e-3)
quantity("2*(1 m)*c^2/G", "2.69e27 kg", rel_tol=3e-3)
C, G, HBAR = 299792458.0, 6.67430e-11, 1.054571817e-34
EA = math.pi**2 * HBAR * C / (720 * (0.2e-6)**3)
s = lambda av: C**4 / (2 * math.pi * G * av)
for av in (1.0, 0.1, 1e-6):
    print(f"a = {av:g} m: gap = {math.log10(s(av)/EA):.2f} orders")
aeq = C**4 / (2 * math.pi * G * EA)
print(f"equality a = {aeq:.3e} m; vs 4.4e26 m: {math.log10(aeq/4.4e26):.1f} orders")
quantity(f"{math.log10(s(1.0)/EA)} m/m", "50.55 m/m", rel_tol=2e-3)
quantity(f"{math.log10(s(1e-6)/EA)} m/m", "56.55 m/m", rel_tol=2e-3)
quantity(f"{aeq} m", "3.6e50 m", rel_tol=2e-2)
raise SystemExit(finish())
