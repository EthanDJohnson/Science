"""M-EXAMINER-07: Vud needed for tau_beta = BL1 with PERKEO III lambda; unitarity-closure shift (F11).
tau ~ 1/Vud^2  =>  Vud_needed = Vud0 sqrt(tau_beta(Vud0)/tau_BL1). Deficit Delta_u = -0.00166 (D-47) closed by
Vud -> Vud + d with (Vud+d)^2 - Vud^2 = 0.00166. Shift of tau_beta: tau*(Vud/(Vud+d))^2 - tau. Seconds (SI); Vud dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
import sympy as sp
from math_checks import identity, sign, finish
from _inputs import *
from _h import cmp

lam, slam = LAM["PERKEO III"]
C = 5024.46 / ((1 + DRV) * (1 + 3 * lam**2))   # tau * Vud^2; K0 from constants, M-EXAMINER-05 route (a)
t0 = C / VUD**2
v = math.sqrt(C / BL1[0])
# errors: BL1, lambda, RC (Vud0 does not enter: Vud_needed = sqrt(C/tau))
e_t = v * 0.5 * BL1[1] / BL1[0]
e_l = v * 0.5 * 6 * lam / (1 + 3 * lam**2) * slam
e_r = v * 0.5 * SDRV / (1 + DRV)
sv = math.sqrt(e_t**2 + e_l**2 + e_r**2)
print(f"tau_beta(PERKEO III) = {t0:.3f} s; Vud needed for BL1 = {v:.5f} +- {sv:.5f}; below superallowed by {VUD - v:.5f}")
cmp("Vud needed", v, 0.96855, 0.000006)
cmp("sigma", sv, 0.00128, 0.000006)
cmp("offset", VUD - v, 0.00506, 0.000006)
d = math.sqrt(VUD**2 + 0.00166) - VUD
dt = C / (VUD + d) ** 2 - t0
print(f"unitarity closure: dVud = {d:.6f}; dtau = {dt:.3f} s")
cmp("dVud", d, 0.00085, 0.000006)
cmp("dtau", dt, -1.54, 0.006, "s")
V, dd = sp.symbols("V dd", positive=True)
sign(sp.diff(1 / V**2, V), "negative")  # raising Vud always shortens tau_beta
raise SystemExit(finish())
