"""M-DIALECTICIAN-04 (F5): estimator share of the same-catalogue ln-gap,
share = ln(g_E1/g_rob) / ln(g_med/g_rob), with g_med = 1.368 (Chae 2024b), g_rob = 1.045 (Boufourou E2),
g_E1 in [1.12, 1.20] (Boufourou's implied full median). Lens: 26-51% estimator, 49-74% remainder."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, sign, finish

a, b, c = sp.symbols("a b c", positive=True)   # a = ln g_rob < b = ln g_E1 < c = ln g_med
share = (b - a) / (c - a)
identity(share + (c - b) / (c - a), 1)
limit(share, "b", c, 1)
limit(share, "b", a, 0)
sign(sp.diff(share, b), "positive", domain={"a": (0, 0.05), "b": (0.06, 0.2), "c": (0.25, 0.4)})
gap = math.log(1.368 / 1.045)
print("total ln-gap", round(gap, 4))
quantity(f"{gap}", "0.269", rel_tol=0.003)
for gE1, lens in ((1.12, 0.26), (1.20, 0.51)):
    sh = math.log(gE1 / 1.045) / gap
    print(f"g_E1={gE1}: estimator share {sh:.4f} (lens {lens}); remainder {1 - sh:.4f}")
    quantity(f"{sh}", f"{lens}", rel_tol=0.02)
# Linear (not log) shares for comparison
for gE1 in (1.12, 1.20):
    print(f"linear share at {gE1}: {(gE1 - 1.045) / (1.368 - 1.045):.4f}")
raise SystemExit(finish())
