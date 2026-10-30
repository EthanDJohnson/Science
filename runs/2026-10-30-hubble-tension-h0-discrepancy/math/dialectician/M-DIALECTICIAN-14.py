"""M-DIALECTICIAN-14: cosmic variance 0.31 km/s/Mpc implies gap ~18-20 sigma (candidate F).

gap / sigma_cv for gaps 73.264-67.19, 73.49-67.19 (SH0ES-SPA), and 73.264-68.50 (H0DN-DESI+BBN).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, units, finish

for name, g in (("H0DN-SPA", 73.264 - 67.19), ("SH0ES-SPA", 73.49 - 67.19), ("H0DN-DESI+BBN", 73.264 - 68.50)):
    print(f"{name}: gap {g:.3f} km/s/Mpc = {g/0.31:.1f} x sigma_cv")
inequality(f"{(73.264-67.19)/0.31}", ">=", "18")
inequality(f"{(73.264-67.19)/0.31}", "<=", "20")
print("note: against DESI BAO+BBN (68.50) the gap is 15.4 sigma_cv; 18-20 refers to the CMB-based gap")
units("6.074 km/s/Mpc / (0.31 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
