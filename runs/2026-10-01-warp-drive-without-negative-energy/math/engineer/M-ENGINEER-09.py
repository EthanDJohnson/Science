"""M-ENGINEER-09 (F14, ENGINEER-A): negative-energy gaps.
Casimir parallel plates: u = -pi^2 hbar c/(720 a^4); a = 0.1 um => -4.3 J/m^3; 1 m^2 => -4.3e-7 J.
Alcubierre Eulerian density (Alcubierre 1994 eq. 19, quoted): rho = -(c^4/8 pi G)(v^2 y_perp^2/(4 r^2)) f'(r)^2;
tanh profile f = [tanh(s(r+R)) - tanh(s(r-R))]/(2 tanh(sR)), D-28 convention Delta = 2/s.
Peak at y_perp = r, f'max -> s/2 = 1/Delta: |rho|max = v^2 c^4/(32 pi G Delta^2): 1.2e42 J/m^3 (1c), 1.2e44 (10c),
R = 100 m, Delta = 1 m. Gaps vs 4.3 J/m^3: 41.4, 43.4. Totals (D-28/D-34/D-29 values, quoted; arithmetic only):
6.72e48 J -> 55.2; 5.38e50 J -> 57.1; Rodal 1.3e44 J -> 50.5; QI wall -> 87.2. Against 5.9e20 J/yr: 23-30, 60.
QI wall Delta = 100 v L_P = 1.6e-32 m at v = 10 (D-29): 12.0 orders below 1.45e-20 m, 21.8 below 1 A."""
import sys
import sympy as sp
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, quantity, units, finish

u = math.pi**2 * hbar * c / (720 * (1e-7)**4)
near("Casimir |u| at 0.1 um (J/m^3)", u, 4.3, 0.05)
quantity("pi^2*hbar*c/(720*(0.1 um)^4)", "4.33 J/m^3", rel_tol=0.01)
# Casimir limit: u -> 0 as a -> oo
limit("pi**2*h*k/(720*a**4)", "a", "oo", "0")
# Alcubierre peak density, tanh wall, numerically
R, Delta = 100.0, 1.0
s = 2 / Delta
r = np.linspace(R - 10, R + 10, 400001)
fp = (s / np.cosh(s * (r + R))**2 - s / np.cosh(s * (r - R))**2) / (2 * np.tanh(s * R))
fpmax = np.max(np.abs(fp))
print(f"  max |f'| = {fpmax:.6f} 1/m (expected 1/Delta = {1/Delta})")
for v, claim in ((1, 1.2e42), (10, 1.2e44)):
    rho = v**2 * fpmax**2 / (32 * math.pi) * c**4 / G
    rel(f"peak |rho| at v = {v}c (J/m^3)", rho, claim, 0.02)
    near(f"density gap at v = {v}c", lg(rho / u), 41.4 if v == 1 else 43.4, 0.05)
units("c^4/G/(1 m^2)", "J/m^3")
# D-28 closed form (tanh) E = v^2 R^2 c^4/(18 G Delta) -- arithmetic check of the quoted value
E10 = 100 * R**2 / (18 * Delta) * c**4 / G
rel("Alcubierre 10c total (J), from D-28 closed form", E10, 6.72e48, 0.01)
near("gap Alcubierre 10c vs 1 m^2 cavity", lg(6.72e48 / (u * 1e-7)), 55.2, 0.05)
near("gap Natario 1c (5.38e50 J)", lg(5.38e50 / (u * 1e-7)), 57.1, 0.05)
near("gap Rodal (1.3e44 J)", lg(1.3e44 / (u * 1e-7)), 50.5, 0.05)
lP = math.sqrt(hbar * G / c**3)
dQI = 100 * 10 * lP
rel("QI wall at 10c (m)", dQI, 1.6e-32, 0.02)
E_qi_tanh = E10 * Delta / dQI
E_qi_ramp = 6.9e63 * c**2
print(f"  QI-wall total: tanh scaling {E_qi_tanh:.3g} J (gap {lg(E_qi_tanh/(u*1e-7)):.2f}); linear-ramp D-29 6.9e63 kg = {E_qi_ramp:.3g} J (gap {lg(E_qi_ramp/(u*1e-7)):.2f})")
near("QI gap (linear-ramp D-29 value)", lg(E_qi_ramp / (u * 1e-7)), 87.2, 0.05)
near("QI gap (tanh convention, same as the 55.2 row)", lg(E_qi_tanh / (u * 1e-7)), 87.2, 0.25)
for lab, E, lo, hi in (("Alcubierre 10c", 6.72e48, 23, 30), ("Natario 1c", 5.38e50, 23, 30.05), ("Rodal", 1.3e44, 23, 30)):
    g = lg(E / WORLD_YR)
    print(f"  {lab} vs world-year: {g:.2f} orders")
    inequality(repr(g), ">=", repr(lo)); inequality(repr(g), "<=", repr(hi))
near("QI wall vs world-year", lg(E_qi_ramp / WORLD_YR), 60, 0.1)
near("QI wall vs LHC 1.45e-20 m", lg(1.45e-20 / dQI), 12.0, 0.05)
near("QI wall vs 1 Angstrom", lg(1e-10 / dQI), 21.8, 0.05)
raise SystemExit(finish())
