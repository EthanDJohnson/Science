"""M-IDEALIZER-10: chirp yields (F8). SI. P = (12 pi/25)(G^2/c^10) Int w L^2 dt = (12 pi/25)(G^2/c^10) Int w L |dE|,
Newtonian quadrupole chirp: L = (32/5)(c^5/G)(G Mc Om/c^3)^(10/3), E_orb = -(1/2) Mc (G Mc Om)^(2/3), w = 2 Om, Om = pi f_GW.
Own derivation of E_orb: E = -G m1 m2/(2a), a^3 = G M/Om^2 -> E = -(1/2) mu (G M Om)^(2/3), mu M^(2/3) = Mc^(5/3).
Claims: integrand proportional to Om^4; GW170817 (Mc = 1.188 Msun, 30-1600 Hz) 2.8e-8; GW150914 inspiral (Mc = 28 Msun,
35-68 Hz) 2.8e-8; WD binary (Mc = 0.3 Msun, 6.2 mHz) L = 1.7e28 W and 4e-43 pairs per year.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, finish
import sympy as sp

Gs, Mc, Om, cs, m1, m2 = sp.symbols("G M_c Omega c m1 m2", positive=True)
# binding energy identity
M = m1 + m2; mu = m1 * m2 / M; Mch = (m1 * m2)**sp.Rational(3, 5) / M**sp.Rational(1, 5)
identity(-Gs * m1 * m2 / (2 * (Gs * M / Om**2)**sp.Rational(1, 3)), -sp.Rational(1, 2) * Mch * (Gs * Mch * Om)**sp.Rational(2, 3))
Eorb = -sp.Rational(1, 2) * Mc * (Gs * Mc * Om)**sp.Rational(2, 3)
Lq = sp.Rational(32, 5) * cs**5 / Gs * (Gs * Mc * Om / cs**3)**sp.Rational(10, 3)
integrand = sp.simplify(2 * Om * Lq * sp.diff(-Eorb, Om) * (-1))   # w L |dE/dOm| (E decreases as Om grows)
integrand = sp.simplify(2 * Om * Lq * sp.Abs(sp.diff(Eorb, Om)))
print("w L |dE/dOm| =", integrand)
identity(sp.simplify(Om * sp.diff(sp.log(integrand), Om)), 4)     # proportional to Om^4

G, c, Msun, yr = 6.67430e-11, 299792458.0, 1.98841e30, 3.15576e7
coef = sp.lambdify((Gs, cs, Mc), sp.simplify(integrand / Om**4))
def P_chirp(mc, flo, fhi):
    Olo, Ohi = math.pi * flo, math.pi * fhi
    return 12 * math.pi / 25 * G**2 / c**10 * coef(G, c, mc * Msun) * (Ohi**5 - Olo**5) / 5
for name, mc, flo, fhi, lens in (("GW170817", 1.188, 30, 1600, 2.8e-8), ("GW150914 inspiral", 28.0, 35, 68, 2.8e-8)):
    p = P_chirp(mc, flo, fhi)
    print(f"{name}: P = {p:.4e} pairs (lens {lens})")
    quantity(f"{p}", f"{lens}", rel_tol=3e-2)
O = math.pi * 6.2e-3
L = 32 / 5 * c**5 / G * (G * 0.3 * Msun * O / c**3)**(10 / 3)
Pyr = 12 * math.pi / 25 * G**2 * 2 * O * L**2 * yr / c**10
print(f"WD binary: L = {L:.4e} W, P = {Pyr:.4e} per yr")
quantity(f"{L} W", "1.7e28 W", rel_tol=2e-2); quantity(f"{Pyr}", "4.1e-43", rel_tol=2e-2)
quantity("32/5 * c^5/G * (G * 0.3 Msun * 0.019478 /s / c^3)^(10/3)", "1.7e28 W", rel_tol=2e-2)   # units of L
raise SystemExit(finish())
