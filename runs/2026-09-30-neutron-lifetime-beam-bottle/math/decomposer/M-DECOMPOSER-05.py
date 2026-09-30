"""M-DECOMPOSER-05 (F5): J-PARC 2024 tensions, internal scale factor, likelihood ratios, three-condition mean.
Totals: up = 1.7 (+) 4.0, down = 1.7 (+) 3.6; pairwise z uses the J-PARC side facing the other value.
S_J = sqrt(15.8/3) applied to stat only. Likelihood ratio definitions tried:
 (a) simple point hypotheses tau = x_S vs tau = x_B, J-PARC error only: exp((zB^2 - zS^2)/2)
 (b) pole errors added in quadrature, exponent only; (c) (b) with Gaussian normalisation.
SI (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import limit, identity, finish
from _inputs import *

up = q(JP_STAT, JP_UP); dn = q(JP_STAT, JP_DN)
print(f"J-PARC totals +{up:.3f} / -{dn:.3f} s")
near("J-PARC up total", up, 4.35, 0.005); near("J-PARC down total", dn, 3.98, 0.005)
mp_, sp_, _, _ = wmean(PROTON)
def zj(x, sx, sJ):
    return abs(x - JP) / q(sx, sJ)
# J-PARC (877.2) is below all three comparison values, so the facing side is "up".
zB = zj(*BL1, up); zBS = zj(mp_, sp_, up); zU = zj(*UCNT, up)
print(f"z: BL1 {zB:.3f}, BL1+SIL {zBS:.3f}, UCNtau {zU:.3f}")
near("vs BL1", zB, 2.15, 0.005); near("vs BL1+SIL", zBS, 2.24, 0.005); near("vs UCNtau", zU, 0.14, 0.005)
SJ = math.sqrt(15.8 / 3); upS = q(JP_STAT * SJ, JP_UP)
zBs = zj(*BL1, upS)
print(f"S_J = {SJ:.4f}; scaled up total {upS:.3f}; vs BL1 {zBs:.3f}")
near("S_J", SJ, 2.29, 0.005); near("scaled vs BL1", zBs, 1.74, 0.005)
for tag, sJ, want in (("quoted", up, 18), ("scaled", upS, 5.8)):
    za = abs(BL1[0] - JP) / sJ; zs = abs(UCNT[0] - JP) / sJ
    LRa = math.exp((za ** 2 - zs ** 2) / 2)
    zb_ = zj(*BL1, sJ); zs_ = zj(*UCNT, sJ)
    LRb = math.exp((zb_ ** 2 - zs_ ** 2) / 2)
    LRc = LRb * q(BL1[1], sJ) / q(UCNT[1], sJ)
    print(f"{tag}: LR point {LRa:.2f}; with pole errors {LRb:.2f}; normalised {LRc:.2f}")
    near(f"LR {tag} (point-hypothesis definition)", LRa, want, 0.05 * want)
# three mutually consistent conditions (stat only) and the fourth
three = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7)]
m3, s3, c3, _ = wmean(three)
print(f"three-condition mean {m3:.3f} +- {s3:.3f} (chi2 {c3:.3f}/2); fourth 884.8 +- 2.4; gap {(884.8-m3)/q(s3,2.4):.2f} sigma")
near("three-condition mean", m3, 869.6, 0.05); near("three-condition sigma", s3, 2.5, 0.05)
m4, s4, c4, _ = wmean(three + [(884.8, 2.4)])
print(f"all four, stat only: {m4:.3f} +- {s4:.3f}, chi2 {c4:.2f}/3")
# limits: tension vanishes as J-PARC error grows; LR -> 1
limit("exp(((xb-j)**2 - (xs-j)**2)/(2*s**2))", "s", "oo", "1")
identity("exp(za**2/2)/exp(zs**2/2)", "exp((za**2-zs**2)/2)")
raise SystemExit(finish())
