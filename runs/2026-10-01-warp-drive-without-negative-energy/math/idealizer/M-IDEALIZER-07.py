"""M-IDEALIZER-07: scaling law of the linear NEC cap (F7). Geometric units.
Claim: beta_max ~ k (2M/R2)(Delta/R2), cubic profile: k = 0.18-0.37 uniform, 0.46-0.83 shaped, for
Delta/R2 in 0.09..0.9; scale-free ((10,20) and (100,200) both 0.0476 at 2M/R2 = 0.333);
-> 0 as Delta -> 0; 7e-3 at 2M/R2 = 0.05 (R2 = 2R1); 100 m payload needs M = 4.48e28 kg = 23.6 M_J.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/idealizer")
import numpy as np
from math_checks import quantity, sign, finish
from profiles import caps, KG_TO_M

Mg = 4.49e27*KG_TO_M
R2 = 20.0
comp = 2*Mg/R2
ku, ks = [], []
for f in [0.09, 0.2, 0.3, 0.5, 0.7, 0.9]:
    R1 = R2*(1 - f)
    bu, bs, bp = caps("cubic", Mg, R1, R2, nr=20000)
    ku.append(bu/(comp*f)); ks.append(bp/(comp*f))   # shaped = pointwise rho = 2|T_0i|
    print(f"Delta/R2 = {f}: beta_uni = {bu:.5f}, k_uni = {ku[-1]:.3f}; beta_shaped(sph) = {bs:.4f}, k_shaped = {ks[-1]:.3f}; pointwise {bp:.4f}")
print(f"k_uniform range {min(ku):.3f}-{max(ku):.3f} (claim 0.18-0.37); k_shaped range {min(ks):.3f}-{max(ks):.3f} (claim 0.46-0.83)")
quantity(f"{min(ku)}", "0.18", rel_tol=0.05); quantity(f"{max(ku)}", "0.37", rel_tol=0.05)
quantity(f"{min(ks)}", "0.46", rel_tol=0.05); quantity(f"{max(ks)}", "0.83", rel_tol=0.05)
# scale-free
b10 = caps("cubic", Mg, 10.0, 20.0)[0]; b100 = caps("cubic", 10*Mg, 100.0, 200.0)[0]
print(f"(10,20): {b10:.5f}; (100,200) with 10M: {b100:.5f}")
quantity(f"{b100/b10}", "1", rel_tol=1e-6)
# thin limit
bthin = [caps("cubic", Mg, R2*(1 - f), R2)[0] for f in (0.02, 0.01, 0.005)]
print("thin-wall caps:", bthin)
quantity(f"{bthin[2]/bthin[1]}", "0.5", rel_tol=0.03)
# compactness 0.05, R2 = 2 R1
Mlow = 0.05*R2/2
b05 = caps("cubic", Mlow, 10.0, 20.0)[0]
print(f"2M/R2 = 0.05: cap {b05:.5f} (claim 7e-3)")
quantity(f"{b05}", "7e-3", rel_tol=0.03)
# 100 m payload mass
M100 = 10*4.49e27
print(f"M for R1 = 100 m: {M100:.4e} kg = {M100/1.898e27:.2f} M_J (claim 4.48e28 kg, 23.6 M_J)")
quantity(f"{M100} kg", "4.48e28 kg", rel_tol=0.005)
quantity(f"{M100/1.898e27}", "23.6", rel_tol=0.005)
raise SystemExit(finish())
