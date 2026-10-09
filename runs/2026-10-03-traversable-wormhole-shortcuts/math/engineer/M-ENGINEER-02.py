"""M-ENGINEER-02: Ellis throat energy density, exotic-mass quantifier, Casimir anchors and gaps.
Ellis-Bronnikov: b(r) = b0^2/r, Phi = 0. Geometric units: rho = b'/(8 pi r^2), p_r = -b/(8 pi r^3).
SI: energy density = c^4/G times geometric (1/m^2). Casimir ideal plates, gap a:
u = -pi^2 hbar c/(720 a^4), E/A = -pi^2 hbar c/(720 a^3).
Omega = 2 * int_{b0}^oo (rho + p_r) 4 pi r^2 dr (Visser-Kar-Dadhich, coordinate volume, two sheets).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, quantity, units, finish

r, b0 = sp.symbols("r b0", positive=True)
b = b0**2 / r
rho = sp.diff(b, r) / (8 * sp.pi * r**2)
pr = -b / (8 * sp.pi * r**3)
identity(rho.subs(r, b0), -1 / (8 * sp.pi * b0**2))
Omega = 2 * sp.integrate((rho + pr) * 4 * sp.pi * r**2, (r, b0, sp.oo))
identity(Omega, -2 * b0)
# rho integral alone (both sheets) = -b0
identity(2 * sp.integrate(rho * 4 * sp.pi * r**2, (r, b0, sp.oo)), -b0)
# flat limit: density at the throat vanishes as b0 -> oo
limit(-1 / (8 * sp.pi * b0**2), "b0", "oo", "0")

units("c^4/(8*pi*G*(1 m)^2)", "pressure or energy density")
quantity("c^4/(8*pi*G*(1 m)^2)", "4.815e42 J/m^3", rel_tol=2e-3)
quantity("c^4/(8*pi*G*(0.1 m)^2)", "4.815e44 J/m^3", rel_tol=2e-3)
quantity("c^4/(8*pi*G*(1 um)^2)", "4.815e54 J/m^3", rel_tol=2e-3)
quantity("2*(1 m)*c^2/G", "2.69e27 kg", rel_tol=3e-3)
quantity("2*(1 um)*c^2/G", "2.69e21 kg", rel_tol=3e-3)
quantity("2*(1.5e7 m)*c^2/G", "4.04e34 kg", rel_tol=3e-3)
quantity("c^4/(8*pi*G*(1.5e7 m)^2)", "2.14e28 J/m^3", rel_tol=3e-3)
# Casimir anchors at 0.2 um
quantity("pi^2*hbar*c/(720*(0.2 um)^4)", "0.271 J/m^3", rel_tol=3e-3)
quantity("pi^2*hbar*c/(240*(0.2 um)^4)", "0.813 Pa", rel_tol=3e-3)
quantity("pi^2*hbar*c/(720*(0.2 um)^3)", "5.42e-8 J/m^2", rel_tol=3e-3)

C, G, HBAR = 299792458.0, 6.67430e-11, 1.054571817e-34
u02 = math.pi**2 * HBAR * C / (720 * (0.2e-6)**4)
u10nm = math.pi**2 * HBAR * C / (720 * (10e-9)**4)
EA02 = math.pi**2 * HBAR * C / (720 * (0.2e-6)**3)
rho = lambda b0v: C**4 / (8 * math.pi * G * b0v**2)
for b0v in (1.0, 0.1, 1e-6, 1.5e7):
    print(f"b0 = {b0v:g} m: gap vs Casimir 0.2 um = {math.log10(rho(b0v)/u02):.2f}, vs 10 nm = {math.log10(rho(b0v)/u10nm):.2f}")
beq = math.sqrt(C**4 / (8 * math.pi * G * u02))
print(f"equality radius b0 = {beq:.3e} m = {beq/(C*365.25*86400):.3e} ly")
area = 2 * 1.0 * C**2 / G * C**2 / EA02
print(f"plate area for |Omega| c^2 at b0 = 1 m: {area:.3e} m^2; vs Earth surface 5.1e14 m^2: {math.log10(area/5.1e14):.1f} orders")
quantity(f"{math.log10(rho(1.0)/u02)} m/m", "43.25 m/m", rel_tol=2e-3)
quantity(f"{math.log10(rho(1e-6)/u02)} m/m", "55.25 m/m", rel_tol=2e-3)
quantity(f"{math.log10(rho(1.0)/u10nm)} m/m", "38.05 m/m", rel_tol=3e-3)
quantity(f"{beq} m", "4.2e21 m", rel_tol=1e-2)
quantity(f"{area} m^2", "4.5e51 m^2", rel_tol=2e-2)
raise SystemExit(finish())
