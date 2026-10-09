"""M-ENGINEER-05: MMP with Standard-Model fields, SI numbers.
Inputs (lens assumptions): r_e = hbar c/(1 TeV); g = 0.06 (0.3 for sensitivity); N = 1 or 54.
Relations (natural units, re-derived in M-ENGINEER-01): q = g r_e/(sqrt(pi) lP); M = r_e c^2/G (extremal);
l = 16 r_e^3/(lP^2 q N); |E_min| = N^2 g^2 hbar c/(256 pi r_e); T < hbar c/(2 pi l kB); validity l/(q^3 lP).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, identity, finish

HBAR, C, G, KB, EV = 1.054571817e-34, 299792458.0, 6.67430e-11, 1.380649e-23, 1.602176634e-19
LP = math.sqrt(HBAR * G / C**3)
re = HBAR * C / (1e12 * EV)
print(f"r_e = {re:.4e} m")
out = {}
for g in (0.06, 0.3):
    q = g * re / (math.sqrt(math.pi) * LP)
    for N in (1, 54):
        l = 16 * re**3 / (LP**2 * q * N)
        Em = N**2 * g**2 * HBAR * C / (256 * math.pi * re)
        T = HBAR * C / (2 * math.pi * l * KB)
        out[(g, N)] = (q, l, Em, T)
        print(f"g={g}, N={N}: q={q:.3e}, l={l:.4g} m, |E_min|={Em:.3e} J = {Em/EV/1e6:.4g} MeV, T<{T*1e3:.3g} mK, l/(q^3 lP)={l/(q**3*LP):.2e}")
# cross-check l by the closed form 16 pi^1.5 q^2 lP/(g^3 N)
q06 = out[(0.06, 1)][0]
quantity(f"{16*math.pi**1.5*q06**2*LP/0.06**3} m", f"{out[(0.06,1)][1]} m", rel_tol=1e-9)
quantity(f"{q06} m/m", "4.1e14 m/m", rel_tol=2e-2)
quantity(f"{out[(0.3,1)][0]} m/m", "2.1e15 m/m", rel_tol=2e-2)
quantity("(hbar*c/(1 TeV))*c^2/G", "2.66e8 kg", rel_tol=3e-3)
quantity(f"{out[(0.06,1)][1]} m", "1.14 m", rel_tol=1e-2)
quantity(f"{out[(0.06,54)][1]} m", "0.021 m", rel_tol=2e-2)
quantity(f"{out[(0.06,1)][2]} J", "7.2e-13 J", rel_tol=1e-2)
quantity(f"{out[(0.06,54)][2]} J", "2.1e-9 J", rel_tol=1e-2)
quantity(f"{out[(0.3,54)][2]} J", "5.2e-8 J", rel_tol=1e-2)
quantity(f"{out[(0.06,1)][3]} K", "0.3 mK", rel_tol=0.1)
quantity(f"{out[(0.06,54)][3]} K", "17 mK", rel_tol=3e-2)
quantity(f"{out[(0.3,54)][3]} K", "86 mK", rel_tol=3e-2)
v = out[(0.06, 1)][1] / (out[(0.06, 1)][0]**3 * LP)
quantity(f"{v} m/m", "1e-9 m/m", rel_tol=0.1)
units("hbar*c/(2*pi*1 m*kB)", "temperature")
# 1 kg payload gap against the best SM case (g = 0.06, N = 54) and size gap 0.1 m vs r_e
gapE = math.log10(1 * C**2 / out[(0.06, 54)][2]); gapE1 = math.log10(C**2 / out[(0.06, 1)][2])
print(f"1 kg gap: {gapE:.2f} orders (N=54, g=0.06); {gapE1:.2f} (N=1); size gap log10(0.1 m/r_e) = {math.log10(0.1/re):.2f}")
quantity(f"{gapE} m/m", "25.6 m/m", rel_tol=5e-3)
quantity(f"{math.log10(0.1/re)} m/m", "17.7 m/m", rel_tol=5e-3)
raise SystemExit(finish())
