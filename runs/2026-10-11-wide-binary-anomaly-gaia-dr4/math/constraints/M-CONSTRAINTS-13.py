"""M-CONSTRAINTS-13 (F15, F17): Galactic tide and GR scales (SI via unit_tools).

Jacobi radius r_J = (G M / (4 A (A - B)))^(1/3), A = 15.3, B = -11.9 km/s/kpc (assumed by lens), M = 1.5 Msun.
In-plane tidal/internal ratio at r: 4A(A-B) r^3/(GM) = (r/r_J)^3. Vertical: 4 pi G rho0 r^3/(G M), rho0 = 0.1 Msun/pc^3.
GR: G M/(r c^2), v_c/c at r = 10 kau.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

T = "(4*15.3*(15.3+11.9)*(1 km/s/kpc)^2)"
quantity(f"(G*1.5*Msun/{T})^(1/3)", "324000 au", rel_tol=3e-3)
quantity(f"(G*1.5*Msun/{T})^(1/3)", "1.57 pc", rel_tol=3e-3)
units(f"{T}*(10000 au)^3/(G*1.5*Msun)", "dimensionless")
for r, lin, lvert in [(10000, 2.9e-5, 9.6e-5), (30000, 7.9e-4, 2.6e-3)]:
    quantity(f"{T}*({r} au)^3/(G*1.5*Msun)", f"{lin}", rel_tol=2e-2)
    quantity(f"4*3.14159265*0.1*Msun/pc^3*({r} au)^3/(1.5*Msun)", f"{lvert}", rel_tol=2e-2)
quantity("G*1.5*Msun/(10000 au*c^2)", "1.5e-12", rel_tol=3e-2)
quantity("(G*1.5*Msun/(10000 au))^(1/2)/c", "1.2e-6", rel_tol=3e-2)
raise SystemExit(finish())
