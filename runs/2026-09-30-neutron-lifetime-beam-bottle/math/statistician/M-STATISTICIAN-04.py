"""M-STATISTICIAN-04: grouped chi2 (F5, F-candidate).
For a partition into classes: chi2_total(all in set, one mean) = chi2_within (sum of per-class chi2 about class means)
+ chi2_between (sum over classes of W_c (m_c - m)^2), dof N-1 = (N-C) + (C-1). z from chi2 p-value, two-sided.
J-PARC symmetrized to 4.16 s. Profile likelihood ratio of two partitions = exp(dchi2/2)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, finish
import math

def between_direct(classes):
    stats = [wmean(c) for c in classes]
    W = [1 / s[1] ** 2 for s in stats]
    m = sum(w * s[0] for w, s in zip(W, stats)) / sum(W)
    return sum(w * (s[0] - m) ** 2 for w, s in zip(W, stats))

def part(classes, label, lens):
    allrows = [r for c in classes for r in c]
    tot = wmean(allrows)[2]
    within = sum(wmean(c)[2] for c in classes)
    dw = sum(len(c) - 1 for c in classes)
    btw = between_direct(classes)
    db = len(classes) - 1
    zb = z_of_p2(chi2_sf(btw, db))
    print(f"{label}: within {within:.2f}/{dw}, between {btw:.2f}/{db} (z {zb:.2f}), total {tot:.2f}  lens {lens}")
    identity(f"{within+btw:.6f}", f"{tot:.6f}")      # decomposition identity
    return within, dw, btw, zb, tot

JP = [JPARC]
identity(f"{JPARC[2]:.2f}", "4.16")
r = part([PROTON, STORAGE], "proton vs storage", "24.1/8, 22.1/1, 4.70")
identity(f"{r[0]:.1f}", "24.1"); identity(f"{r[2]:.1f}", "22.1"); identity(f"{r[3]:.2f}", "4.70")
r2 = part([PROTON, STORAGE + JP], "proton vs rest", "24.2/9, 22.1/1, 4.70")
identity(f"{r2[0]:.1f}", "24.2"); identity(f"{r2[2]:.1f}", "22.1"); identity(f"{r2[3]:.2f}", "4.70")
r3 = part([PROTON + JP, STORAGE], "beam vs storage", "29.5/9, 16.8/1, 4.10")
identity(f"{r3[0]:.1f}", "29.5"); identity(f"{r3[2]:.1f}", "16.8"); identity(f"{r3[3]:.2f}", "4.10")
r4 = part([PROTON, JP, STORAGE], "three classes", "24.1/8, 22.2/2, 4.33")
identity(f"{r4[0]:.1f}", "24.1"); identity(f"{r4[2]:.1f}", "22.2"); identity(f"{r4[3]:.2f}", "4.33")
r5 = part([PROTON, JP, MATERIAL, MAGNETIC], "four classes", "8.4/7 p=0.30, 38.0/3, 5.55")
identity(f"{r5[0]:.1f}", "8.4"); identity(f"{r5[2]:.1f}", "38.0"); identity(f"{r5[3]:.2f}", "5.55")
identity(f"{chi2_sf(r5[0], 7):.2f}", "0.30")
allm = wmean(PROTON + JP + STORAGE)
print("all 11: chi2", allm[2], "S", allm[4], "p", chi2_sf(allm[2], 10))
identity(f"{allm[2]:.1f}", "46.3"); identity(f"{allm[4]:.2f}", "2.15"); identity(f"{chi2_sf(allm[2],10):.1e}", "1.3e-6")
# two-mean fits: total chi2 = within (between is absorbed by two free means)
dchi = r3[0] - r2[0]
print("dchi2 beam/bottle minus proton/rest", dchi, "LR", math.exp(dchi / 2))
identity(f"{dchi:.1f}", "5.3"); identity(f"{math.exp(dchi/2):.0f}", "14")
# BL1 alone vs rest
rb = part([[BL1], [SUS] + STORAGE + JP], "BL1 vs rest", "within 29.2")
identity(f"{rb[0]:.1f}", "29.2")
dd = rb[0] - r2[0]
print("BL1-alone minus proton/rest dchi2", dd, "z-equivalent sqrt", math.sqrt(dd))
raise SystemExit(finish())
