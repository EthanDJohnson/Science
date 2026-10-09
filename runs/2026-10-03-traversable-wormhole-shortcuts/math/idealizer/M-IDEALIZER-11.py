"""M-IDEALIZER-11: Ford-Roman QI applied to a throat and to a thin band (arithmetic on a quoted inequality).

Quoted input (not re-derived): flat-space QI for a massless scalar with Lorentzian sampling of length s:
  rho_bar >= -3 hbar c / (32 pi^2 s^4).
Uniform throat: |rho| = c^4/(8 pi G r0^2) sampled over s = f r0.
Thin band of width w carrying the same column (|rho| r0 per area): |rho_b| = c^4/(8 pi G r0 w), sampled over s = f w.
Claims: r0 <= sqrt(3/(4 pi)) l_P / f^2 (0.489 l_P at f = 1; 4.9e3 l_P at f = 0.01);
        w <= (3 r0/(4 pi f^4 l_P))^(1/3) l_P (1.84e-21 m at r0 = 1 m, f = 0.01); band density 2.6e63 J/m^3;
        6e58 x ideal 10 nm Casimir density; 37 orders at r0 = 1 ly.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

hbar, c, G, r0, f, w = sp.symbols("hbar c G r0 f w", positive=True)
lP = sp.sqrt(hbar * G / c**3)
qi = 3 * hbar * c / (32 * sp.pi**2)
# uniform throat: c^4/(8 pi G r0^2) = qi/(f r0)^4 at the limit
r0max = sp.solve(sp.Eq(c**4 / (8 * sp.pi * G * r0**2), qi / (f * r0)**4), r0)[0]
identity(r0max, sp.sqrt(3 / (4 * sp.pi)) * lP / f**2)
# band
wmax = sp.solve(sp.Eq(c**4 / (8 * sp.pi * G * r0 * w), qi / (f * w)**4), w)[0]
identity(wmax, (3 * r0 / (4 * sp.pi * f**4 * lP))**sp.Rational(1, 3) * lP)
# limit: band as thick as the throat recovers the uniform bound (w = r0 <=> r0 = r0max)
identity(wmax.subs(r0, r0max), r0max)
units("c^4 / (G * 1 m^2)", "J/m^3")
print("sqrt(3/4pi) =", math.sqrt(3 / (4 * math.pi)))
identity(sp.N(sp.sqrt(3 / (4 * sp.pi)), 4), sp.Float(0.4886, 4))
lp = 1.616255e-35
wv = (3 * 1.0 / (4 * math.pi * 0.01**4 * lp))**(1 / 3) * lp
print("w at r0 = 1 m, f = 0.01:", wv, "m")
quantity(f"{wv} m", "1.84e-21 m", rel_tol=0.01)
quantity(f"c^4 / (8 * {math.pi} * G * 1 m * {wv} m)", "2.6e63 J/m^3", rel_tol=0.02)
cas = f"{math.pi**2/720} * hbar * c / (10 nm)^4"
quantity(cas, "4.33e4 J/m^3", rel_tol=0.01)
ratio = (2.62e63) / (math.pi**2 / 720 * 1.054571817e-34 * 299792458.0 / 1e-32)
print("band density / Casimir(10 nm) at r0 = 1 m:", f"{ratio:.3e}")
quantity(f"{ratio}", "6e58", rel_tol=0.03)
# r0 = 1 ly: w ~ r0^(1/3), density ~ 1/(r0 w) ~ r0^(-4/3)
ly = 9.4607304725808e15
dens_ly = 2.62e63 * ly**(-4 / 3)
print("band density at r0 = 1 ly:", f"{dens_ly:.3e}", "J/m^3; orders above Casimir:", math.log10(dens_ly / 4.33e4))
quantity(f"{math.floor(math.log10(dens_ly / 4.33e4))}", "37", rel_tol=1e-9)
raise SystemExit(finish())
