"""M-EXAMINER-02: material bottles vs magnetic traps (F5) and the loss rate the difference needs (F7).
Weighted means (s, SI), z = (m1 - m2)/sqrt(s1^2 + s2^2); rate difference 1/tau_a - 1/tau_b in s^-1."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
from math_checks import identity, series, units, finish
from _inputs import *
from _h import cmp

mm, sm, chm, _ = wmean(MATERIAL)
mg, sg, chg, _ = wmean(MAGNETIC)
w, dw, b, db, tot = grouped([MATERIAL, MAGNETIC])
print(f"material {mm:.3f} +- {sm:.3f} s (chi2 {chm:.2f}/4); magnetic {mg:.3f} +- {sg:.3f} s (chi2 {chg:.3f}/1)")
cmp("material mean", mm, 880.03, 0.005, "s")
cmp("material sigma", sm, 0.49, 0.005, "s")
cmp("magnetic mean", mg, 877.83, 0.005, "s")
cmp("magnetic sigma", sg, 0.28, 0.005, "s")
cmp("between chi2", b, 15.07, 0.005)
z = (mm - mg) / q(sm, sg)
cmp("z material-magnetic", z, 3.88, 0.005)
# scaled alternative (S of material class), for context only
S = (chm / 4) ** 0.5
print(f"material internal S = {S:.3f}; z with material error scaled by S = {(mm-mg)/q(sm*S, sg):.3f}")

MOD = {k: MATERIAL[k] for k in ("Grav", "MAMBO", "Arz")}
m3, s3, ch3, _ = wmean(MOD)
z3 = (m3 - mg) / q(s3, sg)
print(f"modern material {m3:.3f} +- {s3:.3f} s, z = {z3:.3f}")
cmp("modern material mean", m3, 880.97, 0.005, "s")
cmp("modern material sigma", s3, 0.68, 0.005, "s")
cmp("modern z", z3, 4.28, 0.005)

# loss rate for the material-magnetic difference; which pair gives 4.8e-6 s^-1?
for lab, a, bb in [("class means", mm, mg), ("modern material vs magnetic", m3, mg),
                   ("Gravitrap vs UCNtau", GRAV[0], U_X), ("3 s at 878 s", 881.0, 878.0)]:
    r = 1 / bb - 1 / a
    print(f"  rate {lab}: {a:.2f} vs {bb:.2f} s -> {r:.3e} s^-1")
cmp("rate Gravitrap vs UCNtau", 1 / U_X - 1 / GRAV[0], 4.8e-6, 0.05e-6, "1/s")
cmp("'about a third of the gap' (3 s / 9.88 s)", 3.0 / (BL1[0] - U_X), 0.33, 0.04)

import sympy as sp
a, d = sp.symbols("a d", positive=True)
series(1 / a - 1 / (a + d), "d", 0, 2, d / a**2)  # small-difference limit: rate ~ delta/tau^2
units("1/(877.83 s) - 1/(880.97 s)", "1/s")
raise SystemExit(finish())
