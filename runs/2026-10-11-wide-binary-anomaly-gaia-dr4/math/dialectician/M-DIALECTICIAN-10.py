"""M-DIALECTICIAN-10 (cand C): Boufourou E2 gamma = 1.045 [1.025, 1.068] 'sits about 3 sigma above 1',
'consistent with Delta lnL(gamma=1) = 4.8'. Interval-based z = (1.045 - 1)/(1.045 - 1.025);
likelihood-ratio z = sqrt(2 Delta lnL) (Wilks, 1 dof). Also cand D's DR4 '> 10 sigma_stat' for a gap of 0.033-0.080 at
sigma_stat = 0.005 and C2(ii) N^-1/2 scaling from +-0.2 at N = 36."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import quantity, limit, finish

z_int = (1.045 - 1) / (1.045 - 1.025)
z_lr = math.sqrt(2 * 4.8)
print(f"interval z = {z_int:.3f}; likelihood-ratio z = {z_lr:.3f}")
quantity(f"{z_lr}", "3", rel_tol=0.05)
quantity(f"{z_int}", "3", rel_tol=0.05)          # expected to fail: the interval gives 2.25 sigma
# cand D: gap / sigma_stat; single-family sigma 0.005 each, difference sigma 0.005*sqrt(2) if independent
for gap in (0.033, 0.080):
    print(f"gap {gap}: {gap / 0.005:.1f} sigma (one sigma 0.005), {gap / (0.005 * math.sqrt(2)):.1f} sigma (difference of two)")
quantity(f"{0.033 / (0.005 * math.sqrt(2))}", "4.67", rel_tol=0.01)
# C2(ii): sigma(N) = 0.2 sqrt(36/N)
Nn = sp.symbols("Nn", positive=True)
limit(sp.Rational(1, 5) * sp.sqrt(36 / Nn), "Nn", sp.oo, 0)
for n in (100, 300, 500):
    print(f"N = {n}: sigma = {0.2 * math.sqrt(36 / n):.3f}")
raise SystemExit(finish())
