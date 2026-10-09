"""M-ENGINEER-09: Schwinger-form pair-creation exponent for extremal magnetic black holes,
Gamma ~ exp(-pi M^2 c^3/(hbar q_m B)) (lens's approximation; SI magnetic charge q_m in A m, force q_m B).
With extremality mu0 q_m^2/(4 pi) = G M^2 and B = B_h = mu0 q_m/(4 pi r_e^2), r_e = G M/c^2,
the exponent equals S_BH = A/(4 lP^2) = pi r_e^2 c^3/(hbar G). At field B the exponent is S_BH B_h/B.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

M, Gs, c, mu0, hb, B = sp.symbols("M G c mu0 hbar B", positive=True)
qm = sp.sqrt(4 * sp.pi * Gs * M**2 / mu0)
re = Gs * M / c**2
Bh = mu0 * qm / (4 * sp.pi * re**2)
expo = sp.pi * M**2 * c**3 / (hb * qm * B)
SBH = 4 * sp.pi * re**2 / (4 * hb * Gs / c**3)
identity(expo.subs(B, Bh), SBH)
identity(expo, SBH * Bh / B)
limit(expo, "B", "oo", "0")   # strong-field limit: unsuppressed
units("pi*(1 kg)^2*c^3/(hbar*(1 A*m)*(1 T))", "dimensionless")
quantity("pi*(hbar*c/(1 TeV))^2*c^3/(hbar*G)", "4.68e32 m/m", rel_tol=5e-3)
quantity("pi*(1.5e7 m)^2*c^3/(hbar*G)", "2.7e84 m/m", rel_tol=1e-2)
C, G, EPS0 = 299792458.0, 6.67430e-11, 8.8541878128e-12
k = C / math.sqrt(4 * math.pi * EPS0 * G)
S_sm = math.pi * (1.973269804e-19)**2 * C**3 / (1.054571817e-34 * G)
S_mm = math.pi * (1.5e7)**2 * C**3 / (1.054571817e-34 * G)
e_sm = S_sm * (k / 1.973269804e-19) / 1200
e_mm = S_mm * (k / 1.5e7) / 1200
print(f"exponent at 1200 T: SM-MMP {e_sm:.3e}, MM {e_mm:.3e}; MM exponent/S_BH = 10^{math.log10(e_mm/S_mm):.2f}")
quantity(f"{e_sm} m/m", "6.9e66 m/m", rel_tol=1e-2)
quantity(f"{e_mm} m/m", "5.2e92 m/m", rel_tol=1e-2)
quantity("2*(hbar*c/(1 TeV))*c^2/G*c^2/(1 GeV)", "2.98e35 m/m", rel_tol=5e-3)
quantity("(hbar*c/(1 TeV))*c^2/G*c^2/(1 GeV)", "1.49e35 m/m", rel_tol=5e-3)
print(f"log10(1.49e35/75) = {math.log10(1.49e35/75):.1f}; log10(B_h/1200 T) SM = {math.log10(k/1.973269804e-19/1200):.2f}")
raise SystemExit(finish())
