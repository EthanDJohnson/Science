"""M-DECOMPOSER-01 (F1, ledger L2): inverse-variance combination of BL1 and Sussex-ILL.
m = sum(w x)/sum(w), w = 1/sigma^2, sigma = stat (+) sys; chi2 = sum w (x-m)^2; BL1 weight w1/(w1+w2).
Lifetimes in s (SI)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import identity, limit, units, finish
from _inputs import *

m, s, c2, S = wmean(PROTON)
w1 = 1 / BL1[1] ** 2; w2 = 1 / SIL[1] ** 2
wBL1 = w1 / (w1 + w2)
print(f"sigma_BL1 = {BL1[1]:.4f} s, sigma_SIL = {SIL[1]:.4f} s")
print(f"mean = {m:.3f} +- {s:.3f} s, chi2 = {c2:.3f}/1, BL1 weight = {wBL1:.4f}")
near("class mean (s)", m, 887.97, 0.01)
near("class sigma (s)", s, 2.04, 0.01)
near("chi2", c2, 0.08, 0.01)
near("BL1 weight (lens: 85%)", wBL1, 0.85, 0.01)
near("Sussex-ILL weight (ledger L2: 15%)", 1 - wBL1, 0.15, 0.01)
# Is 85% perhaps a weight computed from stat errors, or from sigma rather than sigma^2?
print(f"alt: stat-only weight {(1/1.2**2)/(1/1.2**2+1/3.0**2):.4f}; 1/sigma weight {(1/BL1[1])/(1/BL1[1]+1/SIL[1]):.4f}")
# Two-point formula identities and limit
identity("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "x1 + (x2 - x1)*s1**2/(s1**2 + s2**2)")
identity("(x1-x2)**2/(s1**2+s2**2)", "(x1 - (x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2))**2/s1**2 + (x2 - (x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2))**2/s2**2")
limit("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "s2", "oo", "x1")
units("887.7 s * 0.8 + 889.2 s * 0.2", "s")
raise SystemExit(finish())
