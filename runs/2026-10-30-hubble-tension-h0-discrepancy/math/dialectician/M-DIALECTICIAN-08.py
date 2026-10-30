"""M-DIALECTICIAN-08: precision a one-step probe needs (F7; candidates A and D).

Point hypotheses H_a = 67.19 (CMB-SPA) and H_b = 73.264 (H0DN), km/s/Mpc. A measurement with
Gaussian error sigma separates them at k sigma when |H_b - H_a| = k sigma, so sigma = Delta/k.
Midpoint truth: excluding both poles at k sigma needs sigma = (Delta/2)/k.
Also computed (caveat): if the poles carry their own errors (0.38, 0.806), the requirement becomes
sqrt(sigma^2 + s_pole^2) <= distance/k.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import limit, inequality, units, finish

limit("sqrt(D**2/k**2 - p**2)", "p", 0, "D/k")   # pole error -> 0 recovers the point-hypothesis result

Ha, Hb = 67.19, 73.264
D = Hb - Ha; mid = (Ha + Hb) / 2
s3, s5, smid = D / 3, D / 5, (D / 2) / 3
print(f"Delta = {D:.3f}; sigma(3) = {s3:.3f} ({100*s3/mid:.2f}%); sigma(5) = {s5:.3f} ({100*s5/mid:.2f}%); "
      f"midpoint {mid:.2f}: sigma = {smid:.3f} ({100*smid/mid:.2f}%)")
inequality(f"abs({s3} - 2.02)", "<=", "0.006")
inequality(f"abs({s5} - 1.21)", "<=", "0.006")
inequality(f"abs({smid} - 1.01)", "<=", "0.006")
inequality(f"abs({100*s3/mid} - 2.9)", "<=", "0.05")
inequality(f"abs({100*s5/mid} - 1.73)", "<=", "0.02")
inequality(f"abs({100*smid/mid} - 1.45)", "<=", "0.02")
# caveat: with pole uncertainties
cmb_side = math.sqrt((D / 2 / 3) ** 2 - 0.38**2)
ladder_side = math.sqrt((D / 2 / 3) ** 2 - 0.806**2)
print(f"with pole errors, midpoint exclusion at 3 sigma needs sigma <= {cmb_side:.3f} (CMB side), "
      f"{ladder_side:.3f} (H0DN side) km/s/Mpc = {100*ladder_side/mid:.2f}%")
units("6.074 km/s/Mpc / 3", "km/s/Mpc")
raise SystemExit(finish())
