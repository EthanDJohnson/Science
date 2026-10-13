"""M-CONSTRAINTS-11: ISCO masses, Hawking ratio, evaporation (F11). SI.
ISCO GW angular frequency w = 0.136 c^3/(G M) (lens input); M(hbar w) = 0.136 c^3 hbar/(G hbar w).
W_gamma = (6/(25 pi)) G^2 hbar E^2 w^2 sigma^2/c^10 (M-CONSTRAINTS-04); W_H = hbar c^6/(15360 pi G^2 M^2) (lens input).
Claim: W_H/W_gamma independent of M when E = e M c^2, w = a c^3/(G M), sigma = eps w. Value 341 for one 65 Msun BH,
GW150914 inputs (E = 3 Msun c^2, f = 150 Hz, sigma = 200 /s); two components (M/2 each) give x8 = 2.7e3.
Hawking temperature kT = hbar c^3/(8 pi G M_comp k), M_comp = M/2. Evaporation t = 5120 pi G^2 M_comp^3/(hbar c^4).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, finish

G, c, hbar, eV, Msun = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19, 1.98841e30
Gs, cs, hb, M, ee, a, eps = sp.symbols("G c hbar M e_frac a eps", positive=True)
E = ee * M * cs**2
w = a * cs**3 / (Gs * M)
Wg = sp.Rational(6, 25) / sp.pi * Gs**2 * hb * E**2 * w**2 * (eps * w)**2 / cs**10
WH = hb * cs**6 / (15360 * sp.pi * Gs**2 * M**2)
identity(sp.diff(sp.simplify(WH / Wg), M), 0)
for EeV, want in [(10, 3.6e18), (2.2e6, 1.6e13), (19.8e6, 1.8e12), (1e10, 3.6e9)]:
    m = 0.136 * c**3 * hbar / (G * EeV * eV)
    Mc = m / 2
    TH = hbar * c**3 / (8 * math.pi * G * Mc) / eV
    tev = 5120 * math.pi * G**2 * Mc**3 / (hbar * c**4)
    print(f"{EeV:g} eV: M={m:.3e} kg, component T_H={TH:.3g} eV, evaporation={tev:.3e} s = {tev/4.36e17:.2e} t_H")
    quantity(f"{m}", f"{want}", rel_tol=0.03)
    if EeV == 1e10:
        quantity(f"{tev/4.36e17}", "1.1e-6", rel_tol=0.05)
    if EeV == 10:
        quantity(f"{TH}", "5.9", rel_tol=0.03)
# GW150914-type ratio
Mtot = 65 * Msun
Ebar = 3 * Msun * c**2
wg = 2 * math.pi * 150
Wgam = 6 / (25 * math.pi) * G**2 * hbar * Ebar**2 * wg**2 * 200.0**2 / c**10
WH1 = hbar * c**6 / (15360 * math.pi * G**2 * Mtot**2)
print("W_gamma =", Wgam, "W ; W_H(65 Msun) =", WH1, "W ; ratio =", WH1 / Wgam, "; two components:", 8 * WH1 / Wgam)
quantity(f"{WH1/Wgam}", "341", rel_tol=0.03)
quantity(f"{8*WH1/Wgam}", "2.7e3", rel_tol=0.03)
raise SystemExit(finish())
