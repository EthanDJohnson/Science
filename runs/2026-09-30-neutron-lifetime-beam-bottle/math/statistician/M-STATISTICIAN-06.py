"""M-STATISTICIAN-06: likelihood ratios between the two poles (F6, F11, discriminating-power table).
Test datum x +- sx; poles S (storage 878.32 +- 0.43 scaled) and B (proton beam 887.97 +- 2.04).
(a) profile LR = exp(-(z_S^2 - z_B^2)/2), z_P = (x - P)/sqrt(sx^2 + sP^2)  [= exp(dchi2/2) of two-mean fits]
(b) marginal LR with flat prior on the pole means = (sB'/sS') exp(...), s' = sqrt(sx^2 + sP^2)
(c) strict point hypotheses (pole values exact) = exp(-((x-S)^2 - (x-B)^2)/(2 sx^2))
Lens numbers: J-PARC 12:1 (5:1 inflated), posterior 0.92 (0.84); PERKEO III tau_b 878.50+-0.88: 8.7e3;
aSPECT 889.58+-3.20: 2.5e-3 (1:400); PDG 879.65+-1.61: 122. J-PARC 2024 setup never reaches 3 sigma."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, inequality, finish
import sympy as sp

mp_, sp_, *_ = wmean(PROTON)
ms, ss, c, d, S = wmean(STORAGE); ss *= S

def lrs(x, sxS, sxB):
    sS, sB = q(sxS, ss), q(sxB, sp_)
    zS, zB = (x - ms) / sS, (x - mp_) / sB
    prof = math.exp(-(zS**2 - zB**2) / 2)
    marg = prof * sB / sS
    return zS, zB, prof, marg

# J-PARC: side facing both poles is the upper side (both poles above 877.2)
for lab, stat, lens, post in [("J-PARC quoted", 1.7, "12", "0.92"), ("J-PARC inflated", 1.7 * math.sqrt(15.8/3), "5", "0.84")]:
    up = q(stat, 4.0)
    zS, zB, prof, marg = lrs(JP_VAL, up, up)
    pt = math.exp(-((JP_VAL - ms)**2 - (JP_VAL - mp_)**2) / (2 * up**2))
    print(f"{lab}: profile LR {prof:.2f} (lens {lens}), marginal {marg:.2f}, strict-point {pt:.2f}, posterior(even) {prof/(1+prof):.3f} (lens {post})")
    identity(f"{prof:.0f}", lens); identity(f"{prof/(1+prof):.2f}", post)
for lab, x, sx, lens in [("PERKEO III", 878.50, 0.88, 8.7e3), ("aSPECT24", 889.58, 3.20, 2.5e-3), ("PDG", 879.65, 1.61, 122)]:
    zS, zB, prof, marg = lrs(x, sx, sx)
    print(f"{lab}: zS {zS:.2f} zB {zB:.2f} profile LR {prof:.4g} (lens {lens}), marginal {marg:.4g}")
    identity(f"{prof:.2g}", f"{lens:.2g}")
# symbolic: marginal/profile ratio -> 1 when the pole errors are equal
a, b = sp.symbols("a b", positive=True)
limit(sp.sqrt(1 + b**2) / sp.sqrt(1 + a**2), "b", a, "1")
# J-PARC setup floor: stat -> 0, sys 3.8 s (mean of sides)
floor_BS = 9.65 / math.sqrt(3.8**2 + sp_**2)
floor_S = 9.65 / math.sqrt(3.8**2 + ss**2)
print("J-PARC stat->0: vs proton pole", floor_BS, "vs storage pole", floor_S)
inequality(f"{floor_BS}", "<", "3"); inequality(f"{floor_S}", "<", "3")
raise SystemExit(finish())
