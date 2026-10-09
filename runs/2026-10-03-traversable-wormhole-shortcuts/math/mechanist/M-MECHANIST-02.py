"""M-MECHANIST-02: threshold numbers (finding 6, O3).
Delta_sc = T_w - D/c, Delta_ctc = T_w + D/c (from M-MECHANIST-01), with T_w = pi*ell/c, ell = 3e3 ly
(lens input [Q-02], [Q-06]; quoted, not derived here). SI / years.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

# T_w = pi * ell / c with ell = 3000 ly -> years
quantity("pi * 3000 ly / c", "9.4e3 yr", rel_tol=0.01)
Tw = math.pi * 3000.0   # yr
for Dc, sc, ctc in [(1e3, 8.4e3, 1.04e4), (3e3, 6.4e3, 1.24e4)]:
    quantity(f"({Tw} - {Dc}) yr", f"{sc} yr", rel_tol=0.01)
    quantity(f"({Tw} + {Dc}) yr", f"{ctc} yr", rel_tol=0.01)
# Short throat: Delta_ctc = D/c
quantity("1 m / c", "3.3 ns", rel_tol=0.02)
quantity("1 au / c", "499 s", rel_tol=0.002)
quantity("1 ly / c", "1 yr", rel_tol=0.002)
units("1 au / c", "time")
raise SystemExit(finish())
