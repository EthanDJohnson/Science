"""M-EXAMINER-03: J-PARC 2024 as discriminator (F6). Lifetimes in s (SI).
Tension z = |x - J| / sqrt(sJ_side^2 + sx_side^2), J's error on the side facing x (stat (+) sys side).
Likelihood ratio LR = exp(-(z_bottle^2 - z_beam^2)/2) (Gaussian, each pole taken at its measured value)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
from math_checks import limit, finish
from _inputs import *
from _h import cmp

def tens(stat_scale=1.0):
    sJup = q(JP_STAT * stat_scale, JP_UP)  # BL1 and UCNtau both lie above 877.2
    d1 = JP_X - BL1[0]
    z1 = abs(d1) / q(sJup, BL1[1])
    d2 = JP_X - U_X
    z2 = abs(d2) / q(sJup, q(U_STAT, U_DN))  # UCNtau side facing J-PARC (below)
    lr = math.exp(-(z2**2 - z1**2) / 2)
    return d1, z1, z2, lr

S = math.sqrt(15.8 / 3)
cmp("internal S", S, 2.30, 0.005)
d1, z1, z2, lr = tens()
print(f"as quoted: J-BL1 = {d1:.2f} s, {z1:.3f} sigma; J-UCNtau {z2:.3f} sigma; LR {lr:.2f}")
cmp("J-PARC - BL1", d1, -10.50, 0.005, "s")
cmp("z vs BL1", z1, 2.15, 0.005)
cmp("z vs UCNtau", z2, 0.14, 0.005)
cmp("LR", lr, 9.9, 0.05)
d1, z1i, z2i, lri = tens(S)
print(f"inflated: {z1i:.3f} sigma vs BL1; {z2i:.3f} vs UCNtau; LR {lri:.2f}")
cmp("inflated z vs BL1", z1i, 1.74, 0.005)
cmp("inflated LR", lri, 4.5, 0.05)

# per-condition (D-24), stat only
low = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7)]
W = sum(1 / s**2 for _, s in low)
m = sum(x / s**2 for x, s in low) / W
print(f"three low conditions: {m:.2f} +- {W**-0.5:.2f} s (stat); UCNtau - m = {U_X - m:.2f} s")
cmp("low-3 mean", m, 869.6, 0.05, "s")
cmp("low-3 sigma", W**-0.5, 2.5, 0.05, "s")
# fourth condition vs BL1: try the plausible error combinations
x4 = 884.8
for lab, s4 in [("stat only", 2.4), ("stat+colB up+colC up", q(2.4, 0.8, 3.2)),
                ("stat+colC up", q(2.4, 3.2))]:
    print(f"  884.8 vs BL1, {lab}: {abs(BL1[0]-x4)/q(s4, BL1[1]):.3f} sigma")
cmp("884.8 vs BL1 (stat (+) upper sys cols)", abs(BL1[0] - x4) / q(2.4, 0.8, 3.2, BL1[1]), 0.64, 0.02)
# limit: as J-PARC's error -> infinity the likelihood ratio -> 1 (no discrimination)
limit("exp(-((a/s)**2 - (b/s)**2)/2)", "s", "oo", "1", domain={"a": (0.1, 1), "b": (5, 15)})
raise SystemExit(finish())
