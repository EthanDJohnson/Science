"""M-EMPIRICIST-07: CMB-SPA 67.19 +- 0.38 vs DESI BAO+BBN 68.50 +- 0.58 (km/s/Mpc).
chi^2 = Δ^2/(s1^2 + s2^2) for 1 dof; PDG scale factor S = sqrt(chi^2/(N-1)), N = 2. Claim: 3.57, S = 1.89, ~1.9σ.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, finish
from _common import H, gls, cmp

# for N = 2, chi^2 about the weighted mean equals Δ^2/(s1^2 + s2^2)
identity("(a - (a/s1**2 + b/s2**2)/(1/s1**2 + 1/s2**2))**2/s1**2 + (b - (a/s1**2 + b/s2**2)/(1/s1**2 + 1/s2**2))**2/s2**2",
         "(a-b)**2/(s1**2+s2**2)", domain={"a": (60, 80), "b": (60, 80)})
(a, s1), (b, s2) = H["CMB"], H["BAOBBN"]
c = (a - b) ** 2 / (s1**2 + s2**2)
cmp("chi2", c, 3.57, 0.006)
cmp("S = sqrt(chi2/1)", c ** 0.5, 1.89, 0.006)
raise SystemExit(finish())
