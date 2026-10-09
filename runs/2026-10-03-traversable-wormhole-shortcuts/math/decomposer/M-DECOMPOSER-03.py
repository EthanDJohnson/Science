"""M-DECOMPOSER-03: MM lags at d = 1000 ly with l = 3e3 ly fixed, L = pi*l (SI via unit_tools)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

ell_ly = 3.0e3
L_ly = math.pi * ell_ly
d_ly = 1.0e3
print(f"L = pi*l = {L_ly:.1f} ly")
quantity(f"{L_ly} ly", "9425 ly", rel_tol=1e-3)
# lag thresholds (M-DECOMPOSER-01): (L-d)/c, (L+d)/c; 1 ly / c = 1 Julian yr
lag_short = f"({L_ly} ly - {d_ly} ly)/c"
lag_ctc = f"({L_ly} ly + {d_ly} ly)/c"
quantity(lag_short, "8425 yr", rel_tol=1e-3)
quantity(lag_ctc, "1.04e4 yr", rel_tol=5e-3)
units(lag_short, "time")
raise SystemExit(finish())
