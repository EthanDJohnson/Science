"""M-MECHANIST-09: passenger proper time with interior lapse N = 0.761 (SI).

Shell frame: interior observers (static or Eulerian) have dtau = N dt_shell. Shell moves at v
relative to the exterior: dt_shell = dt_ext / gamma. Coast time (exterior) t = d / v, d = 4.37 ly.
Claim: 109.2 yr -> 83.1 yr (0.04 c); 218.5 -> 166.3 yr (0.02 c). 1 g photon rocket: 3.58 yr.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
from math_checks import quantity, limit, finish

N = 0.761
for v, text, tauc in [(0.04, "109.2 yr", "83.1 yr"), (0.02, "218.5 yr", "166.3 yr")]:
    t = 4.37 / v
    g = 1 / math.sqrt(1 - v * v)
    print(f"v={v}: t_ext = {t:.3f} yr; N t = {N*t:.3f} yr; N t / gamma = {N*t/g:.3f} yr")
    quantity(f"{t} yr", text, rel_tol=5e-4)
    quantity(f"{N*t/g} yr", tauc, rel_tol=2e-3)
# 1 g, accelerate then decelerate, d = 4.37 ly (Julian year, ly = c * yr)
c = 2.99792458e8; yr = 365.25 * 86400; a = 9.80665
d = 4.37 * c * yr
phi = math.acosh(1 + a * (d / 2) / c**2)
tau = 2 * c / a * phi
print(f"photon rocket 1 g: phi = {phi:.4f}, tau = {tau/yr:.3f} yr")
quantity(f"{tau} s", "3.58 yr", rel_tol=3e-3)
limit("N_l*d/v", "N_l", 1, "d/v")
raise SystemExit(finish())
