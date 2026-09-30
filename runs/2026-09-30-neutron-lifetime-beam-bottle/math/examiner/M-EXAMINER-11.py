"""M-EXAMINER-11: precision a new non-proton result needs to 'settle' (lens table A: 1.98 s at 5 sigma, 3.29 s at 3 sigma).
A new result x_new (error s) is compared with a pole P (error s_P): n = Delta / sqrt(s^2 + s_P^2). Required
s = sqrt((Delta/n)^2 - s_P^2), real only if s_P < Delta/n. Delta = 887.7 - 877.82 = 9.88 s. Poles: UCNtau 0.287 s, BL1 2.247 s. SI (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
import sympy as sp
from math_checks import inequality, limit, finish
from _inputs import *
from _h import cmp

D = BL1[0] - U_X
print(f"Delta = {D:.2f} s; lens's numbers are Delta/n: {D/5:.3f} s (5 sigma), {D/3:.3f} s (3 sigma), i.e. pole errors set to zero")
for n in (3, 5):
    for lab, sp_ in (("UCNtau pole", UCNTAU[1]), ("BL1 pole", BL1[1])):
        v = (D / n) ** 2 - sp_**2
        print(f"  n = {n}, {lab}: required s = {math.sqrt(v):.3f} s" if v > 0 else f"  n = {n}, {lab}: impossible (s_P = {sp_:.3f} s > Delta/n = {D/n:.3f} s)")
zmax = D / BL1[1]
print(f"max separation from the BL1 pole even with s -> 0: {zmax:.2f} sigma")
cmp("ceiling vs BL1 pole", zmax, 4.40, 0.005)
# with both poles jointly in a two-hypothesis test (new result predicted at 877.82 under A, 887.7 under C):
# LR test statistic uses the larger-error pole; the 5-sigma distance to the BL1 pole needs s_BL1 < Delta/5
d, s, sP = sp.symbols("d s sP", positive=True)
inequality(d / sp.sqrt(s**2 + sP**2), "<", d / sP, domain={"d": (1, 20), "s": (0.1, 5), "sP": (0.1, 5)})
limit(d / sp.sqrt(s**2 + sP**2), "sP", 0, d / s)  # lens's formula is the sP -> 0 limit
raise SystemExit(finish())
