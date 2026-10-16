#!/usr/bin/env python3
"""M-MECH-07  Motion blur is rotation-dominated.

CLAIM (mechanist finding 7, candidate MECH-B)
  Symbols: f focal length [px]; omega body rate [rad/s]; v forward/lateral speed [m/s];
  d distance to the feature [m]; t_exp exposure [s]. Assumptions: pinhole camera, feature near
  the optical axis, pure rotation about an axis perpendicular to the line of sight, translation
  perpendicular to the line of sight (the largest-blur case), blur = (image-plane rate) t_exp.
  Claimed: blur_rot = f omega t_exp = 3.9 px/ms at omega = 500 deg/s with f = 447 px;
  blur_trans = f (v/d) t_exp = 1.8 px/ms at v = 20 m/s, d = 5 m; ratio = omega d/v = 2.2.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

f848 = 848 / (2 * math.tan(math.radians(87.0) / 2))
print(f"inputs: 848 px over 87 deg -> f = {f848:.2f} px (lens: 447 px)")
quantity(f"{f848:.6f} m", "447 m", rel_tol=5e-3)

# ---------------------------------------------------------------- ratio is a pure geometry result
f, w, v, d, te = sp.symbols("f w v d t_e", positive=True)
blur_rot = f * w * te
blur_tr = f * v / d * te
identity(sp.simplify(blur_rot / blur_tr), w * d / v,
         domain={"f": (10, 2000), "w": (0.1, 50), "v": (0.1, 50), "d": (0.5, 50), "t_e": (1e-4, 1e-2)})
limit(blur_rot / blur_tr, "d", 0, 0)       # very close features are translation-dominated
units("447 * 8.727/s * 1 ms", "")          # px are dimensionless: blur in px
units("447 * (20 m/s)/(5 m) * 1 ms", "")

W = math.radians(500.0)
br = f848 * W * 1e-3            # px per ms
bt = f848 * (20.0 / 5.0) * 1e-3
print(f"blur_rot(500 deg/s = {W:.4f} rad/s) = {br:.3f} px/ms   (lens: 3.9)")
print(f"blur_trans(20 m/s at 5 m)          = {bt:.3f} px/ms   (lens: 1.8)")
print(f"ratio = {br/bt:.3f}   (lens: 2.2); closed form omega d/v = {W*5.0/20.0:.3f}")
quantity(f"{br:.6f} m", "3.9 m", rel_tol=2e-2)
quantity(f"{bt:.6f} m", "1.8 m", rel_tol=2e-2)
quantity(f"{br/bt:.6f} m", "2.2 m", rel_tol=2e-2)

# the crossover: rotation dominates whenever omega > v/d
print(f"rotation dominates for omega > v/d = {20.0/5.0:.2f} rad/s = "
      f"{math.degrees(20.0/5.0):.0f} deg/s at (20 m/s, 5 m)")

raise SystemExit(finish())
