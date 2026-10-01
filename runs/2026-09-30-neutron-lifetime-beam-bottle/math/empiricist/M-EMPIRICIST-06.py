"""M-EMPIRICIST-06: UCNtau per-year chi2 (F8). Per-year values D-27 (mean of analyses A-D), s.
chi2 about the inverse-variance mean, 4 dof; p = chi2 survival; S = sqrt(chi2/4)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import limit, finish

Y = {"2018": (877.73, 0.32), "2019": (877.80, 0.50), "2020": (879.39, 0.89), "2021": (878.41, 0.58),
     "2022": (876.93, 0.57)}
m, s = wmean(list(Y), Y); c = chi2(list(Y), Y)
print(f"mean {m:.3f} +- {s:.3f} s; chi2 {c:.3f}/4; p {pchi2(c,4):.4f}; S {(c/4)**0.5:.3f}")
agree("chi2", c, 6.67, 0.006); agree("p", pchi2(c, 4), 0.16, 0.006); agree("S", (c / 4) ** 0.5, 1.29, 0.006)
# chi2 survival for 4 dof has closed form exp(-x/2)(1 + x/2): check limit x -> 0 gives 1
limit("exp(-x/2)*(1 + x/2)", "x", 0, "1")
agree("closed-form p", float(mp.exp(-c / 2) * (1 + c / 2)), pchi2(c, 4), 1e-12)
raise SystemExit(finish())
