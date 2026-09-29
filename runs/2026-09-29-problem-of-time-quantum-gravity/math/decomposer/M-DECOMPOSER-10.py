# M-DECOMPOSER-10: how many orders of magnitude the superposed-source rate shifts lie below the
# demonstrated fractional clock resolution 7.6e-21 (Q-05, dimensionless). Lens: "20-30 orders".
import sys, math; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish
res = 7.6e-21
for name, shift in (("QGEM linear 9.2e-39", 9.2e-39), ("QGEM exact max 2.06e-38", 2.06e-38),
                    ("QGEM exact min 5.9e-39", 5.9e-39), ("1 g at 1 mm 7.4e-31", 7.4e-31)):
    print(f"{name}: log10(res/shift) = {math.log10(res/shift):.2f}")
quantity(f"{math.log10(res/9.2e-39)}", "17.9", rel_tol=0.01)
quantity(f"{math.log10(res/7.4e-31)}", "10.0", rel_tol=0.01)
# The claim "at least 20 orders below" requires log10(res/shift) >= 20 for both cases:
inequality(f"{math.log10(res/9.2e-39)}", ">=", "20")
inequality(f"{math.log10(res/7.4e-31)}", ">=", "20")
# Against the lambda*omega coupling (2.35e-60) the gap is ~40 orders, so "20-30" matches neither comparison
quantity(f"{math.log10(res/2.35e-60)}", "39.5", rel_tol=0.01)
raise SystemExit(finish())
