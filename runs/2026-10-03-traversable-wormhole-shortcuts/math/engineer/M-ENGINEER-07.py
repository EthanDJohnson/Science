"""M-ENGINEER-07: formation mass-energy 2 M c^2 (M = r_e c^2/G, extremal) against world primary energy
592 EJ/yr (quoted anchor); MM world-energy gap; 592 EJ as mass.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, identity, limit, finish

units("2*(1 m)*c^4/G", "energy")
quantity("2*(hbar*c/(1 TeV))*c^4/G", "4.78e25 J", rel_tol=3e-3)
quantity("2*(hbar*c/(1 TeV))*c^4/G/(592 EJ/yr)", "8.07e4 yr", rel_tol=3e-3)
quantity("592 EJ/c^2", "6.59e3 kg", rel_tol=3e-3)
quantity("(1.5e7 m)*c^2/G", "2.02e34 kg", rel_tol=3e-3)
quantity("(1.5e7 m)*c^2/G/Msun", "1.02e4 m/m", rel_tol=1e-2)
quantity("2*(1.5e7 m)*c^4/G", "3.63e51 J", rel_tol=3e-3)
quantity("2*(1.5e7 m)*c^4/G/(592 EJ/yr)", "6.1e30 yr", rel_tol=1e-2)
C, G = 299792458.0, 6.67430e-11
y_sm = 2 * 1.973269804e-19 * C**4 / G / 592e18
y_mm = 2 * 1.5e7 * C**4 / G / 592e18
print(f"log10 years: SM-MMP {math.log10(y_sm):.2f}, MM {math.log10(y_mm):.2f}")
quantity(f"{math.log10(y_sm)} m/m", "4.9 m/m", rel_tol=5e-3)
quantity(f"{math.log10(y_mm)} m/m", "30.8 m/m", rel_tol=2e-3)
raise SystemExit(finish())
