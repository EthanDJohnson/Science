"""M-EXAMINER-01: gap restatements (F2, F6).
Definitions: ladder 5 log10 H0 = M_B + 5 a_B + 25 at fixed a_B (intercept from the Hubble-flow SNe)
  => Delta M_B = 5 log10(H_loc/H_early) (mag).
BAO+SN fix the product r_d*H0 => r_d,new/r_d,old = H_early/H_loc; reduction = 1 - H_early/H_loc.
Fractional gap = (H_loc - H_early)/H_early."""
import math, sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from common import *
from math_checks import identity, limit, quantity, units, finish

H, Hl, MB, aB, C = sp.symbols("H H_l M_B a_B C", positive=True)
# from 5 log10 H = M_B + 5 aB + 25 at fixed aB: M_B(H) = 5 log10 H - 5 aB - 25
MBf = lambda h: 5 * sp.log(h, 10) - 5 * aB - 25
identity(MBf(Hl) - MBf(H), 5 * sp.log(Hl / H, 10))
# r_d from fixed product C = r_d*H0
identity(1 - (C / Hl) / (C / H), 1 - H / Hl)
limit(1 - H / Hl, "H_l", H, 0)  # no gap -> no reduction
limit(5 * sp.log(Hl / H, 10), "H_l", H, 0)
# small-gap limit: Delta M_B ~ (5/ln10) * x
x = sp.symbols("x", positive=True)
limit(5 * sp.log(1 + x, 10) / x, "x", 0, 5 / sp.log(10))

pairs = {"SH0ES vs CMB-SPA": (SH0ES, CMB), "H0DN 73.26 vs BAO+BBN": ((73.26, 0.81, 0.81), BAOBBN),
         "CCHP vs CMB-SPA": (CCHP, CMB), "CCHP vs BAO+BBN": (CCHP, BAOBBN),
         "SH0ES 73.04 vs Planck 67.4": ((73.04, 1.04, 1.04), (67.4, 0.5, 0.5)),
         "SH0ES 73.04 vs CMB-SPA": ((73.04, 1.04, 1.04), CMB), "73.5 vs CMB-SPA": ((73.5, 1, 1), CMB)}
res = {}
for k, (a, b) in pairs.items():
    d = a[0] - b[0]
    pct = 100 * d / b[0]
    dM = 5 * math.log10(a[0] / b[0])
    rd = 100 * (1 - b[0] / a[0])
    z = z_facing(a, b)
    res[k] = (d, z, pct, dM, rd)
    print(f"{k}: diff {d:.2f} km/s/Mpc, z {z:.3f}, gap {pct:.3f}%, dM_B {dM:.4f} mag, r_d reduction {rd:.3f}%")
print("r_d base implied by 134.4 Mpc at -8.57%:", 134.4 / (1 - 0.0857), "Mpc")
print("r_d at 147.09 Mpc * 67.19/73.49:", 147.09 * 67.19 / 73.49, "Mpc")
# compare with the lens's quoted numbers
d, z, pct, dM, rd = res["SH0ES vs CMB-SPA"]
quantity(f"{d}", "6.30", rel_tol=2e-3); quantity(f"{z}", "6.27", rel_tol=2e-3)
quantity(f"{pct}", "9.38", rel_tol=1e-3); quantity(f"{dM}", "0.195", rel_tol=3e-3); quantity(f"{rd}", "8.57", rel_tol=1e-3)
d, z, pct, dM, rd = res["H0DN 73.26 vs BAO+BBN"]
quantity(f"{pct}", "6.95", rel_tol=1e-3); quantity(f"{dM}", "0.146", rel_tol=4e-3); quantity(f"{rd}", "6.50", rel_tol=2e-3)
d, z, pct, dM, rd = res["CCHP vs CMB-SPA"]
quantity(f"{d}", "3.20", rel_tol=2e-3); quantity(f"{z}", "1.62", rel_tol=4e-3)
quantity(f"{pct}", "4.76", rel_tol=1e-3); quantity(f"{dM}", "0.101", rel_tol=5e-3); quantity(f"{rd}", "4.55", rel_tol=1e-3)
d, z, pct, dM, rd = res["CCHP vs BAO+BBN"]
quantity(f"{dM}", "0.059", rel_tol=1e-2); quantity(f"{rd}", "2.7", rel_tol=1e-2)
# D-56 understatement: against 67.19 the requirement is larger than against 67.4
print("reduction 73.04 vs 67.4:", res["SH0ES 73.04 vs Planck 67.4"][4], " vs 67.19:", res["SH0ES 73.04 vs CMB-SPA"][4])
# M_B naive difference (F6)
quantity("-19.253 - (-19.375)", "0.122", rel_tol=1e-6); quantity("-19.253 - (-19.394)", "0.141", rel_tol=1e-6)
units("5 * 1 km/s/Mpc / (1 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
