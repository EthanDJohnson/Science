"""M-DIALECTICIAN-10: f_EDE profile best fit vs Bayesian 95% upper limits (F9).

(0.09 - f_lim)/0.03 for f_lim = 0.061 (Planck NPIPE) and 0.070 (SPT+ACT+Planck) [D-53].
Dimensionless. Also the calc summary's '0.07-0.97 sigma' is compared with F9's '0.67-0.97'.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, limit, finish

limit("(f - flim)/s", "f", "flim", "0")
a = (0.09 - 0.061) / 0.03; b = (0.09 - 0.070) / 0.03
print(f"distance above 0.061: {a:.3f} sigma; above 0.070: {b:.3f} sigma")
inequality(f"abs({a} - 0.97)", "<=", "0.005")
inequality(f"abs({b} - 0.67)", "<=", "0.005")
print(f"Calculations bullet says 0.07-0.97 sigma; F9 says 0.67-0.97; computed lower end {b:.3f} -> the 0.07 is a typo")
raise SystemExit(finish())
