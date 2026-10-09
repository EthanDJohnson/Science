"""M-ENGINEER-06: horizon magnetic field of an extremal magnetically charged RN black hole, SI.
Magnetic charge q_m (A m), B = mu0 q_m/(4 pi r^2). Extremality (duality with Q^2/(4 pi eps0) = G M^2,
Q = q_m/c): mu0 q_m^2/(4 pi) = G M^2. Horizon r_e = G M/c^2. Then B_h = c/(sqrt(4 pi eps0 G) r_e).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

M, Gs, c, mu0, re = sp.symbols("M G c mu0 r_e", positive=True)
eps0 = 1 / (mu0 * c**2)
qm = sp.sqrt(4 * sp.pi * Gs * M**2 / mu0)
Bh = (mu0 * qm / (4 * sp.pi * re**2)).subs(M, re * c**2 / Gs)
identity(Bh, c / (sp.sqrt(4 * sp.pi * eps0 * Gs) * re))
# limit: field vanishes for large holes (B_h ~ 1/r_e)
limit(Bh, "r_e", "oo", "0")
units("c/((4*pi*eps0*G)^0.5*1 m)", "T")
quantity("c/((4*pi*eps0*G)^0.5*(hbar*c/(1 TeV)))", "1.76e37 T", rel_tol=5e-3)
quantity("c/((4*pi*eps0*G)^0.5*(1.5e7 m))", "2.3e11 T", rel_tol=1e-2)
B = 299792458.0 / math.sqrt(4 * math.pi * 8.8541878128e-12 * 6.67430e-11)
print(f"B_h r_e = {B:.4e} T m; MM: {B/1.5e7:.3e} T, log10(/1200 T) = {math.log10(B/1.5e7/1200):.2f}")
quantity(f"{math.log10(B/1.5e7/1200)} m/m", "8.3 m/m", rel_tol=5e-3)
raise SystemExit(finish())
