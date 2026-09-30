"""M-CONSTRAINTS-14: Diosi-Penrose numbers for QGEM and the DP heating formula (SI).

Uniform sphere mass m, radius R, displaced by d >= 2R. With I = int int rho(r) rho(r')/|r-r'|:
  I_self = 6 m^2/(5R) (from U_self = -3 G m^2/(5R) = -(G/2) I_self), I_mutual(d) = m^2/d.
  Penrose's E_G = (G/2) int int (rho1-rho2)(rho1'-rho2')/|r-r'| = (G/2)(2 I_self - 2 I_mutual) = G m^2 (6/(5R) - 1/d);
  the other common convention (G, not G/2) doubles it. Claim (F14): E_G = (1 to 2) x G m^2 (6/(5R) - 1/dx) = 0.9-1.8e-32 J,
  tau = hbar/E_G = 6-12 ms, for m = 1e-14 kg, R = 0.88 um (diamond, rho = 3510 kg/m^3), dx = 250 um.
Granular term with per-nucleus smearing R0 = 0.54e-10 m: N G m_a^2 (6/(5 R0)), claim ~3e-40 J.
Heating (dossier Q-04): dT/dt = 4 sqrt(pi) m0 G hbar/(3 kB R0^3); claim 2.0e-3 K/s at R0 = 1e-15 m (not 1e-4), 1.3e-17 K/s at 0.54e-10 m.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

# Self-energy of uniform sphere: U = -int_0^R G M(r) dm / r
r, R, m, Gs = sp.symbols("r R m G", positive=True)
Mr = m * r**3 / R**3
U = -sp.integrate(Gs * Mr * (3 * m * r**2 / R**3) / r, (r, 0, R))
identity(U, -3 * Gs * m**2 / (5 * R))
d = sp.symbols("d", positive=True)
EG = (Gs / 2) * (2 * (-2 * U / Gs) - 2 * m**2 / d)
identity(EG, Gs * m**2 * (sp.Rational(6, 5) / R - 1 / d))
limit(EG.subs(d, 2 * R), "R", sp.oo, "0")   # large-body limit sanity: E_G -> 0 as R -> oo at d = 2R
# numbers
quantity("(3*1e-14 kg/(4*pi*3510 kg/m^3))^(1/3)", "0.88 um", rel_tol=0.01)
Rs = "(3*1e-14 kg/(4*pi*3510 kg/m^3))^(1/3)"
EGs = f"G*(1e-14 kg)^2*(1.2/{Rs} - 1/(250 um))"
units(EGs, "energy")
quantity(EGs, "0.9e-32 J", rel_tol=0.03)
quantity(f"2*{EGs}", "1.8e-32 J", rel_tol=0.03)
quantity(f"hbar/({EGs})", "12 ms", rel_tol=0.05)
quantity(f"hbar/(2*{EGs})", "6 ms", rel_tol=0.05)
# granular term: N = m/(12.011 u) atoms, each smeared over R0
quantity("(1e-14 kg/(12.011 amu)) * G * (12.011 amu)^2 * 1.2/(0.54e-10 m)", "3e-40 J", rel_tol=0.05)
# heating formula: nucleon mass
heat = "4*pi^0.5*mp*G*hbar/(3*kB*({R0})^3)"
units(heat.format(R0="1e-15 m"), "K/s")
quantity(heat.format(R0="1e-15 m"), "2.0e-3 K/s", rel_tol=0.02)
quantity(heat.format(R0="0.54e-10 m"), "1.3e-17 K/s", rel_tol=0.03)
raise SystemExit(finish())
