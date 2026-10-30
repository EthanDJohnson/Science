"""M-DIALECTICIAN-04: SH0ES - CCHP-JWST split (F3).

Inputs: SH0ES 73.49 [D-20]; CCHP JWST-only 68.81 [D-25]; HST on CCHP-selected subset 71.2,
SH0ES-selected 73.6-73.9 (mid 73.75) [D-28]; Hoyt spread 68.4-69.6 [D-25]. All km/s/Mpc.
Lens: 4.68 = 2.55 (selection) + 2.39 (residual, 0.074 mag); Hoyt 1.2 km/s/Mpc = 0.036 mag.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, quantity, finish

tot = 73.49 - 68.81
sel_lens = 73.75 - 71.2
sel_alt = 73.49 - 71.2
resid = 71.2 - 68.81
print(f"total {tot:.2f}; selection (73.75-71.2) {sel_lens:.2f}; selection (73.49-71.2) {sel_alt:.2f}; "
      f"residual (71.2-68.81) {resid:.2f}")
print(f"2.55 + 2.39 = {2.55+2.39:.2f} vs total {tot:.2f}; total - 2.55 = {tot-2.55:.2f}")
quantity("73.49 km/s/Mpc - 68.81 km/s/Mpc", "4.68 km/s/Mpc", rel_tol=1e-3)
# Does the stated decomposition add up?
inequality(f"abs(2.55 + 2.39 - {tot})", "<=", "0.05")
# consistent decompositions
inequality(f"abs({sel_alt} + {resid} - {tot})", "<=", "1e-9")
dm_res = 5 * math.log10(71.2 / 68.81)
dm_res_alt = 5 * math.log10((68.81 + tot - 2.55) / 68.81)
print(f"residual 71.2/68.81 -> {dm_res:.4f} mag; residual if selection=2.55 -> {tot-2.55:.2f} km/s/Mpc = {dm_res_alt:.4f} mag")
inequality(f"abs({dm_res} - 0.074)", "<=", "0.001")
dm_hoyt = 5 * math.log10(69.6 / 68.4)
print(f"Hoyt 69.6/68.4 -> {dm_hoyt:.4f} mag; 1.2/73.26 linear -> {5/math.log(10)*1.2/73.26:.4f} mag")
inequality(f"abs({dm_hoyt} - 0.036)", "<=", "0.003")
raise SystemExit(finish())
