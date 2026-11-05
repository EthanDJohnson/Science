"""M-DIALECTICIAN-03: probability of the selection draw (F2, C-I 'p ~ 0.01-0.02').

Gaussian tail for z in 2.3-2.9 (nested) and 2.4-3.0 (disjoint) from M-02.
p_two = erfc(z/sqrt2); p_one = p_two/2.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, limit, finish

# identity: two-sided tail = erfc(z/sqrt2) = 2(1 - Phi(z))
identity("erfc(z/sqrt(2))", "2*(1 - (1 + erf(z/sqrt(2)))/2)", domain={"z": (0, 5)})
limit("erfc(z/sqrt(2))", "z", 0, "1")

for z in (2.3, 2.4, 2.9, 3.0):
    p2 = math.erfc(z / math.sqrt(2))
    print(f"z={z}: two-sided p={p2:.4f}, one-sided p={p2/2:.4f}")
p_hi = math.erfc(2.3 / math.sqrt(2)); p_lo = math.erfc(2.9 / math.sqrt(2))
# Lens claims p in 0.01-0.02 over the whole 2.3-2.9 sigma range.
inequality(f"{p_hi}", "<=", "0.022")      # upper end consistent (two-sided at 2.3 sigma)
inequality(f"{p_lo}", ">=", "0.01")       # lower end: does 2.9 sigma still give p >= 0.01?
inequality(f"{p_lo/2}", ">=", "0.01")     # even one-sided?
raise SystemExit(finish())
