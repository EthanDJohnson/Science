"""M-STATISTICIAN-09: storage internal splits (F9, S3, S7). Lifetimes in s.
Lens: material - magnetic = 2.22 +- 0.75 s, 2.95 sigma (material scaled); Serebrov18 vs Musedinovic25 3.80 sigma;
UCNtau per-year (D-27) chi2 6.67/4, p 0.155, S 1.29; 2020 - 2022 = 2.46 s, 2.3 sigma."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, finish

mm = wmean(MATERIAL); mg = wmean(MAGNETIC)
D = mm[0] - mg[0]; sD = q(mm[1] * mm[4], mg[1]); print("material-magnetic", D, sD, D / sD)
identity(f"{D:.2f}", "2.22"); identity(f"{sD:.2f}", "0.75"); identity(f"{D/sD:.2f}", "2.95")
s18 = MATERIAL[4]; mu = MAGNETIC[0]
z_sym = (s18[1] - mu[1]) / q(s18[2], mu[2]); z_side = (s18[1] - mu[1]) / q(s18[2], q(0.22, 0.20))
print("Serebrov18 vs Musedinovic25: symmetrized", z_sym, "facing side", z_side)
identity(f"{z_side:.2f}", "3.80")
yrs = [("2018", 877.73, 0.32), ("2019", 877.80, 0.50), ("2020", 879.39, 0.89), ("2021", 878.41, 0.58), ("2022", 876.93, 0.57)]
y = wmean(yrs); print("per-year", y, "p", chi2_sf(y[2], 4))
identity(f"{y[2]:.2f}", "6.67"); identity(f"{chi2_sf(y[2],4):.3f}", "0.155"); identity(f"{y[4]:.2f}", "1.29")
z = (879.39 - 876.93) / q(0.89, 0.57); print("2020-2022", z); identity(f"{z:.1f}", "2.3")
raise SystemExit(finish())
