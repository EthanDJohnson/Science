"""M-DIALECTICIAN-08: (a) BL1 vs UCNtau significance with BL1's total error scaled by k;
(b) error sigma a future experiment needs to separate 877.8 s from 887.7 s at n sigma (sigma = gap/n, lens's convention). SI: s."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

gap = BL1 - UCN
for k, want in [(1, 4.36), (1.5, 2.92), (2, 2.19), (2.3, 1.91)]:
    z_face = gap / q(k * sBL1, sUCN_up)
    z_sym = gap / q(k * sBL1, sUCN_sym)
    print(f"k = {k}: z = {z_face:.3f} (UCNtau upper side), {z_sym:.3f} (symmetrized)")
    num(f"z at k={k}", z_face, want, unit="", abs_tol=0.006)
for n, want in [(5, 2.0), (3, 3.3)]:
    s = (887.7 - 877.8) / n
    print(f"{n} sigma: sigma = {s:.3f} s")
    num(f"sigma for {n} sigma", s, want, abs_tol=0.051)
# With the poles' own errors (BL1 2.25 s dominates) the requirement is sigma = sqrt((gap/n)^2 - ...) only if the
# comparison is against a pole value; the lens's figure is the bare gap/n. Note the BL1 pole error alone exceeds 1.98 s:
print(f"BL1 pole error {sBL1:.3f} s vs gap/5 {(887.7-877.8)/5:.3f} s")
limit("g/sqrt((k*s)**2 + u**2)", "k", "oo", "0", domain={"g": (1, 20), "s": (0.5, 5), "u": (0.1, 1)})
units("(887.7 s - 877.82 s)/(2.25 s)", "dimensionless")
raise SystemExit(finish())
