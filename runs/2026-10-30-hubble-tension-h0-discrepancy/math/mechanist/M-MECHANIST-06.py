"""M-MECHANIST-06: d ln h / d ln ω_c at fixed θ_* and ω_b (background only), and the ω_c change needed
for h: 67.19 -> 73.264. Lens: -0.62; ω_c ~14% low (13.9%); 14σ with an ASSUMED 1% σ(ω_c).
Sign expectation: lower ω_c at fixed θ_* -> larger r_s and the h that restores θ_* rises (negative slope).
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
from math_checks import inequality, finish
from mm_common import near
import mm_bg as B

ob, oc, th = 0.02237, 0.1200, 1.04110e-2
eps = 1e-3
hp, hm = B.h_from_theta(th, ob, oc * (1 + eps)), B.h_from_theta(th, ob, oc * (1 - eps))
deriv = (math.log(hp) - math.log(hm)) / (math.log(1 + eps) - math.log(1 - eps))
near("dlnh/dln omega_c", deriv, -0.62, 0.03)
inequality(f"{deriv!r}", "<", "0")
lin = 100 * (math.exp(math.log(73.264 / 67.19) / deriv) - 1)
near("omega_c change % (linear in logs)", lin, -13.9, 0.6)   # expected FAIL
near("lens -13.9 equals Delta ln omega_c taken as a fraction", 100 * math.log(73.264 / 67.19) / (-0.62), -13.9, 0.1)
# exact: solve for omega_c giving the same h ratio
from scipy.optimize import brentq
h0 = B.h_from_theta(th, ob, oc)
target = h0 * 73.264 / 67.19
oc_need = brentq(lambda x: B.h_from_theta(th, ob, x) - target, 0.05, 0.12, xtol=1e-10)
exact = 100 * (oc_need / oc - 1)
near("omega_c change % (exact solve)", exact, -13.9, 1.0)
near("sigma at 1% (ASSUMED)", abs(exact), 14, 1.0)
raise SystemExit(finish())
