"""M-EMPIRICIST-01: class weighted means (F5, F8, F14).
Inverse-variance mean m = sum(w x)/sum(w), w = 1/sigma^2, sigma_m = 1/sqrt(sum w); chi2 = sum w (x - m)^2;
S = sqrt(chi2/(N-1)). Lifetimes in s (SI)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, units, finish

for k, (x, s) in D.items():
    print(f"{k}: {x} +- {s:.4f} s")

# Limits of the weighted mean: equal errors -> arithmetic mean; sigma2 -> oo -> x1
identity("(x1/s**2 + x2/s**2)/(1/s**2 + 1/s**2)", "(x1 + x2)/2")
limit("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "s2", "oo", "x1")
units("(887.7 s / (2.25 s)^2 + 878.4 s / (0.29 s)^2) / (1/(2.25 s)^2 + 1/(0.29 s)^2)", "s")

mp_, sp_ = wmean(PROTON); print(f"proton {mp_:.3f} +- {sp_:.3f} s")
agree("proton mean", mp_, 887.97, 0.006); agree("proton sigma", sp_, 2.04, 0.006)
mm, sm = wmean(MATERIAL); cm = chi2(MATERIAL)
print(f"material {mm:.3f} +- {sm:.3f} s, chi2 {cm:.3f}/4, S {(cm/4)**0.5:.3f}")
agree("material mean", mm, 880.03, 0.006); agree("material sigma", sm, 0.49, 0.006)
agree("material chi2", cm, 8.2, 0.05); agree("material S", (cm / 4) ** 0.5, 1.43, 0.006)
mg, sg = wmean(MAGNETIC); print(f"magnetic {mg:.3f} +- {sg:.3f} s")
agree("magnetic mean", mg, 877.83, 0.006); agree("magnetic sigma", sg, 0.29, 0.006)
ms, ss = wmean(STORAGE); print(f"storage {ms:.3f} +- {ss:.3f} s, chi2 {chi2(STORAGE):.2f}/6")
agree("storage mean", ms, 878.41, 0.006); agree("storage sigma", ss, 0.25, 0.006)
raise SystemExit(finish())
