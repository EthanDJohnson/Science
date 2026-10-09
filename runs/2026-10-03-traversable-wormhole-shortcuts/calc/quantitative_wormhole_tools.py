"""Quantitative facet: numbers from wormhole_tools for the Ellis throat, an MT wormhole and a thin shell,
plus Ford-Roman / Fewster-Eveson arithmetic (SI unless stated)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wormhole_tools as wt
from unit_tools import Q

C = wt.C; G = wt.G
c4G = C**4 / G
hbar = Q("hbar").si
lp = math.sqrt(hbar * G / C**3)
print("c^4/G (N) =", c4G, " Planck length (m) =", lp)

# Ellis throat, b0 = 1 m and 1 km
for b0 in (1.0, 1e3):
    th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", {"b0": b0})
    a = th.anec()
    print(f"\nEllis b0={b0} m: anec dict keys:", list(a.keys()))
    print(a)
    rho_p_geom = -1.0 / (8 * math.pi * b0**2)   # rho+p_l at throat (geom, 1/m^2): rho=-1/(8 pi b0^2)... check
    print("  analytic rho+p_l at throat (J/m^3 = Pa):", rho_p_geom * c4G, "  [ -1/(8 pi b0^2) * c^4/G ]")
    print("  I = -1/(8 b0) per unit E -> J/m^2 via c^4/G:", -1 / (8 * b0) * c4G)

# Morris-Thorne b = r0^2/r (Ellis in r form), r0 = 1 m, transit etc
mt = wt.MorrisThorne("1.0/r", "0", r0=1.0)
print("MT b=r0^2/r r0=1 m: stress", mt.stress(1.0000001), "anec", mt.anec(), "vkd", mt.vkd())
th = wt.ProperThroat("sqrt(l**2 + 1.0)", "0")
print("Ellis b0=1 stress l=0:", th.stress(0.0), th.energy_conditions(0.0))
print("Ellis transit 1 km each side v=0.01:", th.transit(-1e3, 1e3, v=0.01))
print("Ellis transit light 1 km each side:", th.transit(-1e3, 1e3, v=1.0))
print("\nMT r0=1 m methods:", [m for m in dir(mt) if not m.startswith('_')])

# Thin-shell Schwarzschild: M=1 Msun, a = 3M..10 km
Msun = Q("Msun").si
Mg = wt.mass_to_geom(Msun)
print("\nM_sun geometric (m):", Mg)
for a_m in (4.0 * Mg, 3.0 * Mg, 10e3):
    sh = wt.ThinShell.schwarzschild(M=Mg, a=a_m)
    print(f"thin shell M=1Msun a={a_m:.1f} m: surface", sh.surface(), "mass_kg", sh.mass_kg(), "anec", sh.anec())
    print("   ec", sh.energy_conditions())

# Ford-Roman arithmetic
print("\n1e4 lp =", 1e4 * lp, "m")
f = 0.01
print("r0 <~ lp/(2 f^2) with f=0.01: =", lp / (2 * f**2), "m  (", 1/(2*f**2), "lp)")
for r0, label in ((1.0, "1 m"),):
    a0 = (r0 / (8 * f**4 * lp))**(1/3) * lp
    print("FR a0 bound r0=1 m, f=0.01:", a0, "m =", a0/lp, "lp")
ly = 9.4607e15
r0 = ly; a0 = (r0 / (8 * f**4 * lp))**(1/3) * lp
print("r0=1 ly:", a0, "m", a0/lp, "lp")
r0 = 1e5 * ly; a0 = (r0 / (8 * f**4 * lp))**(1/3) * lp
print("r0=1e5 ly:", a0, "m", a0/lp, "lp")

# Fewster-Eveson vs Ford-Roman Lorentzian, 4D massless
print("\nLorentzian FR coefficient 3/(32 pi^2) =", 3/(32*math.pi**2), " FE 27/(2048 pi^2) =", 27/(2048*math.pi**2), " ratio =", (27/2048)/(3/32), " 9/64 =", 9/64)
# QI energy density scale for tau0 = 1 s, in J/m^3 : rho >= -(27/(2048 pi^2)) hbar/(c^3 tau0^4) (SI restoring hbar c)
for tau in (1e-15, 1e-9, 1.0):
    rho = 27/(2048*math.pi**2) * hbar / (C**3 * tau**4) * C**0  # J/m^3 = hbar/(c^3 tau^4)
    print(f"Fewster-Eveson Lorentzian bound, tau0={tau} s: rho >= -{rho:.3e} J/m^3 (|rho|c^-2 = {rho/C**2:.3e} kg/m^3)")
