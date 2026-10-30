"""M-DIALECTICIAN-12: common magnitude offset a ladder systematic needs (F13), and EDE+ladder residual (C-III ii).

Delta mu = 5 log10(H_ladder/H_target) (H0 ∝ 1/distance, distance modulus shift).
H0DN 73.264 -> CMB-SPA 67.19 and -> DESI BAO+BBN 68.50. C-III(ii): 73.264 -> EDE ceilings 71.0-71.4.
Candidate E: 'about 0.2 mag' between near calibrators and Hubble-flow SNe.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import limit, inequality, units, finish

limit("5*log(1 + x, 10)", "x", 0, "0")
a = 5 * math.log10(73.264 / 67.19); b = 5 * math.log10(73.264 / 68.50)
print(f"to SPA: {a:.4f} mag; to DESI+BBN: {b:.4f} mag")
inequality(f"abs({a} - 0.188)", "<=", "0.0006")
inequality(f"abs({b} - 0.146)", "<=", "0.0006")
for h in (71.0, 71.4):
    print(f"EDE ceiling {h}: ladder excess {73.264-h:.2f} km/s/Mpc = {5*math.log10(73.264/h):.3f} mag")
c1 = 5 * math.log10(73.264 / 71.0); c2 = 5 * math.log10(73.264 / 71.4)
inequality(f"abs({(c1+c2)/2} - 0.06)", "<=", "0.01")
inequality(f"abs({(73.264-71.0 + 73.264-71.4)/2} - 2.0)", "<=", "0.1")
units("73.264 km/s/Mpc / (67.19 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
