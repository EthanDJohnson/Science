"""M-EXAMINER-07: r_s-free H0 (D-49) and equality-scale H0 (D-50) against SH0ES and CMB-SPA (F7).
z with facing-side errors. Claim: D-49 1.90-3.50 sigma below SH0ES, 0.27-2.47 from CMB-SPA; D-50 0.76-2.67 below SH0ES.
Separation claim: a measurement with sigma = 1.0 separates point hypotheses 73.3 and 67.5 at (73.3-67.5)/1.0 = 5.8 sigma, 1.5%."""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from common import *
from math_checks import identity, quantity, finish

zs = [z_facing(v, SH0ES) for v in RSFREE.values()]
zc = [z_facing(v, CMB) for v in RSFREE.values()]
for (k, v), a, b in zip(RSFREE.items(), zs, zc):
    print(f"{k} {v}: vs SH0ES {a:.3f} (sym {z_sym(v, SH0ES):.3f}), vs CMB-SPA {b:.3f} (sym {z_sym(v, CMB):.3f})")
print("D-49 range vs SH0ES", min(zs), max(zs), "; vs CMB-SPA", min(zc), max(zc))
quantity(f"{min(zs)}", "1.90", rel_tol=3e-3); quantity(f"{max(zs)}", "3.50", rel_tol=3e-3)
quantity(f"{min(zc)}", "0.27", rel_tol=1.5e-2)  # 0.2732 rounds to 0.27
quantity(f"{max(zc)}", "2.47", rel_tol=3e-3)
ze = [z_facing(EQ["EQ-Pantheon"], SH0ES), z_facing(EQ["EQ-BAOlens"], SH0ES)]
print("D-50 vs SH0ES", ze)
quantity(f"{ze[0]}", "2.67", rel_tol=3e-3); quantity(f"{ze[1]}", "0.76", rel_tol=6e-3)
quantity("(73.3 - 67.5)/1.0", "5.8", rel_tol=1e-9)
quantity("100*1.0/67.5", "1.5", rel_tol=2e-2)
raise SystemExit(finish())
