"""M-EMPIRICIST-08: precision needed (F14). A new measurement at one pole, compared with the other pole:
n = Delta/sqrt(sigma^2 + sigma_pole^2) -> sigma_max = sqrt((Delta/n)^2 - sigma_pole^2). Lifetimes in s (SI)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, units, finish

identity("d/sqrt(sqrt((d/n)**2 - p**2)**2 + p**2)", "n", domain={"d": (5, 10), "n": (1, 2), "p": (0.01, 0.5)})
limit("sqrt((d/n)**2 - p**2)", "p", 0, "d/n")
units("(9.56 s)/((1 s)^2 + (0.25 s)^2)^0.5", "dimensionless")

tp, sp_ = wmean(PROTON); ts, ss = wmean(STORAGE); gap = 887.97 - 878.41  # lens's rounded poles, 9.56 s
print(f"gap {gap:.3f} s, storage error {ss:.3f} s")
s3 = ((gap / 3) ** 2 - 0.25 ** 2) ** 0.5; s5 = ((gap / 5) ** 2 - 0.25 ** 2) ** 0.5
print(f"sigma_max 3 sigma {s3:.3f} s, 5 sigma {s5:.3f} s")
agree("3 sigma", s3, 3.18, 0.006); agree("5 sigma", s5, 1.90, 0.006)
zj = gap / q(4.16, 0.25); z1 = gap / q(1, 0.25); z2 = gap / q(2, 0.25)
print(f"J-PARC 4.16 s: {zj:.3f}; at 1 s {z1:.3f}; at 2 s {z2:.3f}")
agree("J-PARC", zj, 2.29, 0.006); agree("1 s", z1, 9.3, 0.06); agree("2 s", z2, 4.7, 0.06)
bl1 = D["BL1"][1]; dB = 887.7 - 878.4
zb1 = dB / q(bl1, 1.0); zb03 = dB / q(bl1, 0.3)
print(f"BL2 at 878.4 vs BL1: sigma 1 s {zb1:.3f}, 0.3 s {zb03:.3f}")
agree("BL2 1 s vs BL1", zb1, 3.8, 0.06); agree("BL2 0.3 s vs BL1", zb03, 4.1, 0.06)
Dn = dict(D, BL2=(888.0, 1.0)); mb, sb = wmean(PROTON + ["BL2"], Dn)
zb = (mb - ts) / q(sb, ss); print(f"beam class with BL2 at 888 +- 1: {mb:.3f} +- {sb:.3f}; vs storage {zb:.2f} sigma")
inequality(repr(zb), ">=", "9")
mm, sm = wmean(MATERIAL); mg, sg = wmean(MAGNETIC); dm = mm - mg
m3 = ((dm / 3) ** 2 - sg ** 2) ** 0.5; m5 = ((dm / 5) ** 2 - sg ** 2) ** 0.5
print(f"material-magnetic {dm:.3f} s; new bottle 3 sigma {m3:.3f} s, 5 sigma {m5:.3f} s")
agree("mat-mag diff", dm, 2.20, 0.006); agree("new bottle 3 sigma", m3, 0.67, 0.006)
agree("new bottle 5 sigma", m5, 0.33, 0.006)
h = 885.7 - 878.5; zh = h / q(0.8, 0.8); zh2 = h / q(0.8, D["SER05"][1])
print(f"2005 history: {h:.2f} s, {zh:.3f} sigma (0.8 (+) 0.8), {zh2:.3f} sigma (0.8 (+) 0.762), ratio to gap {h/gap:.3f}")
agree("history sigma", zh, 6.4, 0.06); agree("history ratio", h / gap, 0.75, 0.006)
raise SystemExit(finish())
