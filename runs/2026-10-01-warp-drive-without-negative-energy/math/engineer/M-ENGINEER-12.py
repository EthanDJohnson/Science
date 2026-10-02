"""M-ENGINEER-12 (F16): photon thrust per watt F/P = 1/c = 3.3 nN/W; a 1.2 uN/W claim exceeds it by
log10(1.2e-6/3.3e-9) = 2.6 orders. SI."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import quantity, units, limit, finish

quantity("1/c", "3.336 nN/W", rel_tol=1e-3)
units("1 W / c", "N")
near("orders 1.2 uN/W over 1/c", lg(1.2e-6 * c), 2.6, 0.05)
limit("1/k", "k", "oo", "0")
raise SystemExit(finish())
