"""M-DECOMPOSER-07: required r_d and M_B differences (F7).

BAO fixes the product H0 r_d. Holding it fixed: r_d(H) = r_d,ref * H_ref / H.
CMB-SPA: H_ref = 67.19 km/s/Mpc, r_d = 147.00 Mpc. DESI DR2: h r_d = 101.54 Mpc -> r_d = 101.54/(H/100).
M_B difference: ladder R22 -19.253 minus inverse-ladder -19.375 / -19.394 mag.
"""
import sys
import math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import num, finish, identity, units, quantity

for H, rd_l, pc_l, pcd_l, rdd_l in [(73.26, 134.8, 8.3, 5.7, 138.6), (70.39, None, 4.6, 1.9, None)]:
    rd = 147.00 * 67.19 / H
    rdd = 101.54 / (H / 100)
    if rd_l:
        num(f"r_d (CMB-SPA product) at H={H} [Mpc]", rd, rd_l, 0.06)
        num(f"r_d (DESI h r_d) at H={H} [Mpc]", rdd, rdd_l, 0.06)
    num(f"fractional reduction vs 147.00 (CMB-SPA) at H={H} [%]", 100 * (1 - rd / 147.00), pc_l, 0.06)
    num(f"fractional reduction vs 147.00 (DESI) at H={H} [%]", 100 * (1 - rdd / 147.00), pcd_l, 0.06)

num("Delta M_B ladder - inverse (cosmography) [mag]", -19.253 - (-19.375), 0.122, 0.0006)
num("Delta M_B ladder - inverse (flat LCDM) [mag]", -19.253 - (-19.394), 0.141, 0.0006)
# the two are 'comparable but not commensurate' with the 0.188-0.195 mag H0 gap: ratio
print("  ratio 0.122/0.188 =", 0.122 / 0.188, "; 0.141/0.195 =", 0.141 / 0.195)

# structure: H r_d = const => fractional change of r_d = 1 - H_ref/H
identity("(r*Hr/H)/r", "Hr/H")
quantity("147.00 Mpc * 67.19 / 73.26", "134.82 Mpc", rel_tol=1e-3)
units("(101.54 Mpc) / (73.26 / 100)", "length")
raise SystemExit(finish())
