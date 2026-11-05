"""M-DIALECTICIAN-13: C-I synthesis and candidate A: '1-2.5 km/s/Mpc, a third to a half of the 6 km/s/Mpc gap'.

Ratio of the sized effect to the gap. Gap taken as 6 km/s/Mpc (lens) and as 6.07 (H0DN - SPA)
or 5.04 (H0DN - P-ACT-LB, the lens's own F8 baseline).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, finish

for gap in (6.0, 6.074, 5.044):
    print(f"gap {gap}: 1/gap = {1/gap:.3f}, 2.5/gap = {2.5/gap:.3f}")
# 'a third to a half' needs 1/gap >= ~0.30 and 2.5/gap >= ~0.45
inequality(f"{1/6.0}", ">=", "0.30")
inequality(f"{2.5/6.0}", ">=", "0.45")
# what effect range would give a third to a half of 6
print(f"a third to a half of 6 km/s/Mpc = {6/3:.1f}-{6/2:.1f} km/s/Mpc")
raise SystemExit(finish())
