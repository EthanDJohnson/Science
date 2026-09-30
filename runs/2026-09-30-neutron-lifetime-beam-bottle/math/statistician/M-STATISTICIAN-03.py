"""M-STATISTICIAN-03: look-elsewhere by Sidak (F4, F9).
p_global = 1 - (1 - p_local)^k, z_global = Phi2^-1(p_global) (two-sided). Dimensionless.
Lens: z_loc 4.63 -> 4.40 (k=3), 4.28 (k=5), 4.13 (k=10); material/magnetic 2.95 -> 2.41 (k=5);
PERKEO III vs aSPECT 3.49 -> 3.18 (k=3)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, series, finish
import sympy as sp

p, k = sp.symbols("p k", positive=True)
sid = 1 - (1 - p) ** k
limit(sid, "p", 0, "0")                  # no local excess -> no global excess
series(sid, "p", 0, 2, "k*p")            # small p: Bonferroni limit
identity(sid.subs(k, 1), "p")           # one trial: unchanged

def glob(zl, kk):
    pl = p2(zl)
    return z_of_p2(1 - (1 - pl) ** kk)

ms, ss, c, d, S = wmean(STORAGE); mp_, sp_, *_ = wmean(PROTON)
zl = (mp_ - ms) / q(sp_, ss * S)
for kk, lens in [(3, "4.40"), (5, "4.28"), (10, "4.13")]:
    g = glob(zl, kk); say(f"k={kk}", f"{g:.3f}", lens); identity(f"{g:.2f}", lens)
g = glob(2.95, 5); say("material/magnetic k=5", f"{g:.3f}", "2.41"); identity(f"{g:.2f}", "2.41")
g = glob(3.49, 3); say("PERKEO III/aSPECT k=3", f"{g:.3f}", "3.18"); identity(f"{g:.2f}", "3.18")
raise SystemExit(finish())
