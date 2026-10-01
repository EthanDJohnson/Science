"""M-STATISTICIAN-05: J-PARC 2024 tensions (F6). J = 877.2 s, stat 1.7, sys +4.0/-3.6 s; errors added in
quadrature; side facing the other value (other value above J -> upper side). z = |x - J|/sqrt(sJ_side^2 + sx^2).
Inflated: stat * S_J with S_J = sqrt(15.8/3). Stat-only chi2 of the four conditions (D-24)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish
import sympy as sp

mp_, sp_, *_ = wmean(PROTON)
ms, ss, c, d, S = wmean(STORAGE); ss *= S
def zt(x, sx, stat=1.7):
    side = q(stat, 4.0) if x > JP_VAL else q(stat, 3.6)
    return (x - JP_VAL), q(side, sx), abs(x - JP_VAL) / q(side, sx)
Dp, sDp, zp = zt(mp_, sp_); say("vs proton", f"{-Dp:.2f} +- {sDp:.2f}, {zp:.2f}", "-10.77 +- 4.80, 2.24")
identity(f"{-Dp:.2f}", "-10.77"); identity(f"{sDp:.2f}", "4.80"); identity(f"{zp:.2f}", "2.24")
_, _, zb = zt(BL1[1], BL1[2]); say("vs BL1", f"{zb:.2f}", "2.15"); identity(f"{zb:.2f}", "2.15")
Ds, sDs, zs = zt(ms, ss); say("vs storage", f"{-Ds:.2f} +- {sDs:.2f}, {zs:.2f}", "-1.12 +- 4.37, 0.26")
identity(f"{-Ds:.2f}", "-1.12"); identity(f"{sDs:.2f}", "4.37"); identity(f"{zs:.2f}", "0.26")
SJ = (15.8 / 3) ** 0.5; say("S_J", f"{SJ:.3f}", "2.29"); identity(f"{SJ:.2f}", "2.29")
_, _, zpi = zt(mp_, sp_, 1.7 * SJ); _, _, zsi = zt(ms, ss, 1.7 * SJ)
say("inflated", f"{zpi:.2f} / {zsi:.2f}", "1.81 / 0.20")
identity(f"{zpi:.2f}", "1.81"); identity(f"{zsi:.2f}", "0.20")
cond = [("100/old", 870.9, 3.5), ("100/new", 868.3, 4.0), ("50/old", 868.2, 7.7), ("50/new", 884.8, 2.4)]
cm = wmean(cond); say("stat-only chi2", f"{cm[2]:.2f}/3", "19.6/3"); identity(f"{cm[2]:.1f}", "19.6")
# limit: tension vanishes as the error grows
x, s = sp.symbols("x s", positive=True)
limit(sp.Abs(x) / sp.sqrt(s**2 + 1), "s", sp.oo, "0")
raise SystemExit(finish())
