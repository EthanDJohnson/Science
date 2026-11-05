"""M-EXAMINER-10: F1 model spread, F9 cosmic-variance ratio, premise-ledger all-local vs CMB-SPA 6.85 sigma,
EXAMINER-H BAO+BBN 4.6 sigma below the all-local mean.
All-local mean: inverse-variance mean of the 7 local classes (symmetrised, independent)."""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from common import *
from math_checks import quantity, inequality, finish

quantity("71.0 - 63.6", "7.40", rel_tol=1e-9)
inequality("71.0 - 63.6", ">", "73.49 - 67.19")
print("gap/CV:", 5.6 / 0.31, 6.30 / 0.31)
quantity("5.6/0.31", "18", rel_tol=1e-2); quantity("6.30/0.31", "20", rel_tol=2e-2)
loc = [sym(m) for m in (SH0ES, CCHP, SBF, TF, TD, MASER, SIREN)]
mu, s, chi = wmean(loc)
zc = (mu - CMB[0]) / math.hypot(s, CMB[1]); zb = (mu - BAOBBN[0]) / math.hypot(s, BAOBBN[1])
print(f"all-local {mu:.3f} +- {s:.3f} (chi2 {chi:.2f}/6); vs CMB-SPA {zc:.3f}; vs BAO+BBN {zb:.3f}")
quantity(f"{zc}", "6.85", rel_tol=5e-3); quantity(f"{zb}", "4.6", rel_tol=1.2e-2)
raise SystemExit(finish())
