"""M-STATISTICIAN-05: pairwise tensions (findings 5, 6). gamma dimensionless.
Tension between independent asymmetric estimates: |x1-x2| / sqrt(s1^2 + s2^2), each s on the side facing the other."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, finish
from _h import report

ok = []
# Chae+26 1.60 +0.24 -0.14 vs Saad & Ting 1.00 +0.24 -0.19 on the same 36 pairs, treated as independent
ok.append(report("Chae+26 vs S&T (indep.)", 0.60 / (0.14**2 + 0.24**2) ** 0.5, 2.2, 0.05))
# Boufourou deep 1.11 +- 0.07 vs 1.37 and vs 1
ok.append(report("deep bin vs 1.37", (1.37 - 1.11) / 0.07, 3.7, 0.02))
ok.append(report("deep bin vs Newton", (1.11 - 1.0) / 0.07, 1.6, 0.03))
# C3PO 1.17 +0.37 -0.23
ok.append(report("C3PO vs 1.37 (upper side)", (1.37 - 1.17) / 0.37, 0.5, 0.05))
ok.append(report("C3PO vs 1 (lower side)", (1.17 - 1.0) / 0.23, 0.7, 0.05))
# Same data rho -> 1: var(x1-x2) = (s1-s2)^2 -> with s1~s2 the difference is not a statistical fluctuation
identity("s1**2 + s2**2 - 2*1*s1*s2", "(s1-s2)**2")
# for rho>0 the independent-assumption sigma overstates the difference error, so 2.2 sigma is a lower bound
inequality("s1**2 + s2**2", ">=", "s1**2 + s2**2 - 2*r*s1*s2", domain={"r": (0, 1)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
